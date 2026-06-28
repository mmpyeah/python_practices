# Lesson 6.2 - 文件路径操作
# ★★★ 核心概念，Python 运维脚本中必不可少

"""
文件路径操作是 Python 运维自动化的重要基础。
本文档涵盖：
1. pathlib.Path - 现代路径操作方式
2. os.path - 传统路径操作方式
3. 路径拼接和分解
4. 文件和目录遍历
5. glob 通配符匹配
6. 目录树操作
"""

# ===== 1. pathlib.Path 基本用法 =====

"""
pathlib 是 Python 3.4+ 推荐的路径操作方式
比 os.path 更简洁、更现代
"""

from pathlib import Path
import os

# ===== 1.1 创建路径对象 =====

# 绝对路径
abs_path = Path("/home/user/documents")
print(f"绝对路径: {abs_path}")

# 相对路径
rel_path = Path("documents/work")

# ===== 1.2 路径拼接 =====

"""
使用 / 操作符拼接路径
"""

path1 = Path("home") / "user" / "documents"
path2 = Path("home") / Path("user") / "documents"
path3 = Path("home") / "user" / "documents" / "file.txt"

print(f"路径拼接: {path3}")

# 路径分解
print(f"父目录: {path3.parent}")
print(f"文件名: {path3.name}")
print(f"文件名（不含扩展名）: {path3.stem}")
print(f"扩展名: {path3.suffix}")
print(f"所有扩展名: {path3.suffixes}")

# ===== 1.3 路径存在性检查 =====

print("\n=== 路径存在性检查 ===")

test_path = Path("test_file.txt")
print(f"测试文件是否存在: {test_path.exists()}")

if not test_path.exists():
    test_path.write_text("测试内容")

print(f"测试文件存在: {test_path.exists()}")

# 判断是否是目录
print(f"测试文件是目录: {test_path.is_dir()}")

# 判断是否是文件
print(f"测试文件是文件: {test_path.is_file()}")

# ===== 1.4 路径遍历 =====

"""
Path.iterdir() - 列出目录下的内容
Path.glob() - 使用通配符匹配
Path.rglob() - 递归匹配
"""

print("\n=== 路径遍历 ===")

# 列出目录内容
if os.path.exists("test_dir"):
    for item in Path("test_dir").iterdir():
        print(f"  {item.name} ({'目录' if item.is_dir() else '文件'})")

# glob 通配符匹配
print("\n  .glob() 模式匹配:")
for p in Path("test_dir").glob("*.txt"):
    print(f"    {p}")

for p in Path("test_dir").glob("**/*.txt"):
    print(f"    {p}")

# 递归 glob
print("\n  .rglob() 递归匹配:")
for p in Path("test_dir").rglob("*.txt"):
    print(f"    {p}")

# ===== 2. os.path 传统方式 =====

"""
os.path 仍然是 Python 2.7 和某些库的兼容方式
"""

import os as traditional_os

# 路径拼接
full_path = traditional_os.path.join("home", "user", "documents", "file.txt")
print(f"os.path.join: {full_path}")

# 路径分解
print(f"dirname: {traditional_os.path.dirname(full_path)}")
print(f"basename: {traditional_os.path.basename(full_path)}")
print(f"splitext: {traditional_os.path.splitext(full_path)}")

# 路径存在性
print(f"exists: {traditional_os.path.exists(full_path)}")
print(f"isdir: {traditional_os.path.isdir(full_path)}")
print(f"isfile: {traditional_os.path.isfile(full_path)}")

# 获取文件大小
if traditional_os.path.isfile(full_path):
    size = traditional_os.path.getsize(full_path)
    print(f"file size: {size} bytes")

# 只有文件存在时才获取修改时间
if traditional_os.path.exists(full_path):
    mtime = traditional_os.path.getmtime(full_path)
    print(f"modified time: {mtime}")

# 文件大小和修改时间

size = p.stat().st_size
mtime = p.stat().st_mtime
print(f"文件大小: {size} bytes")
print(f"修改时间: {mtime}")

# 格式化时间
from datetime import datetime
print(f"修改时间 (格式化): {datetime.fromtimestamp(mtime)}")

# ===== 3. glob 通配符匹配 =====

"""
glob 是查找文件的神器
支持 * ? [ ] 等 通配符
"""

import glob

print("\n=== glob 通配符匹配 ===")

# 匹配当前目录的所有 .txt 文件
print("  *.txt:")
for p in glob.glob("*.txt"):
    print(f"    {p}")

# 匹配所有子目录中的 .py 文件
print("  **/*.py:")
for p in glob.glob("**/*.py", recursive=True):
    print(f"    {p}")

# 匹配以 test 开头的文件
print("  test*:")
for p in glob.glob("test*"):
    print(f"    {p}")

# 匹配文件名中包含 "test" 的所有文件
print("  *test*:")
for p in glob.glob("*test*"):
    print(f"    {p}")

# ===== 4. 目录操作 =====

"""
创建、删除、遍历目录
"""

print("\n=== 目录操作 ===")

# 创建目录
new_dir = Path("new_directory")
if not new_dir.exists():
    new_dir.mkdir()
    print(f"创建目录: {new_dir}")

# 创建多级目录
multi_dir = Path("level1") / "level2" / "level3"
multi_dir.mkdir(parents=True, exist_ok=True)
print(f"创建多级目录: {multi_dir}")

# 创建目录时带模式
multi_dir.mkdir(mode=0o755, exist_ok=True)

