# Lesson 9.1 - 类型注解
# ★ 核心概念，Python 类型系统

"""
类型注解（Type Hints）是 Python 3.5+ 引入的特性
用于为函数参数、返回值、变量添加类型信息
本文档涵盖：
1. 基础类型注解
2. Optional、Union、List、Dict
3. 泛型（Generic）
4. mypy 静态检查简介
"""

# ===== 1. 基础类型注解 =====

"""
类型注解使用冒号（:）指定变量类型
使用箭头（->）指定返回值类型
"""

# 基础类型注解
age: int = 25
name: str = "张三"
score: float = 95.5
is_active: bool = True
count: int = 0

print("=== 1. 基础类型注解 ===")
print(f"age: {age} ({type(age).__name__})")
print(f"name: {name} ({type(name).__name__})")
print(f"score: {score} ({type(score).__name__})")
print(f"is_active: {is_active} ({type(is_active).__name__})")

# 函数类型注解
def greet(name: str, age: int) -> str:
    """问候函数"""
    return f"你好，{name}！你{age}岁了。"

result = greet("张三", 25)
print(f"\n函数调用: {result}")

# 类型注解函数
def add(a: int, b: int) -> int:
    """求和函数"""
    return a + b

def divide(a: float, b: float) -> float:
    """除法函数"""
    return a / b

print(f"\nadd(5, 3) = {add(5, 3)}")
print(f"divide(10, 2) = {divide(10, 2)}")

# ===== 2. Optional 和 Union =====

"""
Optional[Type] = Type | None
Union[Type1, Type2] = Type1 | Type2
"""

from typing import Optional, Union

# Optional：表示可以是指定类型或 None
def find_user(username: str) -> Optional[str]:
    """查找用户，可能返回 None"""
    if username == "admin":
        return "找到用户: admin"
    else:
        return None

print(f"\n=== 2. Optional 和 Union ===")
print(f"find_user('admin') = {find_user('admin')}")
print(f"find_user('unknown') = {find_user('unknown')}")

# Union：表示多种可能的类型
def process_value(value: Union[str, int, float]) -> str:
    """处理不同类型的值"""
    return f"处理: {value} ({type(value).__name__})"

print(f"\nprocess_value('hello') = {process_value('hello')}")
print(f"process_value(42) = {process_value(42)}")
print(f"process_value(3.14) = {process_value(3.14)}")

# ===== 3. List、Dict、Tuple =====

"""
List[Type] - 列表，元素类型为 Type
Dict[KeyType, ValueType] - 字典，键类型为 KeyType，值为 ValueType
Tuple[Type1, Type2, ...] - 元组
Set[Type] - 集合
"""

from typing import List, Dict, Tuple, Set

# List
names: List[str] = ["张三", "李四", "王五"]
numbers: List[int] = [1, 2, 3, 4, 5]

print(f"\n=== 3. List、Dict、Tuple ===")
print(f"names = {names}")
print(f"numbers = {numbers}")

# Dict
user_dict: Dict[str, int] = {
    "张三": 25,
    "李四": 30,
    "王五": 35
}

print(f"user_dict = {user_dict}")

# Tuple
point: Tuple[int, int] = (10, 20)
print(f"point = {point}")

# Set
unique_numbers: Set[int] = {1, 2, 3, 2, 1}
print(f"unique_numbers = {unique_numbers}")

# 类型注解的函数
def get_students() -> List[Dict[str, Union[str, int]]]:
    """获取学生列表"""
    return [
        {"name": "张三", "age": 25, "grade": "A"},
        {"name": "李四", "age": 30, "grade": "B"},
        {"name": "王五", "age": 28, "grade": "A"}
    ]

students = get_students()
for student in students:
    print(f"  {student}")

# ===== 4. 函数参数类型注解 =====

"""
使用 Callable 类型注解函数
"""

from typing import Callable

def apply_function(func: Callable[[int, int], int], x: int, y: int) -> int:
    """应用函数"""
    return func(x, y)

def multiply(a: int, b: int) -> int:
    return a * b

result = apply_function(multiply, 5, 3)
print(f"\napply_function(multiply, 5, 3) = {result}")

# ===== 5. Callable 类型 =====

"""
Callable[[参数类型], 返回类型] - 表示可调用对象
"""

from typing import Callable

def apply_operation(x: int, y: int, op: Callable[[int, int], int]) -> int:
    """应用操作"""
    return op(x, y)

result = apply_operation(10, 5, lambda a, b: a + b)
print(f"\napply_operation(10, 5, lambda a, b: a + b) = {result}")

# ===== 6. 泛型 =====

"""
泛型（Generic）用于处理多种数据类型
使用 TypeVar 定义类型变量
"""

