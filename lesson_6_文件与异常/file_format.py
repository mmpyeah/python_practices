# Lesson 6.3 - 文件格式处理
# ★★★ 核心概念，Python 运维中处理各种格式的文件

"""
文件格式处理是运维自动化的核心技能。
本文档涵盖：
1. JSON 读写
2. CSV 读写
3. INI 配置文件处理（configparser）
4. Excel 处理（openpyxl 简介）
"""

# ===== 1. JSON 文件处理 =====

"""
JSON (JavaScript Object Notation) 是一种轻量级的数据交换格式
Python 的 json 模块提供完整的 JSON 支持
"""

import json
from pathlib import Path

# ===== 1.1 JSON 基本读写 =====

print("=== 1. JSON 读写 ===")

# 创建测试 JSON 文件
data = {
    "name": "张三",
    "age": 30,
    "city": "北京",
    "hobbies": ["编程", "阅读", "旅行"],
    "address": {
        "street": "长安街",
        "number": 123
    }
}

json_file = "data.json"

# 写入 JSON
with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"JSON 文件已创建: {json_file}")

# 读取 JSON
with open(json_file, 'r', encoding='utf-8') as f:
    loaded_data = json.load(f)

print(f"读取的数据: {loaded_data}")
print(f"name: {loaded_data['name']}")
print(f"age: {loaded_data['age']}")
print(f"hobbies: {loaded_data['hobbies']}")

# ===== 1.2 JSON 格式化输出 =====

print("\n=== 2. JSON 格式化输出 ===")

# 格式化输出（pretty print）
formatted_json = json.dumps(data, ensure_ascii=False, indent=4)
print(f"格式化 JSON:\n{formatted_json}")

# 不缩进输出
compact_json = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
print(f"紧凑 JSON: {compact_json}")

# 单行输出
short_json = json.dumps(data, ensure_ascii=False)
print(f"短格式 JSON: {short_json}")

# ===== 1.3 JSON 特殊数据类型 =====

"""
JSON 支持的基本类型：
- object: dict
- array: list
- string: str
- number: int/float
- boolean: True/False
- null: None
"""

print("\n=== 3. JSON 特殊数据类型 ===")

mixed_data = {
    "name": "张三",
    "age": 25,
    "active": True,
    "scores": [90, 85, 92],
    "married": False,
    "address": None,
    "metadata": {
        "created": "2024-01-01",
        "version": 1.0
    }
}

json_file_mixed = "mixed_data.json"
with open(json_file_mixed, 'w', encoding='utf-8') as f:
    json.dump(mixed_data, f, ensure_ascii=False, indent=2)

print(f"混合类型数据已写入: {json_file_mixed}")

# ===== 1.4 JSON 文件遍历 =====

def process_json_file(filename, processor):
    """
    处理 JSON 文件
    :param filename: JSON 文件名
    :param processor: 处理函数
    :return: 处理结果列表
    """
    results = []

    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

        if isinstance(data, list):
            # 如果是列表，遍历每个元素
            for item in data:
                result = processor(item)
                if result is not None:
                    results.append(result)
        elif isinstance(data, dict):
            # 如果是字典，遍历每个值
            for key, value in data.items():
                result = processor({key: value})
                if result is not None:
                    results.append(result)

    return results


def find_person_by_age(data):
    """查找指定年龄的人"""
    if isinstance(data, dict) and 'age' in data:
        if data['age'] == 25:
            return f"找到年龄为 {data['age']} 的人: {data.get('name', '未知')}"
    return None


# ===== 1.5 JSON 批量操作 =====

