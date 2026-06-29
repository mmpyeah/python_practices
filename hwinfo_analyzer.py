# -*- coding: utf-8 -*-
"""
HWiNFO64 CSV 日志分析脚本
用途：分析游戏中硬件数据，排查自动关机原因（电源/过热/功耗异常）
作者：Leo
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import rcParams
import os
import sys
import warnings

warnings.filterwarnings("ignore")

# ========== 配置区 ==========
# 修改为你的 CSV 文件路径
CSV_FILE = r"C:\Users\tianfeng\Desktop\hwinfo - 副本.CSV"

# 图表输出目录（自动创建）
OUTPUT_DIR = r"D:\PythonProjects\Project1\output"

# 电压异常阈值
V12_LOW_THRESHOLD = 11.4   # +12V 低于此值视为异常
V5_LOW_THRESHOLD  = 4.75   # +5V  低于此值视为异常
V33_LOW_THRESHOLD = 3.135  # +3.3V 低于此值视为异常

# 功耗异常阈值
CPU_POWER_HIGH = 200        # CPU 封装功率超过此值（W）标红
GPU_POWER_HIGH = 280        # GPU TGP 超过此值（W）标红
# ============================

# 支持中文显示
rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
rcParams['axes.unicode_minus'] = False


def load_csv(filepath):
    """读取 HWiNFO CSV，自动处理编码 + 列数对齐（不丢数据）"""
    from io import StringIO
    print(f"[*] 正在读取文件: {filepath}")

    # 先读入全部文本行
    encodings = ['utf-8-sig', 'utf-8', 'gbk', 'gb18030']
    lines = None
    for enc in encodings:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                lines = f.readlines()
            break
        except (UnicodeDecodeError, UnicodeError):
            continue

    if lines is None:
        # 强制解码
        with open(filepath, 'rb') as f:
            raw = f.read()
        if raw[:3] == b'\xef\xbb\xbf':
            raw = raw[3:]
        text = raw.decode('utf-8', errors='replace')
        lines = text.splitlines(keepends=True)
        print(f"[*] utf-8 强制解码（坏字节已替换）")

    # 列数对齐：以表头为准，截断/填充每行
    header_cols = lines[0].strip().split(',')
    n_cols = len(header_cols)
    cleaned = []
    skipped = 0
    for i, line in enumerate(lines):
        fields = line.rstrip('\r\n').split(',')
        if i == 0:
            cleaned.append(line.rstrip('\r\n'))
        elif len(fields) == n_cols:
            cleaned.append(line.rstrip('\r\n'))
        elif len(fields) > n_cols:
            # 截断多余列
            cleaned.append(','.join(fields[:n_cols]))
            skipped += 1
        else:
            # 列数不足，跳过（通常是末尾空行）
            skipped += 1
            continue

    if skipped > 0:
        print(f"[*] 对齐了 {skipped} 行列数不匹配的情况（保留所有数据）")

    text = '\n'.join(cleaned)
    df = pd.read_csv(StringIO(text), low_memory=False)

    if df.empty:
        print("[错误] 没有读取到任何有效数据行，请检查 CSV 文件格式")
        sys.exit(1)

    # 合并时间列
    df['Timestamp'] = pd.to_datetime(
        df['Date'].astype(str) + ' ' + df['Time'].astype(str),
        format='%d.%m.%Y %H:%M:%S.%f',
        errors='coerce'
    )
    df = df.dropna(subset=['Timestamp'])
    df = df.sort_values('Timestamp').reset_index(drop=True)

    print(f"[*] 共加载 {len(df)} 条记录，时间范围: {df['Timestamp'].iloc[0]} ~ {df['Timestamp'].iloc[-1]}")
    return df

def find_col(df, keyword):
    """模糊匹配列名（处理重复列名情况）"""
    matches = [c for c in df.columns if keyword in c]
    return matches[0] if matches else None


def to_numeric_series(df, col):
    """将列转换为数值，·否· 等无效值转为 NaN"""
    if col is None:
        return None
    return pd.to_numeric(df[col], errors='coerce')


def print_stats(name, series):
    """打印统计摘要"""
    if series is None or series.dropna().empty:
        print(f"  {name}: 数据不可用")
        return
    print(f"  {name}: 最小={series.min():.3f}  最大={series.max():.3f}  平均={series.mean():.3f}")


def detect_anomalies(df, col_12v, col_5v, col_33v, col_cpu_pwr, col_gpu_pwr):
    """检测异常时间点，打印报告"""
    print("\n" + "="*60)
    print("【异常检测报告】")
    print("="*60)

    anomalies_found = False

    checks = [
        (col_12v,    "+12V 低压异常",    V12_LOW_THRESHOLD,  "低于"),
        (col_5v,     "+5V 低压异常",     V5_LOW_THRESHOLD,   "低于"),
        (col_33v,    "+3.3V 低压异常",   V33_LOW_THRESHOLD,  "低于"),
        (col_cpu_pwr,"CPU 功耗高峰",     CPU_POWER_HIGH,     "高于"),
        (col_gpu_pwr,"GPU 功耗高峰",     GPU_POWER_HIGH,     "高于"),
    ]

    for col, label, threshold, direction in checks:
        if col is None:
            continue
        series = to_numeric_series(df, col)
        if series is None:
            continue
        if direction == "低于":
            mask = series < threshold
        else:
            mask = series > threshold

        anomaly_rows = df[mask]
        if not anomaly_rows.empty:
            anomalies_found = True
            print(f"\n[WARN]  {label}（{direction} {threshold}）共 {len(anomaly_rows)} 条：")
            for _, row in anomaly_rows.iterrows():
                print(f"    {row['Timestamp']}  →  {series[row.name]:.3f}")
        else:
            print(f"[OK]  {label}：未检测到异常")

    # 检查性能下降原因
    for keyword, label in [
        ("性能下降原因 - 功率", "GPU 功率降频"),
        ("性能下降原因 - 过热", "GPU 过热降频"),
        ("性能下降原因 - 电流", "GPU 电流降频"),
    ]:
        col = find_col(df, keyword)
        if col:
            yes_rows = df[df[col].astype(str).str.strip().str.lower() == 'yes']
            if not yes_rows.empty:
                anomalies_found = True
                print(f"\n[WARN]  {label} 触发 {len(yes_rows)} 次：")
                for _, row in yes_rows.iterrows():
                    print(f"    {row['Timestamp']}")
            else:
                print(f"[OK]  {label}：未触发")

    if not anomalies_found:
        print("\n[OK] 本次日志未检测到明显异常，建议在游戏实际崩溃时采集数据再分析。")

    print("="*60)


def plot_panel(df, panels, title, filename):
    """通用多子图绘制函数"""
    n = len(panels)
    fig, axes = plt.subplots(n, 1, figsize=(16, 4 * n), sharex=True)
    if n == 1:
        axes = [axes]

    fig.suptitle(title, fontsize=14, fontweight='bold')

    for ax, (label, col, color, threshold, threshold_label) in zip(axes, panels):
        series = to_numeric_series(df, col) if col else None
        if series is not None and not series.dropna().empty:
            ax.plot(df['Timestamp'], series, color=color, linewidth=1.2, label=label)
            if threshold is not None:
                ax.axhline(y=threshold, color='red', linestyle='--', linewidth=1,
                           label=f'警戒线 {threshold_label}')
            ax.legend(loc='upper right', fontsize=9)
            ax.set_ylabel(label, fontsize=9)
            ax.grid(True, alpha=0.3)
            # 标记异常点
            if threshold is not None:
                if '低于' in (threshold_label or ''):
                    mask = series < threshold
                else:
                    mask = series > threshold
                bad = df[mask]
                if not bad.empty:
                    ax.scatter(bad['Timestamp'], series[bad.index],
                               color='red', s=20, zorder=5, label='异常点')
        else:
            ax.text(0.5, 0.5, f'{label}\n（数据不可用）',
                    ha='center', va='center', transform=ax.transAxes, color='gray')
            ax.set_ylabel(label, fontsize=9)

    # 格式化 X 轴时间
    axes[-1].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    plt.xticks(rotation=30)
    plt.tight_layout()

    out_path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"[*] 图表已保存: {out_path}")


def main():
    # 检查文件
    csv_path = CSV_FILE
    if len(sys.argv) > 1:
        csv_path = sys.argv[1]

    if not os.path.exists(csv_path):
        print(f"[错误] 找不到文件: {csv_path}")
        print("用法: python hwinfo_analyzer.py [CSV文件路径]")
        print("  或修改脚本顶部 CSV_FILE 变量")
        sys.exit(1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 加载数据
    df = load_csv(csv_path)

    # 定位关键列
    col_12v      = find_col(df, '+12V [V]')
    col_5v       = find_col(df, '+5V [V]')
    col_33v      = find_col(df, '+3.3V [V]')
    col_cpu_pkg  = find_col(df, 'CPU 封装功率 [W]')
    col_cpu_ppt  = find_col(df, 'CPU PPT [W]')
    col_cpu_ppt_lim = find_col(df, 'CPU PPT Limit [%]')
    col_cpu_temp = find_col(df, 'CPU (Tctl/Tdie) [℃]')
    col_gpu_tgp  = find_col(df, 'Total Graphics Power (TGP) [W]')
    col_gpu_ppt  = find_col(df, 'GPU PPT [W]')
    col_gpu_temp = find_col(df, 'GPU 温度 [℃]')
    col_gpu_hot  = find_col(df, 'GPU 热点温度 [℃]')
    col_gpu_util = find_col(df, 'GPU 使用率 [%]')
    col_fps      = find_col(df, '帧率 [FPS]')

    # 打印统计摘要
    print("\n" + "="*60)
    print("【关键指标统计摘要】")
    print("="*60)
    print("--- 电源电压 ---")
    print_stats("+12V [V]",      to_numeric_series(df, col_12v))
    print_stats("+5V [V]",       to_numeric_series(df, col_5v))
    print_stats("+3.3V [V]",     to_numeric_series(df, col_33v))
    print("--- CPU ---")
    print_stats("CPU 封装功率 [W]",    to_numeric_series(df, col_cpu_pkg))
    print_stats("CPU PPT [W]",         to_numeric_series(df, col_cpu_ppt))
    print_stats("CPU PPT Limit [%]",   to_numeric_series(df, col_cpu_ppt_lim))
    print_stats("CPU 温度 [℃]",        to_numeric_series(df, col_cpu_temp))
    print("--- GPU ---")
    print_stats("GPU TGP [W]",         to_numeric_series(df, col_gpu_tgp))
    print_stats("GPU PPT [W]",         to_numeric_series(df, col_gpu_ppt))
    print_stats("GPU 温度 [℃]",        to_numeric_series(df, col_gpu_temp))
    print_stats("GPU 热点温度 [℃]",    to_numeric_series(df, col_gpu_hot))
    print_stats("GPU 使用率 [%]",      to_numeric_series(df, col_gpu_util))
    print_stats("帧率 [FPS]",          to_numeric_series(df, col_fps))

    # 异常检测
    detect_anomalies(df, col_12v, col_5v, col_33v, col_cpu_pkg, col_gpu_tgp)

    # ===== 图表 1：电源电压 =====
    plot_panel(df, [
        ("+12V [V]",  col_12v,  '#e74c3c', V12_LOW_THRESHOLD, "低于 11.4V"),
        ("+5V [V]",   col_5v,   '#e67e22', V5_LOW_THRESHOLD,  "低于 4.75V"),
        ("+3.3V [V]", col_33v,  '#f1c40f', V33_LOW_THRESHOLD, "低于 3.135V"),
    ], "电源电压监控（排查 PSU 问题）", "01_psu_voltage.png")

    # ===== 图表 2：CPU 功耗 & 温度 =====
    plot_panel(df, [
        ("CPU 封装功率 [W]",  col_cpu_pkg,     '#3498db', CPU_POWER_HIGH, "高于 200W"),
        ("CPU PPT [W]",       col_cpu_ppt,     '#2980b9', None,           None),
        ("CPU PPT Limit [%]", col_cpu_ppt_lim, '#1abc9c', 95,             "高于 95%"),
        ("CPU 温度 [℃]",      col_cpu_temp,    '#e74c3c', 90,             "高于 90℃"),
    ], "CPU 功耗 & 温度监控", "02_cpu_power_temp.png")

    # ===== 图表 3：GPU 功耗 & 温度 =====
    plot_panel(df, [
        ("GPU TGP [W]",      col_gpu_tgp,  '#9b59b6', GPU_POWER_HIGH, "高于 280W"),
        ("GPU PPT [W]",      col_gpu_ppt,  '#8e44ad', None,           None),
        ("GPU 温度 [℃]",     col_gpu_temp, '#e74c3c', 85,             "高于 85℃"),
        ("GPU 热点温度 [℃]", col_gpu_hot,  '#c0392b', 100,            "高于 100℃"),
    ], "GPU 功耗 & 温度监控", "03_gpu_power_temp.png")

    # ===== 图表 4：CPU+GPU 合计功耗 & 帧率 =====
    cpu_s = to_numeric_series(df, col_cpu_pkg)
    gpu_s = to_numeric_series(df, col_gpu_tgp)
    if cpu_s is not None and gpu_s is not None:
        df['_total_power'] = cpu_s.fillna(0) + gpu_s.fillna(0)
        col_total = '_total_power'
    else:
        col_total = None

    plot_panel(df, [
        ("CPU+GPU 合计功耗 [W]", col_total,  '#2c3e50', 580, "高于 580W（电源压力区间）"),
        ("帧率 [FPS]",           col_fps,    '#27ae60', None, None),
    ], "总功耗 & 帧率（关键：合计超 580W 时电源压力最大）", "04_total_power_fps.png")

    print(f"\n[完成] 所有图表已保存到: {OUTPUT_DIR}")
    print("[提示] 重点查看 01_psu_voltage.png，看 +12V 在高功耗时段是否出现压降")


if __name__ == '__main__':
    main()





