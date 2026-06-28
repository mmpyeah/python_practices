# Lesson 8.2 - os 模块
# ★★ 核心概念，Python 运维必备

"""
os 模块提供了与操作系统交互的功能。
本文档涵盖：
1. os.path - 路径操作
2. os.listdir/walk - 文件和目录遍历
3. os.makedirs - 目录创建
4. os.environ - 环境变量
5. os.getcwd - 当前工作目录
6. shutil - 高级文件操作
"""

import os
import shutil
from pathlib import Path

# ===== 1. os.path 路径操作 =====

"""
os.path 提供路径拼接、分解、判断等功能
"""

# ===== 1.1 路径拼接 =====

print("=== 1. os.path 路径操作 ===")

# 路径拼接
path1 = os.path.join("home", "user", "documents", "file.txt")
path2 = os.path.join("home", "user", "documents", "folder")
print(f"路径拼接: {path1}")
print(f"目录路径: {path2}")

# 路径分解
print(f"\n路径分解:")
print(f"  dirname: {os.path.dirname(path1)}")
print(f"  basename: {os.path.basename(path1)}")
print(f"  splitext: {os.path.splitext(path1)}")
print(f"  split: {os.path.split(path1)}")

# 相对路径
relative_path = os.path.relpath(path1, "home")
print(f"\n相对路径: {relative_path}")

# 绝对路径
absolute_path = os.path.abspath(relative_path)
print(f"绝对路径: {absolute_path}")

# ===== 1.2 路径判断 =====

print(f"\n路径判断:")
print(f"  路径存在: {os.path.exists(path1)}")
print(f"  是文件: {os.path.isfile(path1)}")
print(f"  是目录: {os.path.isdir(path2)}")
print(f"  绝对路径: {os.path.isabs(path1)}")
print(f"  绝对路径: {os.path.isabs('relative.txt')}")

# 路径规范化
normalized_path = os.path.normpath("/home/user/./documents/../documents/file.txt")
print(f"\n路径规范化: {normalized_path}")

# ===== 1.3 路径获取 =====

print(f"\n路径获取:")
print(f"  当前目录: {os.getcwd()}")
print(f"  当前目录: {Path('.').resolve()}")
print(f"  用户目录: {os.path.expanduser('~')}")
print(f"  当前文件: {os.path.abspath(__file__)}")

# ===== 2. os.listdir 和 os.walk =====

"""
os.listdir() - 列出目录内容
os.walk() - 递归遍历目录树
"""

# ===== 2.1 os.listdir() =====

print("\n=== 2. os.listdir() ===")

# 创建测试目录
test_dir = "test_listdir"
os.makedirs(test_dir, exist_ok=True)

# 创建测试文件
for i in range(3):
    with open(os.path.join(test_dir, f"file{i}.txt"), 'w') as f:
        f.write(f"文件 {i} 的内容")

with open(os.path.join(test_dir, "subdir", "nested.txt"), 'w') as f:
    f.write("嵌套文件的内容")

os.makedirs(os.path.join(test_dir, "subdir"))

# 列出目录内容
print(f"目录: {test_dir}")
entries = os.listdir(test_dir)
for entry in sorted(entries):
    path = os.path.join(test_dir, entry)
    is_dir = os.path.isdir(path)
    print(f"  {entry} ({'目录' if is_dir else '文件'})")

# 使用 Path.listdir()
print(f"\n使用 Path.listdir():")
for entry in sorted(Path(test_dir).iterdir()):
    print(f"  {entry.name} ({'目录' if entry.is_dir() else '文件'})")

# ===== 2.2 os.walk() =====

print(f"\n=== 2. os.walk() 递归遍历 ===")

# 递归遍历目录
for root, dirs, files in os.walk(test_dir):
    level = root.replace(test_dir, '').count(os.sep)
    indent = ' ' * 2 * level
    print(f'{indent}{os.path.basename(root)}/')

    subindent = ' ' * 2 * (level + 1)
    for file in files:
        print(f'{subindent}{file}')
    for dir in dirs:
        print(f'{subindent}{dir}/')

# 使用 Path.rglob() 进行递归 glob
print(f"\n使用 Path.rglob() 进行递归 glob:")
for file_path in sorted(Path(test_dir).rglob("*.txt")):
    print(f"  {file_path.relative_to(test_dir)}")


# ===== 3. os.makedirs - 目录创建 =====

"""
os.makedirs() - 创建多级目录
os.makedirs() exist_ok=True 参数避免已存在时出错
"""

print("\n=== 3. os.makedirs 创建目录 ===")