# 遍历目录树
print("\n  遍历目录树:")
def walk_directory(path, depth=0):
    """递归遍历目录"""
    indent = "  " * depth
    for item in sorted(path.iterdir()):
        if item.is_file():
            print(f"{indent}📄 {item.name}")
        elif item.is_dir():
            print(f"{indent}📁 {item.name}")
            walk_directory(item, depth + 1)

if new_dir.exists():
    walk_directory(new_dir)

# 获取目录内容
print("\n  目录内容:")
for item in new_dir.iterdir():
    print(f"    {item.name} ({'目录' if item.is_dir() else '文件'})")

# 获取所有子目录
print("\n  所有子目录:")
for d in new_dir.iterdir():
    if d.is_dir():
        print(f"    {d.name}")

# 获取所有文件
print("\n  所有文件:")
for f in new_dir.iterdir():
    if f.is_file():
        print(f"    {f.name}")

# ===== 5. 目录树操作 =====

"""
递归获取目录树结构
"""

def get_directory_tree(path, show_files=True):
    """
    获取目录树结构
    :param path: 路径对象
    :param show_files: 是否显示文件
    :return: 目录树结构列表
    """
    tree = []

    for item in sorted(path.iterdir()):
        if item.is_dir():
            tree.append({
                'name': item.name,
                'type': 'dir',
                'children': get_directory_tree(item, show_files)
            })
        elif show_files:
            tree.append({
                'name': item.name,
                'type': 'file',
                'size': item.stat().st_size
            })

    return tree


def print_directory_tree(tree, indent=0):
    """打印目录树"""
    for node in tree:
        prefix = "  " * indent
        if node['type'] == 'dir':
            print(f"{prefix}📁 {node['name']}/")
            print_directory_tree(node['children'], indent + 1)
        else:
            print(f"{prefix}📄 {node['name']} ({node['size']} bytes)")


print("\n=== 目录树结构 ===")
tree = get_directory_tree(new_dir, show_files=True)
print_directory_tree(tree)


# ===== 6. 实战应用 =====

def backup_directory(source, destination):
    """
    备份目录：递归复制所有文件
    """
    dest_path = Path(destination)

    if not dest_path.exists():
        dest_path.mkdir(parents=True, exist_ok=True)

    count = 0
    for item in source.rglob("*"):
        if item.is_file():
            # 计算相对路径
            rel_path = item.relative_to(source)
            dest_file = dest_path / rel_path

            # 确保目标目录存在
            dest_file.parent.mkdir(parents=True, exist_ok=True)

            # 复制文件
            import shutil
            shutil.copy2(item, dest_file)
            count += 1

    return count


def find_files_by_extension(directory, extension):
    """
    查找指定扩展名的所有文件
    """
    path = Path(directory)
    files = list(path.rglob(f"*.{extension}"))
    return files


def count_files_in_directory(directory):
    """
    统计目录中的文件和子目录数量
    """
    path = Path(directory)

    if not path.exists():
        return 0, 0

    file_count = 0
    dir_count = 0

    for item in path.rglob("*"):
        if item.is_file():
            file_count += 1
        elif item.is_dir():
            dir_count += 1

    return file_count, dir_count


def get_file_size(path):
    """
    获取文件大小
    """
    path = Path(path)
    if path.exists():
        return path.stat().st_size
    return 0


def create_directory_structure(base_path, structure):
    """
    创建目录结构
    :param base_path: 基础路径
    :param structure: 目录结构字典
    """
    base = Path(base_path)

    for name, content in structure.items():
        if isinstance(content, dict):
            # 子目录
            sub_dir = base / name
            sub_dir.mkdir(parents=True, exist_ok=True)
            create_directory_structure(sub_dir, content)
        else:
            # 文件
            file_path = base / name
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content)


# ===== 7. 路径操作最佳实践 =====

"""
1. 优先使用 pathlib.Path（Python 3.4+）
2. 路径拼接使用 / 操作符
3. 使用 exists() 检查路径
4. 递归操作使用 rglob()
5. 注意处理路径不存在的情况
"""

def safe_file_operation(filename):
    """安全的文件操作"""
    path = Path(filename)

    if not path.exists():
        print(f"路径不存在: {path}")
        return None

    if not path.is_file():
        print(f"路径不是文件: {path}")
        return None

    # 执行文件操作
    return path.read_text()


# ===== 测试代码 =====

print("\n=== 6. 实战应用测试 ===")

# 测试目录备份
if new_dir.exists():
    backup_dir = Path("backup_directory")
    file_count = backup_directory(new_dir, backup_dir)
    print(f"备份完成，共复制 {file_count} 个文件")

# 测试查找文件
print("\n  查找 .txt 文件:")
found_files = find_files_by_extension(".", "txt")
for f in found_files[:5]:  # 只显示前5个
    print(f"    {f}")

# 测试统计文件
file_count, dir_count = count_files_in_directory(".")
print(f"当前目录: {file_count} 个文件, {dir_count} 个子目录")

# 测试创建目录结构
structure = {
    "project": {
        "src": {
            "main.py": "# main code",
            "utils.py": "# utility functions"
        },
        "tests": {
            "test_main.py": "# test main",
            "test_utils.py": "# test utils"
        }
    },
    "docs": {
        "README.md": "# Project README"
    }
}

test_structure = Path("test_structure")
create_directory_structure(test_structure, structure)
print(f"\n目录结构创建完成: {test_structure}")
print("\n创建的结构:")
for item in sorted(test_structure.rglob("*")):
    if item.is_file():
        print(f"  {item.relative_to(test_structure)}")

# 清理测试
shutil.rmtree("new_directory", ignore_errors=True)
shutil.rmtree("backup_directory", ignore_errors=True)
shutil.rmtree("test_structure", ignore_errors=True)