def write_json_batch(filename, batch_data, batch_size=1000):
    """
    批量写入 JSON 文件
    :param filename: 文件名
    :param batch_data: 数据列表
    :param batch_size: 每批写入的数量
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(batch_data, f, ensure_ascii=False, indent=2)
    print(f"已写入 {len(batch_data)} 条数据到 {filename}")


def read_json_lines(filename):
    """
    逐行读取 JSON Lines 格式（每行一个 JSON 对象）
    适用于大文件处理
    """
    results = []

    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                results.append(data)
            except json.JSONDecodeError as e:
                print(f"JSON 解析错误: {e}")

    return results


# ===== 2. CSV 文件处理 =====

"""
CSV (Comma-Separated Values) 是最常用的表格数据格式
Python 的 csv 模块提供完整的 CSV 支持
"""

import csv
from io import StringIO

# ===== 2.1 CSV 基本读写 =====

print("\n=== 4. CSV 基本读写 ===")

# 写入 CSV
csv_file = "data.csv"
data = [
    ["姓名", "年龄", "城市", "职业"],
    ["张三", "25", "北京", "工程师"],
    ["李四", "30", "上海", "设计师"],
    ["王五", "28", "广州", "产品经理"]
]

with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerows(data)

print(f"CSV 文件已创建: {csv_file}")

# 读取 CSV
with open(csv_file, 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    rows = list(reader)

    print(f"读取到 {len(rows)} 行数据:")
    for row in rows:
        print(f"  {row}")

# ===== 2.2 DictReader - 按列名读取 =====

print("\n=== 5. DictReader 按列名读取 ===")

with open(csv_file, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)

    print(f"列名: {reader.fieldnames}")
    print(f"共 {reader.line_num} 行数据")

    for row in reader:
        print(f"  {row}")

# ===== 2.3 DictWriter - 按列名写入 =====

print("\n=== 6. DictWriter 按列名写入 ===")

new_data = [
    {"姓名": "赵六", "年龄": "35", "城市": "深圳", "职业": "技术总监"},
    {"姓名": "钱七", "年龄": "32", "城市": "成都", "职业": "CTO"}  # city 不在列名中
]

fieldnames = ["姓名", "年龄", "城市", "职业"]
new_csv_file = "new_data.csv"

with open(new_csv_file, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()  # 写入列名
    writer.writerows(new_data)

print(f"已写入 {len(new_data)} 行到 {new_csv_file}")

# ===== 2.4 CSV 批量处理 =====

def filter_csv_by_age(input_file, output_file, min_age):
    """
    过滤 CSV 文件中的年龄数据
    """
    with open(input_file, 'r', encoding='utf-8-sig') as f_in:
        reader = csv.DictReader(f_in)
        fieldnames = reader.fieldnames

        with open(output_file, 'w', newline='', encoding='utf-8-sig') as f_out:
            writer = csv.DictWriter(f_out, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                try:
                    age = int(row['年龄'])
                    if age >= min_age:
                        writer.writerow(row)
                except (ValueError, KeyError):
                    continue

    print(f"已过滤，生成 {output_file}")


def aggregate_csv(input_file, output_file, group_field):
    """
    按字段聚合数据
    """
    from collections import defaultdict

    with open(input_file, 'r', encoding='utf-8-sig') as f_in:
        reader = csv.DictReader(f_in)

        # 按分组字段聚合
        groups = defaultdict(list)
        for row in reader:
            groups[row[group_field]].append(row)

        # 写入聚合结果
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as f_out:
            writer = csv.DictWriter(f_out, fieldnames=reader.fieldnames)
            writer.writeheader()

            for group_name, items in groups.items():
                # 计算平均值
                avg_age = sum(int(item['年龄']) for item in items) / len(items)
                result_row = items[0].copy()
                result_row['平均年龄'] = f"{avg_age:.1f}"
                writer.writerow(result_row)


# ===== 3. INI 配置文件处理 =====

"""
INI (Initialization) 格式常用于配置文件
Python 的 configparser 模块提供支持
"""

import configparser

# ===== 3.1 INI 基本读写 =====

print("\n=== 7. INI 配置文件处理 ===")

# 写入 INI 文件
config = configparser.ConfigParser()
config['database'] = {
    'host': 'localhost',
    'port': '5432',
    'database': 'mydb',
    'username': 'admin',
    'password': 'secret123'
}

config['logging'] = {
    'level': 'INFO',
    'file': 'app.log',
    'max_size': '10MB'
}

config['cache'] = {
    'enabled': 'True',
    'ttl': '3600'
}

ini_file = "config.ini"
with open(ini_file, 'w', encoding='utf-8') as f:
    config.write(f)

print(f"INI 文件已创建: {ini_file}")

# 读取 INI 文件
config = configparser.ConfigParser()
config.read(ini_file, encoding='utf-8')

print(f"数据库配置:")
print(f"  host: {config.get('database', 'host')}")
print(f"  port: {config.get('database', 'port')}")
print(f"  database: {config.get('database', 'database')}")

print(f"\n日志配置:")
print(f"  level: {config.get('logging', 'level')}")
print(f"  file: {config.get('logging', 'file')}")

# 获取所有章节
print(f"\n所有章节: {config.sections()}")

# 检查章节是否存在
if config.has_section('cache'):
    print(f"\n缓存配置:")
    for key, value in config.items('cache'):
        print(f"  {key}: {value}")

# 获取布尔值
cache_enabled = config.getboolean('cache', 'enabled')
print(f"\n缓存已启用: {cache_enabled}")

# 获取整数
cache_ttl = config.getint('cache', 'ttl')
print(f"缓存 TTL: {cache_ttl} 秒")

# ===== 3.2 INI 高级操作 =====

def update_config_file(filename, section, option, value):
    """
    更新配置文件中的值
    """
    config = configparser.ConfigParser()
    config.read(filename, encoding='utf-8')

    if not config.has_section(section):
        config.add_section(section)

    config.set(section, option, str(value))

    with open(filename, 'w', encoding='utf-8') as f:
        config.write(f)

    print(f"已更新 {filename} [{section}] {option} = {value}")


def backup_config_file(filename):
    """
    备份配置文件
    """
    import shutil
    import time

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    backup_name = f"{filename}.bak.{timestamp}"
    shutil.copy2(filename, backup_name)
    print(f"已备份配置文件: {backup_name}")

    return backup_name


# ===== 4. 实战应用 =====

def create_config_template():
    """
    创建配置模板文件
    """
    config = configparser.ConfigParser()

    # 数据库配置
    config['database'] = {
        'host': 'localhost',
        'port': '5432',
        'database': 'your_database',
        'username': 'your_username',
        'password': 'your_password'
    }

    # 日志配置
    config['logging'] = {
        'level': 'INFO',
        'file': 'app.log',
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    }

    # 应用配置
    config['app'] = {
        'name': 'My Application',
        'version': '1.0.0',
        'debug': 'True',
        'workers': '4'
    }

    return config


def load_config_with_fallback(primary_file, fallback_file):
    """
    加载配置文件，如果没有则创建
    """
    config = configparser.ConfigParser()

    if os.path.exists(primary_file):
        config.read(primary_file, encoding='utf-8')
        print(f"已加载配置文件: {primary_file}")
    else:
        # 如果文件不存在，创建默认配置
        config = create_config_template()
        with open(primary_file, 'w', encoding='utf-8') as f:
            config.write(f)
        print(f"已创建默认配置文件: {primary_file}")

    return config


def export_data_to_json(data, filename):
    """
    导出数据到 JSON 文件
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"已导出 {len(data)} 条数据到 {filename}")


