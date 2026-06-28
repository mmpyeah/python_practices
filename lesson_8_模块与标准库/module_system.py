# Lesson 8.1 - 模块系统
# ★★ 核心概念，Python 程序组织的核心

"""
模块是 Python 程序组织的基本单位。
本文档涵盖：
1. import 机制
2. __name__ 和 __main__
3. 包结构和 __init__.py
4. __all__ 导出控制
5. 相对导入
6. 模块搜索路径 sys.path
"""

# ===== 1. import 机制 =====

"""
模块是包含 Python 代码的文件
使用 import 关键字导入模块
"""

print("=== 1. import 机制 ===")

# 导入模块
import math
import sys
import os

# 使用模块中的函数和变量
print(f"math.pi = {math.pi}")
print(f"math.sqrt(16) = {math.sqrt(16)}")
print(f"sys.version = {sys.version[:30]}")
print(f"os.getcwd() = {os.getcwd()}")

# 导入模块中的特定对象
from math import sqrt, pi
print(f"sqrt(16) = {sqrt(16)}")
print(f"pi = {pi}")

# 导入模块并重命名
try:
    import numpy as np  # 虽然 numpy 可能未安装，但演示语法
    print(f"numpy 可用: numpy 版本 {np.__version__}")
except ImportError:
    np = None
    print("numpy 未安装，跳过")

# 导入所有内容（不推荐）
# from math import *  # 会导入所有公开名称


# ===== 2. __name__ 和 __main__ =====

"""
__name__ 是模块的内置属性
当直接运行模块时，__name__ 是 "__main__"
当作为模块导入时，__name__ 是模块名
"""

def greet():
    """打招呼函数"""
    print("你好！")

if __name__ == "__main__":
    print(f"当前模块名: {__name__}")
    print("这是直接运行的模块")
    greet()
else:
    print(f"当前模块名: {__name__}")
    print("这是被导入的模块")


# 创建模块示例
def process_data(data):
    """处理数据"""
    return data * 2

def calculate_sum(a, b):
    """计算和"""
    return a + b

if __name__ == "__main__":
    print("直接运行模块")
    print(process_data(10))
    print(calculate_sum(5, 3))


# ===== 3. 包结构和 __init__.py =====

"""
包是包含多个模块的目录
__init__.py 告诉 Python 这是一个包
"""

# 创建目录结构
import os
import shutil

package_dir = "mypackage"
if not os.path.exists(package_dir):
    os.makedirs(package_dir)

# 创建 __init__.py
with open(os.path.join(package_dir, "__init__.py"), 'w') as f:
    f.write('"""我的 Python 包"""\n')

# 创建子模块
with open(os.path.join(package_dir, "utils.py"), 'w') as f:
    f.write('def hello():\n    return "Hello from utils"\n')

with open(os.path.join(package_dir, "config.py"), 'w') as f:
    f.write('DEBUG = True\nBASE_URL = "http://example.com"\n')


# 在包中使用模块
print("\n=== 3. 包结构 ===")

# 尝试导入包
try:
    import mypackage
    print(f"导入包成功: {mypackage.__file__}")

    # 导入包中的模块
    from mypackage import utils, config
    print(f"utils.hello() = {utils.hello()}")
    print(f"config.DEBUG = {config.DEBUG}")
    print(f"config.BASE_URL = {config.BASE_URL}")

    # 导入包中的特定函数
    from mypackage.utils import hello
    print(f"hello() = {hello()}")

except ImportError as e:
    print(f"导入包失败: {e}")

# 清理测试文件
shutil.rmtree(package_dir, ignore_errors=True)


# ===== 4. __all__ 导出控制 =====

"""
__all__ 定义模块可以导出的公开 API
它影响 from module import * 的行为
"""

# 定义模块
__all__ = ['add', 'subtract', 'multiply', 'div']

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("不能除以零")
    return a / b

# 私有函数（不以 _ 开头，但不在 __all__ 中）
def internal_helper(x):
    """内部辅助函数"""
    return x * 2


# 导入测试
print("\n=== 4. __all__ 导出控制 ===")

# 使用 import 导入
from mymodule import add, multiply
print(f"add(5, 3) = {add(5, 3)}")
print(f"multiply(4, 3) = {multiply(4, 3)}")

# 使用 import * 导入（只导入 __all__ 中定义的）
from mymodule import *
print(f"add(5, 3) = {add(5, 3)}")
print(f"multiply(4, 3) = {multiply(4, 3)}")

# 尝试导入不在 __all__ 中的函数
try:
    from mymodule import internal_helper
    print(f"internal_helper(5) = {internal_helper(5)}")
except ImportError:
    print("无法导入 internal_helper（不在 __all__ 中）")


# ===== 5. 相对导入 =====

"""
相对导入使用点号 . 表示当前包的父包
从 . 开始表示当前包
从 .. 开始表示父包
"""

# 创建包结构
package_dir = "relative_package"
if not os.path.exists(package_dir):
    os.makedirs(package_dir)

# 创建 __init__.py
with open(os.path.join(package_dir, "__init__.py"), 'w') as f:
    f.write('"""相对导入包"""\n')

# 创建父包
parent_dir = os.path.join(package_dir, "parent")
os.makedirs(parent_dir)
with open(os.path.join(parent_dir, "__init__.py"), 'w') as f:
    f.write('"""父包"""\n')