# 创建多级目录
dir_path = os.path.join("test_dir", "level1", "level2", "level3")
print(f"创建目录: {dir_path}")
os.makedirs(dir_path, exist_ok=True)

# 验证目录已创建
print(f"目录存在: {os.path.exists(dir_path)}")
print(f"是目录: {os.path.isdir(dir_path)}")

# 创建时的错误处理
try:
    # 尝试创建已存在的目录
    os.makedirs(dir_path, exist_ok=True)
    print(f"目录已存在，成功创建")
except Exception as e:
    print(f"错误: {e}")

# ===== 4. os.environ - 环境变量 =====

"""
os.environ 用于访问和设置环境变量
"""

print("\n=== 4. os.environ 环境变量 ===")

# 读取环境变量
print(f"当前用户: {os.environ.get('USER', '未知')}")
print(f"当前系统: {os.environ.get('OS', '未知')}")
print(f"当前路径长度: {len(os.environ.get('PATH', ''))} 字符")

# 设置环境变量（仅当前进程有效）
test_var = "test_value"
os.environ['TEST_VAR'] = test_var
print(f"设置环境变量: TEST_VAR={test_var}")
print(f"读取环境变量: {os.environ.get('TEST_VAR')}")

# 环境变量遍历
print(f"\n所有环境变量:")
count = 0
for key, value in os.environ.items():
    count += 1
    if count > 5:  # 只显示前几个
        print(f"  ... (共 {len(os.environ)} 个变量)")
        break
    print(f"  {key}={value}")

# ===== 5. shutil - 高级文件操作 =====

"""
shutil 提供高级文件和目录操作
"""

# ===== 5.1 复制文件 =====

print("\n=== 5. shutil 高级文件操作 ===")

# 创建源文件
source_file = os.path.join(test_dir, "source.txt")
with open(source_file, 'w') as f:
    f.write("这是源文件的内容")

# 复制文件
dest_file = os.path.join(test_dir, "destination.txt")
shutil.copy2(source_file, dest_file)
print(f"复制文件: {source_file} -> {dest_file}")

# 验证文件已复制
print(f"文件存在: {os.path.exists(dest_file)}")

# ===== 5.2 复制目录 =====

print(f"\n复制目录:")

# 创建源目录
source_dir = os.path.join(test_dir, "source_dir")
os.makedirs(source_dir)
with open(os.path.join(source_dir, "file1.txt"), 'w') as f:
    f.write("源目录文件1")
with open(os.path.join(source_dir, "file2.txt"), 'w') as f:
    f.write("源目录文件2")

# 复制目录
dest_dir = os.path.join(test_dir, "dest_dir")
shutil.copytree(source_dir, dest_dir)
print(f"复制目录: {source_dir} -> {dest_dir}")

# 验证目录已复制
print(f"目录存在: {os.path.exists(dest_dir)}")

# 列出复制的目录内容
print(f"\n复制后的目录内容:")
for root, dirs, files in os.walk(dest_dir):
    level = root.replace(dest_dir, '').count(os.sep)
    indent = ' ' * 2 * level
    print(f'{indent}{os.path.basename(root)}/')
    subindent = ' ' * 2 * (level + 1)
    for file in files:
        print(f'{subindent}{file}')

# ===== 5.3 移动文件/目录 =====

print(f"\n移动文件:")
shutil.move(source_file, dest_file)
print(f"移动文件: {source_file} -> {dest_file}")
print(f"源文件存在: {os.path.exists(source_file)}")
print(f"目标文件存在: {os.path.exists(dest_file)}")

# ===== 5.4 删除文件/目录 =====

print(f"\n删除文件和目录:")
# 删除文件
os.remove(dest_file)
print(f"删除文件: {dest_file}")
print(f"文件存在: {os.path.exists(dest_file)}")

# 删除空目录
os.rmdir(os.path.join(dest_dir, "file1.txt.txt"))  # 不存在
os.rmdir(os.path.join(test_dir, "empty_dir"))  # 不存在

# 使用 shutil.rmtree 删除非空目录
print(f"删除目录: {dest_dir}")
shutil.rmtree(dest_dir)
print(f"目录存在: {os.path.exists(dest_dir)}")

# ===== 5.5 获取文件大小 =====

print(f"\n获取文件大小:")
file_path = os.path.join(test_dir, "file0.txt")
with open(file_path, 'w') as f:
    f.write("这是一些测试内容")

size = os.path.getsize(file_path)
print(f"文件: {file_path}")
print(f"大小: {size} 字节")

# ===== 5.6 重命名 =====

