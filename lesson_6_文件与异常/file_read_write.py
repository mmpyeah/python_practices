# Lesson 6.1 - 文件操作基础
# ★★★ 核心概念，Python 运维脚本必须掌握的技能

"""
文件操作是 Python 运维自动化中最常用的功能之一。
本文档涵盖：
1. open() 函数及其各种模式
2. read()、readline()、readlines() 方法
3. write() 和 writelines() 方法
4. with 上下文管理器（推荐方式）
5. 文件指针和 seek()
6. 异常处理与文件安全
"""

# ===== 1. open() 函数基本用法 =====

"""
open(file, mode='r', encoding=None)

常用模式：
- 'r': 读取（默认）
- 'w': 写入（覆盖）
- 'a': 追加
- 'b': 二进制模式
- 'x': 独占创建
- '+': 读写模式
"""

# 读取文件
print("=== 1. 读取文件 ===")

# 检查文件是否存在
import os

filename = "test_file.txt"
if os.path.exists(filename):
    os.remove(filename)

# 创建测试文件
with open(filename, 'w', encoding='utf-8') as f:
    f.write("Hello World\n")
    f.write("Python 是一门伟大的语言\n")
    f.write("文件操作非常重要\n")

# 读取整个文件
with open(filename, 'r', encoding='utf-8') as f:
    content = f.read()
    print(f"读取整个文件: {content}")

# 读取一行
with open(filename, 'r', encoding='utf-8') as f:
    first_line = f.readline()
    print(f"第一行: {first_line.strip()}")
    second_line = f.readline()
    print(f"第二行: {second_line.strip()}")

