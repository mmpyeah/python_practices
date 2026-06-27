"""
解析 tarab_all_gift_give_running_water.json
支持两种格式：
  1. JSON 数组  [ {...}, {...} ]
  2. JSONL 每行一个对象
"""

import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# ── 配置 ──────────────────────────────────────────────────────────────────────
# FILE_PATH = r"D:\PythonProjects\Project1\tarab_all_gift_give_running_water.json"
FILE_PATH = r"C:\Users\tianfeng\Documents\DataGrip\tarab_all_gift_give_running_water2.json"
# ─────────────────────────────────────────────────────────────────────────────


def parse_date(val) -> datetime | None:
    """兼容 {"$date": "..."} 和普通字符串"""
    if val is None:
        return None
    if isinstance(val, dict) and "$date" in val:
        val = val["$date"]
    try:
        return datetime.fromisoformat(val.replace("Z", "+00:00"))
    except Exception:
        return None


def parse_decimal(val) -> float | None:
    if val is None:
        return None
    if isinstance(val, dict) and "$numberDecimal" in val:
        return float(val["$numberDecimal"])
    try:
        return float(val)
    except Exception:
        return None


def _parse_java_tostring(s: str) -> list[dict]:
    """
    解析 Java List.toString() 格式：[{key=value, key2=value2}, ...]
    value 可以是：数字、true/false、带连字符/点/中文的字符串
    """
    results = []
    for block in re.finditer(r'\{([^}]*)\}', s):
        content = block.group(1)
        obj = {}
        # 按 ", word=" 切割，避免 value 里的逗号误切
        tokens = re.split(r',\s*(?=[\w]+\s*=)', content)
        for token in tokens:
            eq = token.find('=')
            if eq == -1:
                continue
            key = token[:eq].strip()
            val = token[eq + 1:].strip()
            if val == 'true':
                obj[key] = True
            elif val == 'false':
                obj[key] = False
            elif val == 'null':
                obj[key] = None
            else:
                try:
                    obj[key] = int(val)
                except ValueError:
                    try:
                        obj[key] = float(val)
                    except ValueError:
                        obj[key] = val
        if obj:
            results.append(obj)
    return results


def parse_accept_users(raw) -> list[dict]:
    """acceptUsers：真正的 list 或 Java toString() 字符串"""
    if isinstance(raw, list):
        return raw
    if not isinstance(raw, str):
        return []
    return _parse_java_tostring(raw)


def parse_gift_value(raw) -> dict:
    """giftValue：真正的 dict 或 Java toString() 字符串"""
    if isinstance(raw, dict):
        return raw
    if not isinstance(raw, str):
        return {}
    parsed = _parse_java_tostring(raw)
    return parsed[0] if parsed else {}


def load_records(path: str) -> list[dict]:
    text = Path(path).read_text(encoding="utf-8")
    text = text.strip()

    # 尝试 JSON 数组
    if text.startswith("["):
        return json.loads(text)

    # 尝试 JSONL
    records = []
    for line in text.splitlines():
        line = line.strip().rstrip(",")
        if line:
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return records


def analyze(records: list[dict]):
    print(f"\n{'='*60}")
    print(f"  总记录数: {len(records)}")
    print(f"{'='*60}")

    # ── 基础统计 ─────────────────────────────────────────────
    lucky_count   = sum(1 for r in records if r.get("luckyGift"))
    processed_cnt = sum(1 for r in records if r.get("processed"))
    refunded_cnt  = sum(1 for r in records if r.get("refunded"))
    platforms     = defaultdict(int)
    gift_types    = defaultdict(int)

    for r in records:
        platforms[r.get("requestPlatform", "unknown")] += 1
        gift_types[r.get("giftType", "unknown")] += 1

    print(f"\n[基础]")
    print(f"  luckyGift=true  : {lucky_count}")
    print(f"  processed=true  : {processed_cnt}")
    print(f"  refunded=true   : {refunded_cnt}")
    print(f"  平台分布        : {dict(platforms)}")
    print(f"  礼物类型分布    : {dict(gift_types)}")

    # ── 每分钟送礼次数（定位 CPU 高峰） ─────────────────────
    minute_count: dict[str, int] = defaultdict(int)
    user_send: dict[str, int] = defaultdict(int)
    total_amount = 0.0

    for r in records:
        ct = parse_date(r.get("createTime"))
        if ct:
            minute_key = ct.strftime("%Y-%m-%d %H:%M")
            minute_count[minute_key] += 1

        uid = str(r.get("userId", ""))
        if uid:
            user_send[uid] += 1

        gv = parse_gift_value(r.get("giftValue", {}))
        amt = gv.get("actualAmount") or gv.get("giftValue")
        if amt:
            try:
                total_amount += float(str(amt))
            except Exception:
                pass

    print(f"\n[金额]")
    print(f"  总礼物价值 (gold): {total_amount:,.2f}")

    print(f"\n[每分钟送礼 TOP 20]")
    top_minutes = sorted(minute_count.items(), key=lambda x: -x[1])[:20]
    for ts, cnt in top_minutes:
        print(f"  {ts}  -> {cnt} 次")

    print(f"\n[送礼最多用户 TOP 20]")
    top_users = sorted(user_send.items(), key=lambda x: -x[1])[:20]
    for uid, cnt in top_users:
        print(f"  userId={uid}  -> {cnt} 次")

    # ── acceptUsers 统计（收礼人数分布） ─────────────────────
    accept_size_dist: dict[int, int] = defaultdict(int)
    for r in records:
        au = parse_accept_users(r.get("acceptUsers", []))
        accept_size_dist[len(au)] += 1

    # 记录 1 人收礼的 userId
    single_accept_users: list[str] = []
    for r in records:
        au = parse_accept_users(r.get("acceptUsers", []))
        if len(au) == 1:
            single_accept_users.append(str(r.get("userId", "")))

    print(f"\n[acceptUsers 人数分布]")
    for size, cnt in sorted(accept_size_dist.items()):
        print(f"  {size} 人收礼: {cnt} 次")

    if single_accept_users:
        print(f"\n[1 人收礼的送礼 userId（共 {len(single_accept_users)} 条）]")
        # 统计每个 userId 出现次数并排序
        uid_cnt: dict[str, int] = defaultdict(int)
        for uid in single_accept_users:
            uid_cnt[uid] += 1
        for uid, cnt in sorted(uid_cnt.items(), key=lambda x: -x[1]):
            print(f"  userId={uid}  -> {cnt} 次")

    # ── 时段分布（按小时，UTC） ──────────────────────────────
    hour_dist: dict[int, int] = defaultdict(int)
    for r in records:
        ct = parse_date(r.get("createTime"))
        if ct:
            hour_dist[ct.hour] += 1

    print(f"\n[每小时送礼分布 (UTC)]")
    for h in sorted(hour_dist):
        bar = "█" * (hour_dist[h] * 40 // max(hour_dist.values()))
        print(f"  {h:02d}:xx  {hour_dist[h]:5d}  {bar}")


if __name__ == "__main__":
    print(f"正在读取: {FILE_PATH}")
    records = load_records(FILE_PATH)
    analyze(records)