print(f"\n重命名文件:")
old_name = os.path.join(test_dir, "file0.txt")
new_name = os.path.join(test_dir, "renamed_file.txt")
os.rename(old_name, new_name)
print(f"重命名: {old_name} -> {new_name}")

# ===== 6. 实战应用 - 系统信息 =====

class SystemInfo:
    """系统信息类"""

    @staticmethod
    def get_current_directory():
        """获取当前工作目录"""
        return os.getcwd()

    @staticmethod
    def get_disk_usage():
        """获取磁盘使用情况"""
        usage = shutil.disk_usage("/")
        return {
            "total": usage.total,
            "used": usage.used,
            "free": usage.free
        }

    @staticmethod
    def list_top_directories():
        """列出顶层目录"""
        return os.listdir(".")

    @staticmethod
    def create_temp_directory():
        """创建临时目录"""
        temp_dir = os.path.join(os.getcwd(), "temp", "test")
        os.makedirs(temp_dir, exist_ok=True)
        return temp_dir

    @staticmethod
    def cleanup_temp_directory(temp_dir):
        """清理临时目录"""
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            return True
        return False

    @staticmethod
    def get_file_permissions(file_path):
        """获取文件权限"""
        if os.path.exists(file_path):
            return os.stat(file_path).st_mode
        return None


print("\n=== 6. 实战应用 - 系统信息 ===")

print(f"当前目录: {SystemInfo.get_current_directory()}")
print(f"磁盘使用: {SystemInfo.get_disk_usage()}")

dirs = SystemInfo.list_top_directories()
print(f"\n顶层目录 ({len(dirs)} 个):")
for d in dirs:
    print(f"  - {d}")

# 测试临时目录
temp_dir = SystemInfo.create_temp_directory()
print(f"\n创建临时目录: {temp_dir}")

# 测试文件权限
test_file = os.path.join(temp_dir, "test.txt")
with open(test_file, 'w') as f:
    f.write("测试内容")

perms = SystemInfo.get_file_permissions(test_file)
print(f"测试文件权限: {perms}")

# 清理
SystemInfo.cleanup_temp_directory(temp_dir)


# ===== 7. pathlib - 现代路径操作 =====

"""
pathlib 提供更现代的路径操作方式
"""

print("\n=== 7. pathlib 现代路径操作 ===")

# 使用 pathlib 创建路径
path = Path("home") / "user" / "documents"
print(f"路径: {path}")

# 路径操作
path.mkdir(parents=True, exist_ok=True)
print(f"路径存在: {path.exists()}")
print(f"是目录: {path.is_dir()}")

# 列出目录
files = list(path.glob("*.txt"))
print(f"找到 {len(files)} 个 .txt 文件")

# 清理
shutil.rmtree("home", ignore_errors=True)


# ===== 8. 路径操作最佳实践 =====

"""
最佳实践：
1. 优先使用 pathlib.Path（Python 3.4+）
2. 使用 os.path 进行兼容性处理
3. 使用 os.makedirs() 创建目录
4. 使用 shutil.copytree() 复制目录
5. 使用 shutil.rmtree() 删除目录
"""

def backup_directory(source, destination):
    """
    备份目录
    """
    try:
        # 复制目录
        shutil.copytree(source, destination)
        print(f"备份完成: {source} -> {destination}")
        return True
    except Exception as e:
        print(f"备份失败: {e}")
        return False


def clean_directory(directory):
    """
    清理目录（删除所有内容）
    """
    try:
        if os.path.exists(directory):
            shutil.rmtree(directory)
            print(f"目录已清理: {directory}")
            return True
        return False
    except Exception as e:
        print(f"清理失败: {e}")
        return False


print("\n=== 8. 路径操作最佳实践 ===")

# 测试目录备份
test_dir = "test_backup"
os.makedirs(test_dir)

with open(os.path.join(test_dir, "test.txt"), 'w') as f:
    f.write("测试内容")

backup_dir = "backup_test"
backup_directory(test_dir, backup_dir)

# 清理
clean_directory(test_dir)
clean_directory(backup_dir)


# ===== 测试代码 =====

# 测试代码
if __name__ == "__main__":
    print("=== 测试 os 模块 ===")
    print(f"Python 版本: {sys.version}")
    print(f"当前目录: {os.getcwd()}")
    print(f"系统: {os.name}")
    print(f"平台: {os.platform}")

    # 列出当前目录
    print(f"\n当前目录内容:")
    for item in sorted(os.listdir(".")):
        print(f"  - {item}")


# 清理测试目录
for d in ["test_listdir", "test_dir", "temp", "home", "source_dir", "dest_dir", "backup_test"]:
    if os.path.exists(d):
        shutil.rmtree(d, ignore_errors=True)