def export_data_to_csv(data, filename, fieldnames=None):
    """
    导出数据到 CSV 文件
    """
    if not fieldnames and data:
        fieldnames = list(data[0].keys())

    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(f"已导出 {len(data)} 条数据到 {filename}")


# ===== 测试代码 =====

print("\n=== 8. 实战应用测试 ===")

# 测试 CSV 过滤
filter_csv_by_age("data.csv", "filtered_data.csv", 28)
print("\n过滤后的 CSV:")
with open("filtered_data.csv", 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    for row in reader:
        print(f"  {row}")

# 测试 CSV 聚合
aggregate_csv("data.csv", "aggregated_data.csv", "城市")
print("\n聚合后的 CSV:")
with open("aggregated_data.csv", 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"  {row}")

# 测试 INI 更新
update_config_file(ini_file, 'database', 'port', '5433')
config = configparser.ConfigParser()
config.read(ini_file)
print(f"\n更新后的数据库端口: {config.get('database', 'port')}")

# 测试备份
backup_config_file(ini_file)

# 测试数据导出
test_data = [
    {"id": 1, "name": "项目A", "status": "进行中"},
    {"id": 2, "name": "项目B", "status": "已完成"},
    {"id": 3, "name": "项目C", "status": "待开始"}
]
export_data_to_json(test_data, "projects.json")
export_data_to_csv(test_data, "projects.csv")

# 清理测试文件
for f in ["data.json", "mixed_data.json", "data.csv", "new_data.csv",
          "config.ini", "filtered_data.csv", "aggregated_data.csv",
          "projects.json", "projects.csv"]:
    if os.path.exists(f):
        os.remove(f)