# 创建子包
child_dir = os.path.join(parent_dir, "child")
os.makedirs(child_dir)
with open(os.path.join(child_dir, "__init__.py"), 'w') as f:
    f.write('"""子包"""\n')

# 创建子模块
with open(os.path.join(child_dir, "module.py"), 'w') as f:
    f.write('''"""子包模块"""\n
def child_function():
    return "Child function called"

def greet():
    return "Hello from child"
''')

# 创建父包模块
with open(os.path.join(parent_dir, "module.py"), 'w') as f:
    f.write('''"""父包模块"""\n
def parent_function():
    return "Parent function called"

def greet():
    return "Hello from parent"
''')

# 测试相对导入
print("\n=== 5. 相对导入 ===")

sys.path.insert(0, package_dir)

try:
    # 导入父包
    import parent
    print(f"父包模块: {parent.greet()}")

    # 导入子包
    from parent import child
    print(f"子包模块: {child.child_function()}")

    # 相对导入：从子包导入父包
    from parent.child import parent
    print(f"相对导入: {parent.greet()}")

except Exception as e:
    print(f"相对导入错误: {e}")

# 恢复路径
sys.path.remove(package_dir)

# 清理测试文件
shutil.rmtree(package_dir, ignore_errors=True)


# ===== 6. 模块搜索路径 sys.path =====

"""
sys.path 是 Python 模块搜索路径列表
包含以下位置：
1. 当前目录
2. PYTHONPATH 环境变量
3. Python 安装目录下的 site-packages
"""

print("\n=== 6. 模块搜索路径 sys.path ===")

print("sys.path 的内容:")
for i, path in enumerate(sys.path, 1):
    print(f"  {i}. {path}")

# 创建自定义模块
custom_module_content = '''"""自定义模块"""\ndef custom_function():
    return "自定义模块被调用"
'''

# 写入自定义模块
with open("custom_module.py", 'w') as f:
    f.write(custom_module_content)

# 添加当前目录到 sys.path
sys.path.insert(0, ".")

# 导入自定义模块
import custom_module
print(f"导入自定义模块: {custom_module.custom_function()}")

# 恢复路径
sys.path.remove(".")

# 清理测试文件
if os.path.exists("custom_module.py"):
    os.remove("custom_module.py")


# ===== 7. 模块别名和导入技巧 =====

"""
使用别名简化模块名
使用 from ... import ... 导入特定成员
"""

print("\n=== 7. 模块别名和导入技巧 ===")

# 1. 使用别名
import math as m
import os as operating_system
print(f"使用别名: m.pi = {m.pi}")
print(f"使用别名: operating_system.getcwd() = {operating_system.getcwd()}")

# 2. 导入特定成员
from math import sqrt, pi, sin
print(f"导入特定成员: sqrt(16) = {sqrt(16)}")
print(f"导入特定成员: pi = {pi}")

# 3. 导入所有，但重命名
from math import *
print(f"导入所有: sqrt(9) = {sqrt(9)}")

# 4. 导入类和函数
from collections import defaultdict, OrderedDict
print(f"defaultdict 示例: {defaultdict(int)}")

# 5. 导入包的属性
from os import path, mkdir, getcwd
print(f"path.join 示例: {path.join('home', 'user', 'file.txt')}")


# ===== 8. __init__.py 的高级用法 =====

"""
__init__.py 可以初始化包、设置默认导出
"""

# 创建包
package_dir = "setup_package"
os.makedirs(package_dir)

# 创建 __init__.py
with open(os.path.join(package_dir, "__init__.py"), 'w') as f:
    f.write('''"""初始化包"""\n
# 设置包的版本
__version__ = "1.0.0"

# 设置包的作者
__author__ = "Python Learner"

# 导入和导出包中的主要功能
from .utils import add, subtract
from .config import DEBUG, BASE_URL

# 设置包的文档字符串
__doc__ = """
我的设置包

这是一个示例包，展示 __init__.py 的高级用法。
"""

# 打印初始化信息
def __getattr__(name):
    """处理未定义的属性"""
    print(f"访问了未定义的属性: {name}")
    return None
''')

# 创建 utils.py
with open(os.path.join(package_dir, "utils.py"), 'w') as f:
    f.write('''"""工具模块"""\n
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b
''')

# 创建 config.py
with open(os.path.join(package_dir, "config.py"), 'w') as f:
    f.write('''"""配置模块"""\n
DEBUG = True
BASE_URL = "http://example.com"
''')

# 导入包
import sys
sys.path.insert(0, package_dir)

try:
    import setup_package as sp
    print(f"setup_package.__version__ = {sp.__version__}")
    print(f"setup_package.__author__ = {sp.__author__}")
    print(f"setup_package.__doc__ = {sp.__doc__}")
    print(f"setup_package.add(5, 3) = {sp.add(5, 3)}")
    print(f"setup_package.subtract(5, 3) = {sp.subtract(5, 3)}")
    print(f"setup_package.DEBUG = {sp.DEBUG}")

except Exception as e:
    print(f"导入错误: {e}")

# 恢复路径
sys.path.remove(package_dir)

# 清理测试文件
shutil.rmtree(package_dir, ignore_errors=True)


# ===== 测试代码 =====

print("\n=== 8. 测试代码 ===")

# 测试直接运行模块
if __name__ == "__main__":
    print("=== 直接运行模块 ===")
    greet()
    print("process_data(10) =", process_data(10))
    print("calculate_sum(5, 3) =", calculate_sum(5, 3))