from typing import TypeVar, Generic

# 定义类型变量
T = TypeVar('T')  # 任何类型
K = TypeVar('K')
V = TypeVar('V')

# 泛型类
class Box(Generic[T]):
    """泛型容器类"""

    def __init__(self, value: T):
        self.value = value

    def get(self) -> T:
        """获取值"""
        return self.value

    def set(self, value: T):
        """设置值"""
        self.value = value

print(f"\n=== 6. 泛型 ===")

# 使用泛型类
int_box = Box[int](42)
str_box = Box[str]("hello")

print(f"int_box.get() = {int_box.get()}")
print(f"str_box.get() = {str_box.get()}")

# 泛型函数
def get_first(items: List[T]) -> T:
    """获取列表第一个元素"""
    return items[0]

result = get_first([1, 2, 3, 4, 5])
print(f"get_first([1, 2, 3, 4, 5]) = {result}")

# ===== 7. Any 和 Unknown =====

"""
Any - 任何类型
Unknown - Python 3.10+ 的 Any 的替代品
"""

from typing import Any

def process_any(value: Any) -> str:
    """处理任何类型的值"""
    return f"值: {value} ({type(value).__name__})"

print(f"\n=== 7. Any 和 Unknown ===")
print(f"process_any(42) = {process_any(42)}")
print(f"process_any('hello') = {process_any('hello')}")
print(f"process_any([1, 2, 3]) = {process_any([1, 2, 3])}")

# ===== 8. 常用类型注解总结 =====

"""
常用类型：
- str - 字符串
- int - 整数
- float - 浮点数
- bool - 布尔值
- List[T] - 列表
- Dict[K, V] - 字典
- Tuple[T, ...] - 元组
- Set[T] - 集合
- Optional[T] - 可选类型（T | None）
- Union[T, ...] - 联合类型
- Any - 任意类型
- Callable[[参数], 返回类型] - 可调用类型
- Generic[T] - 泛型
"""

# 实战：使用类型注解
def calculate_stats(numbers: List[float]) -> Dict[str, float]:
    """计算统计信息"""
    if not numbers:
        return {"count": 0, "sum": 0.0, "avg": 0.0}

    total = sum(numbers)
    count = len(numbers)
    average = total / count
    min_val = min(numbers)
    max_val = max(numbers)

    return {
        "count": float(count),
        "sum": total,
        "avg": average,
        "min": min_val,
        "max": max_val
    }

stats = calculate_stats([1.5, 2.5, 3.5, 4.5, 5.5])
print(f"\n=== 8. 实战：统计计算 ===")
print(f"stats = {stats}")

# ===== 9. 类型检查工具 =====

"""
mypy - 静态类型检查工具
可以检测类型错误
"""

print(f"\n=== 9. 类型检查工具 ===")

print("安装 mypy:")
print("pip install mypy")

print("\n使用 mypy:")
print("mypy script.py")

# 类型注解的正确示例
def greet_user(name: str, age: int) -> str:
    """问候用户"""
    return f"你好，{name}！你{age}岁了。"

result = greet_user("张三", 25)
print(f"\n函数调用: {result}")

# 类型错误示例（注释掉以避免错误）
# def greet_user(name: int, age: str) -> str:  # 错误：参数类型与实现不匹配
#     return f"你好，{name}！你{age}岁了。"

# ===== 10. 类型注解最佳实践 =====

"""
最佳实践：
1. 为所有公共函数和变量添加类型注解
2. 使用 Union 或 Optional 表示可选类型
3. 使用泛型处理通用类型
4. 使用 TypeVar 定义类型变量
5. 避免使用 Any 除非必要
6. 定期使用 mypy 检查类型错误
7. 类型注解应该准确反映实际类型
"""

# 类型注解的最佳实践示例
from typing import List, Optional, Dict, Tuple

def process_data(data: List[Dict[str, any]]) -> Tuple[int, Optional[str]]:
    """
    处理数据并返回统计信息

    参数:
        data: 包含字典的列表，每个字典可能有不同的结构

    返回:
        元组：(总数, 错误消息)
    """
    total = 0
    error_msg: Optional[str] = None

    for item in data:
        if isinstance(item, dict):
            total += 1
        else:
            error_msg = "数据格式错误：必须是字典列表"
            break

    return (total, error_msg)

# 测试
test_data = [
    {"name": "item1"},
    {"name": "item2"},
    {"name": "item3"}
]

count, error = process_data(test_data)
print(f"\n=== 10. 类型注解最佳实践 ===")
print(f"process_data 测试:")
print(f"  总数: {count}")
print(f"  错误: {error}")