# 读取所有行
with open(filename, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    print(f"所有行: {lines}")

# 逐行读取
with open(filename, 'r', encoding='utf-8') as f:
    for line in f:
        print(f"  逐行: {line.strip()}")

# ===== 2. write() 和 writelines() =====

print("\n=== 2. 写入文件 ===")

# 写入模式 'w'（会覆盖）
with open(filename, 'w', encoding='utf-8') as f:
    f.write("第一行内容\n")
    f.write("第二行内容\n")
    f.writelines(["第三行\n", "第四行\n", "第五行\n"])

# 读取验证
with open(filename, 'r', encoding='utf-8') as f:
    content = f.read()
    print(f"写入后的内容:\n{content}")

# 追加模式 'a'（不会覆盖）
with open(filename, 'a', encoding='utf-8') as f:
    f.write("\n第六行（追加）\n")

# 读取验证
with open(filename, 'r', encoding='utf-8') as f:
    content = f.read()
    print(f"追加后的内容:\n{content}")

# ===== 3. 上下文管理器 with =====

"""
with 语句自动处理文件的打开和关闭
即使发生异常也能保证文件正确关闭
这是 Python 中推荐的文件操作方式
"""

print("\n=== 3. 上下文管理器 with ===")

def read_file_safely(filename):
    """安全的文件读取方式"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            return content
    except FileNotFoundError:
        print(f"文件 {filename} 不存在")
        return None
    except Exception as e:
        print(f"读取文件出错: {e}")
        return None

# 测试不存在的文件
result = read_file_safely("nonexistent.txt")
print(f"读取不存在的文件: {result}")

# ===== 4. 文件指针和 seek() =====

"""
seek(offset, whence)
whence 参数：
- 0: 从文件开头（默认）
- 1: 从当前位置
- 2: 从文件末尾
"""

print("\n=== 4. 文件指针和 seek() ===")

with open(filename, 'r', encoding='utf-8') as f:
    print(f"初始位置: {f.tell()}")

    # 读取前 20 个字符
    chunk = f.read(20)
    print(f"前 20 个字符: {chunk}")

    # 跳到文件末尾
    f.seek(0, 2)
    print(f"跳到末尾后的位置: {f.tell()}")

    # 从文件末尾读取 10 个字符
    content = f.read(10)
    print(f"末尾 10 个字符: {content}")

    # 回到开头
    f.seek(0)
    print(f"回到开头后的位置: {f.tell()}")

# ===== 5. 文件模式总结 =====

print("\n=== 5. 文件模式总结 ===")

modes = {
    'r': '只读',
    'w': '写入（覆盖）',
    'a': '追加',
    'x': '独占创建',
    'r+': '读写',
    'w+': '读写（覆盖）',
    'a+': '读写（追加）',
    'rb': '二进制只读',
    'wb': '二进制写入',
}

for mode, desc in modes.items():
    print(f"  '{mode}': {desc}")

# ===== 6. 文件编码 =====

"""
默认使用系统编码，但建议显式指定
UTF-8 是最常用的编码
"""

print("\n=== 6. 文件编码 ===")

with open(filename, 'w', encoding='utf-8') as f:
    f.write("中文测试\n")
    f.write("Unicode 字符\n")

with open(filename, 'r', encoding='utf-8') as f:
    content = f.read()
    print(f"UTF-8 编码内容: {content}")

# GBK 编码测试
filename_gbk = "test_gbk.txt"
with open(filename_gbk, 'w', encoding='gbk') as f:
    f.write("中文 GBK 测试\n")

with open(filename_gbk, 'r', encoding='gbk') as f:
    content = f.read()
    print(f"GBK 编码内容: {content}")

# 自动检测编码
try:
    import chardet

    with open(filename_gbk, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        print(f"自动检测编码: {result}")
except ImportError:
    print("chardet 模块未安装，跳过自动检测")

# ===== 7. 实战应用 =====

def process_log_file(log_file, keyword, output_file):
    """
    处理日志文件：提取包含关键字的行
    """
    try:
        with open(log_file, 'r', encoding='utf-8') as f_in:
            with open(output_file, 'w', encoding='utf-8') as f_out:
                for line in f_in:
                    if keyword.lower() in line.lower():
                        f_out.write(line)
                print(f"提取完成，共提取 {output_file}")
    except FileNotFoundError:
        print(f"日志文件 {log_file} 不存在")
    except Exception as e:
        print(f"处理日志时出错: {e}")


def backup_file(source, backup_dir):
    """
    备份文件：复制文件到备份目录
    """
    try:
        import shutil

        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        backup_name = f"{os.path.basename(source)}_{timestamp}"
        backup_path = os.path.join(backup_dir, backup_name)

        shutil.copy2(source, backup_path)
        print(f"备份完成: {backup_path}")
        return backup_path
    except Exception as e:
        print(f"备份失败: {e}")
        return None


def count_words(filename):
    """
    统计文件中的单词数
    """
    try:
        word_count = 0
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                words = line.split()
                word_count += len(words)
        return word_count
    except FileNotFoundError:
        print(f"文件 {filename} 不存在")
        return 0
    except Exception as e:
        print(f"统计单词时出错: {e}")
        return 0


# ===== 8. 文件操作最佳实践 =====

"""
1. 始终使用 with 语句
2. 显式指定编码（utf-8）
3. 使用异常处理
4. 大文件逐行读取，不要一次性读取
5. 及时关闭文件
"""

def read_large_file(filename):
    """读取大文件（逐行处理）"""
    with open(filename, 'r', encoding='utf-8') as f:
        for line_number, line in enumerate(f, 1):
            # 处理每一行
            process_line(line_number, line)
            # 每处理 1000 行，暂停一下
            if line_number % 1000 == 0:
                time.sleep(0.001)


def process_line(line_number, line):
    """处理单行"""
    # 这里可以实现任何处理逻辑
    pass


# ===== 9. 文件读写性能对比 =====

"""
小文件：可以一次性读取
大文件：必须逐行读取，否则内存溢出
"""

def compare_read_methods(size=1000000):
    """比较不同读取方式的内存占用"""
    import sys

    # 方法1：一次性读取（大文件时危险）
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
        size_1 = sys.getsizeof(content)

    # 方法2：逐行读取
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        size_2 = sum(sys.getsizeof(line) for line in lines)

    # 方法3：迭代器逐行
    with open(filename, 'r', encoding='utf-8') as f:
        for _ in f:
            pass
        size_3 = sys.getsizeof(f)

    print(f"一次性读取内存: {size_1 / 1024:.2f} KB")
    print(f"readlines() 内存: {size_2 / 1024 / 1024:.2f} MB")
    print(f"迭代器内存: {size_3:.2f} 字节")

# ===== 测试代码 =====

print("\n=== 7. 实战应用测试 ===")

# 测试日志文件处理
os.makedirs("logs", exist_ok=True)
process_log_file("test_file.txt", "Python", "filtered.txt")
if os.path.exists("filtered.txt"):
    with open("filtered.txt", 'r', encoding='utf-8') as f:
        print(f"过滤后的内容:\n{f.read()}")

# 测试单词统计
word_count = count_words(filename)
print(f"文件 {filename} 的单词数: {word_count}")

# 测试文件备份
if os.path.exists(filename):
    backup_path = backup_file(filename, "backups")
    if backup_path:
        # 验证备份文件
        with open(backup_path, 'r', encoding='utf-8') as f:
            backup_content = f.read()
        print(f"备份文件内容验证: {'内容一致' if backup_content == content else '内容不一致'}")

# 清理测试文件
for f in [filename, filename_gbk, "filtered.txt"]:
    if os.path.exists(f):
        os.remove(f)
if os.path.exists("logs"):
    shutil.rmtree("logs")
if os.path.exists("backups"):
    shutil.rmtree("backups")
