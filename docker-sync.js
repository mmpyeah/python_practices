// ==UserScript==
// @name         Docker Hub → 阿里云镜像一键同步
// @namespace    http://tampermonkey.net/
// @version      1.3
// @description  在 Docker Hub 镜像页注入按钮，一键触发 GitHub Actions 同步到阿里云
// @author       Leo
// @match        https://hub.docker.com/_/*
// @match        https://hub.docker.com/r/*/*
// @grant        GM_xmlhttpRequest
// @grant        GM_getValue
// @grant        GM_setValue
// @grant        GM_addStyle
// @connect      workers.dev
// ==/UserScript==

(function () {
  'use strict';

  // ========== 配置区（首次使用需填写） ==========
  const CONFIG_KEY = 'dockerhub_sync_config';

  function getConfig() {
    const saved = GM_getValue(CONFIG_KEY, null);
    return saved ? JSON.parse(saved) : {
      workerUrl: 'https://docker-sync.tianfeng0v0.workers.dev/',    // Cloudflare Worker URL，如 https://docker-sync.xxx.workers.dev
      callSecret: 'd27d9U0Z',   // 与 Worker 环境变量 CALL_SECRET 一致的调用密钥
    };
  }

  function saveConfig(cfg) {
    GM_setValue(CONFIG_KEY, JSON.stringify(cfg));
  }

  // ========== 样式 ==========
  GM_addStyle(`
    #dh-sync-btn {
      position: fixed;
      bottom: 32px;
      right: 32px;
      z-index: 99999;
      background: #0066cc;
      color: #fff;
      border: none;
      border-radius: 8px;
      padding: 10px 18px;
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
      box-shadow: 0 2px 8px rgba(0,0,0,0.18);
      display: flex;
      align-items: center;
      gap: 8px;
    }
    #dh-sync-btn:hover { background: #0052a3; }
    #dh-sync-btn:disabled { background: #888; cursor: not-allowed; }

    #dh-sync-overlay {
      position: fixed; inset: 0; background: rgba(0,0,0,0.45);
      z-index: 999998; display: flex; align-items: center; justify-content: center;
    }
    #dh-sync-modal {
      background: #fff; border-radius: 12px; padding: 24px 28px;
      min-width: 380px; max-width: 480px; width: 90%;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    #dh-sync-modal h3 { margin: 0 0 16px; font-size: 16px; color: #111; }
    #dh-sync-modal label { display: block; font-size: 13px; color: #555; margin-bottom: 4px; }
    #dh-sync-modal input, #dh-sync-modal select {
      width: 100%; box-sizing: border-box; padding: 7px 10px;
      border: 1px solid #ddd; border-radius: 6px; font-size: 14px;
      margin-bottom: 12px; color: #111;
    }
    #dh-sync-modal .row { display: flex; gap: 10px; }
    #dh-sync-modal .row input { flex: 1; }
    .dh-btn-primary {
      background: #0066cc; color: #fff; border: none; border-radius: 6px;
      padding: 8px 20px; font-size: 14px; font-weight: 600; cursor: pointer; width: 100%;
    }
    .dh-btn-primary:hover { background: #0052a3; }
    .dh-btn-secondary {
      background: transparent; color: #555; border: 1px solid #ddd; border-radius: 6px;
      padding: 8px 16px; font-size: 14px; cursor: pointer;
	  align-self: center;
    }
    .dh-btn-secondary:hover { background: #f5f5f5; }
    .dh-modal-footer { display: flex; gap: 10px; margin-top: 4px; }
    .dh-status { font-size: 13px; margin-top: 8px; padding: 6px 10px; border-radius: 6px; }
    .dh-status.success { background: #e6f4ea; color: #1a7340; }
    .dh-status.error { background: #fce8e6; color: #c5221f; }
    .dh-status.loading { background: #e8f0fe; color: #1a56cc; }
    .dh-tag-list { max-height: 160px; overflow-y: auto; border: 1px solid #eee; border-radius: 6px; margin-bottom: 12px; }
    .dh-tag-item { padding: 6px 10px; font-size: 13px; cursor: pointer; display: flex; justify-content: space-between; }
    .dh-tag-item:hover { background: #f0f7ff; }
    .dh-tag-item.selected { background: #dbeafe; font-weight: 600; }
    .dh-config-link { font-size: 12px; color: #0066cc; cursor: pointer; text-align: right; display: block; margin-bottom: 12px; }
  `);

  // ========== 解析当前页面镜像信息 ==========
  function parseImageInfo() {
    const url = location.href;
    let registry = 'docker.io';
    let path = '';
    let name = '';

    const officialMatch = url.match(/hub\.docker\.com\/_\/([^/?#]+)/);
    const thirdPartyMatch = url.match(/hub\.docker\.com\/r\/([^/]+)\/([^/?#]+)/);

    if (officialMatch) {
      name = officialMatch[1];
      path = '';  // 官方镜像无 path
    } else if (thirdPartyMatch) {
      path = '/' + thirdPartyMatch[1];
      name = thirdPartyMatch[2];
    } else {
      return null;
    }

    return { registry, path, name };
  }

  // ========== 获取 Tags 列表（Docker Hub API） ==========
  function fetchTags(namespace, repoName, callback) {
    const apiUrl = namespace
      ? `https://hub.docker.com/v2/repositories/${namespace}/${repoName}/tags?page_size=20&ordering=last_updated`
      : `https://hub.docker.com/v2/repositories/library/${repoName}/tags?page_size=20&ordering=last_updated`;

    GM_xmlhttpRequest({
      method: 'GET',
      url: apiUrl,
      onload(res) {
        try {
          const data = JSON.parse(res.responseText);
          const tags = (data.results || []).map(t => t.name);
          callback(null, tags);
        } catch (e) {
          callback('解析 tags 失败');
        }
      },
      onerror() { callback('获取 tags 失败'); }
    });
  }

  // ========== 触发 GitHub Actions（通过 Cloudflare Worker 中转） ==========
  function triggerWorkflow(info, version, cfg, onResult) {
    const { registry, path: imagePath, name } = info;

    // 参数内容安全校验，防止注入
    const validPattern = /^[a-zA-Z0-9._\-/:]+$/;
    if (!validPattern.test(name) || !validPattern.test(version)) {
      onResult('镜像名或版本号包含非法字符');
      return;
    }

    GM_xmlhttpRequest({
      method: 'POST',
      url: cfg.workerUrl,
      headers: {
        'X-Secret': cfg.callSecret,
        'Content-Type': 'application/json',
      },
      data: JSON.stringify({
        registry,
        path: imagePath,
        imageName: name,
        imageVersion: version,
      }),
      onload(res) {
        if (res.status === 200) {
          onResult(null, `✅ 已触发同步: ${name}:${version}`);
        } else {
          let msg = `请求失败 (${res.status})`;
          try {
            const d = JSON.parse(res.responseText);
            msg = d.error || msg;
          } catch (_) {}
          onResult(msg);
        }
      },
      onerror() { onResult('网络请求失败，请检查 Worker URL 和网络'); }
    });
  }

  // ========== 配置弹窗 ==========
  function showConfigModal(afterSave) {
    const cfg = getConfig();
    const overlay = document.createElement('div');
    overlay.id = 'dh-sync-overlay';
    overlay.innerHTML = `
      <div id="dh-sync-modal">
        <h3>⚙️ 配置同步服务</h3>
        <label>Cloudflare Worker URL</label>
        <input id="cfg-worker-url" type="text" placeholder="https://docker-sync.xxx.workers.dev" value="${cfg.workerUrl}">
        <label>调用密钥（与 Worker 的 CALL_SECRET 一致）</label>
        <input id="cfg-call-secret" type="password" placeholder="your-call-secret" value="${cfg.callSecret}">
        <div class="dh-modal-footer">
          <button class="dh-btn-secondary" id="cfg-cancel">取消</button>
          <button class="dh-btn-primary" id="cfg-save" style="flex:1">保存</button>
        </div>
        <div id="cfg-status"></div>
      </div>
    `;
    document.body.appendChild(overlay);

    overlay.querySelector('#cfg-cancel').onclick = () => overlay.remove();
    overlay.querySelector('#cfg-save').onclick = () => {
      const newCfg = {
        workerUrl: overlay.querySelector('#cfg-worker-url').value.trim(),
        callSecret: overlay.querySelector('#cfg-call-secret').value.trim(),
      };
      if (!newCfg.workerUrl || !newCfg.callSecret) {
        overlay.querySelector('#cfg-status').innerHTML = '<div class="dh-status error">请填写所有必填项</div>';
        return;
      }
      saveConfig(newCfg);
      overlay.remove();
      if (afterSave) afterSave(newCfg);
    };
  }

  // ========== 同步弹窗 ==========
  function showSyncModal(info) {
    const cfg = getConfig();
    const overlay = document.createElement('div');
    overlay.id = 'dh-sync-overlay';

    const ns = info.path ? info.path.replace('/', '') : null;

    overlay.innerHTML = `
      <div id="dh-sync-modal">
        <h3>🚀 同步镜像到阿里云</h3>
        <a class="dh-config-link" id="open-cfg">修改配置 ⚙️</a>
        <div style="background:#f5f5f5;border-radius:6px;padding:8px 12px;margin-bottom:12px;font-size:13px;">
          <strong>镜像：</strong>${info.path || ''}/${info.name} &nbsp;&nbsp;
          <strong>Registry：</strong>${info.registry}
        </div>
        <label>选择 Tag（自动加载最近 20 个）</label>
        <div class="dh-tag-list" id="tag-list"><div style="padding:10px;color:#888;font-size:13px">加载中...</div></div>
        <label>或手动输入 Tag</label>
        <input id="manual-tag" placeholder="如 latest、1.0.0、v2.3-alpine" value="latest">
        <div class="dh-modal-footer">
          <button class="dh-btn-secondary" id="sync-cancel">取消</button>
          <button class="dh-btn-primary" id="sync-confirm">立即同步</button>
        </div>
        <div id="sync-status"></div>
      </div>
    `;
    document.body.appendChild(overlay);

    // 加载 tags
    fetchTags(ns, info.name, (err, tags) => {
      const list = overlay.querySelector('#tag-list');
      if (err || !tags.length) {
        list.innerHTML = `<div style="padding:10px;color:#888;font-size:13px">${err || '无 tags'}</div>`;
        return;
      }
      list.innerHTML = tags.map(t =>
        `<div class="dh-tag-item" data-tag="${t}"><span>${t}</span><span style="color:#aaa;font-size:12px">点击选择</span></div>`
      ).join('');
      list.querySelectorAll('.dh-tag-item').forEach(el => {
        el.onclick = () => {
          list.querySelectorAll('.dh-tag-item').forEach(e => e.classList.remove('selected'));
          el.classList.add('selected');
          overlay.querySelector('#manual-tag').value = el.dataset.tag;
        };
      });
    });

    overlay.querySelector('#sync-cancel').onclick = () => overlay.remove();
    overlay.querySelector('#open-cfg').onclick = () => {
      overlay.remove();
      showConfigModal(() => showSyncModal(info));
    };

    overlay.querySelector('#sync-confirm').onclick = () => {
      const version = overlay.querySelector('#manual-tag').value.trim();
      const statusEl = overlay.querySelector('#sync-status');
      if (!version) {
        statusEl.innerHTML = '<div class="dh-status error">请输入或选择 Tag</div>';
        return;
      }
      if (!cfg.workerUrl || !cfg.callSecret) {
        statusEl.innerHTML = '<div class="dh-status error">请先配置 Worker URL 和调用密钥</div>';
        return;
      }
      statusEl.innerHTML = '<div class="dh-status loading">⏳ 正在触发 GitHub Actions...</div>';
      overlay.querySelector('#sync-confirm').disabled = true;

      triggerWorkflow(info, version, cfg, (err, msg) => {
        if (err) {
          statusEl.innerHTML = `<div class="dh-status error">❌ ${err}</div>`;
          overlay.querySelector('#sync-confirm').disabled = false;
        } else {
          statusEl.innerHTML = `<div class="dh-status success">${msg}<br>
            <a href="https://github.com" target="_blank" style="color:#1a7340">前往 GitHub 查看运行状态 →</a>
          </div>`;
          setTimeout(() => overlay.remove(), 4000);
        }
      });
    };
  }

  // ========== 注入入口按钮 ==========
  function injectButton() {
    if (document.getElementById('dh-sync-btn')) return;
    const info = parseImageInfo();
    if (!info) return;

    const btn = document.createElement('button');
    btn.id = 'dh-sync-btn';
    btn.innerHTML = `<span>☁</span> 同步到阿里云`;
    btn.onclick = () => {
      const cfg = getConfig();
      if (!cfg.workerUrl || !cfg.callSecret) {
        showConfigModal((newCfg) => showSyncModal(info));
      } else {
        showSyncModal(info);
      }
    };
    document.body.appendChild(btn);
  }

  // Docker Hub 是 SPA，监听路由变化
  let lastUrl = location.href;
  const observer = new MutationObserver(() => {
    if (location.href !== lastUrl) {
      lastUrl = location.href;
      setTimeout(injectButton, 800);
    }
  });
  observer.observe(document.body, { childList: true, subtree: true });

  setTimeout(injectButton, 1000);

})();