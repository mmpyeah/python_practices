# Lesson 5.1 - 函数参数详解
# ★★★ 核心概念，函数式编程的基础

"""
函数参数是 Python 中非常灵活的概念，理解好这部分才能写出优雅、可复用的代码。

本文档涵盖：
1. 位置参数 vs 关键字参数
2. 默认参数的陷阱
3. *args 收集位置参数
4. **kwargs 收集关键字参数
5. 参数解包
"""

# ===== 1. 基本参数类型 =====

def greet(name, greeting="Hello", times=1):
    """
    函数参数默认值
    greeting: 默认 "Hello"
    times: 重复次数
    """
    result = f"{greeting}, {name}!"
    return result * times


# ===== 2. *args - 收集位置参数 =====

def sum_all(*args):
    """
    *args 将位置参数收集为一个元组
    调用方式：sum_all(1, 2, 3, 4, 5)
    """
    return sum(args)


def print_names(*names):
    """
    *names 收集所有传入的名称，用于遍历
    """
    print(f"共收到 {len(names)} 个名字：")
    for i, name in enumerate(names, 1):
        print(f"  {i}. {name}")


# ===== 3. **kwargs - 收集关键字参数 =====

def process_data(**kwargs):
    """
    **kwargs 将关键字参数收集为一个字典
    """
    print("接收到的参数：")
    for key, value in kwargs.items():
        print(f"  {key} = {value}")


def create_user(**info):
    """
    创建用户，关键字参数收集所有信息
    """
    print(f"创建用户：{info.get('name', '未命名')}")
    print(f"年龄：{info.get('age', '未知')}")
    print(f"邮箱：{info.get('email', '无')}")


# ===== 4. 参数解包 =====

def concat_str(a, b, c):
    """
    需要三个参数的函数
    """
    return f"{a} - {b} - {c}"


# ===== 5. 位置参数解包 =====

args = ['hello', 'world', 'python']
result = concat_str(*args)
print(f"位置参数解包：{result}")  # hello - world - python

# ===== 6. 关键字参数解包 =====

kwargs = {'a': 'foo', 'b': 'bar', 'c': 'baz'}
result = concat_str(**kwargs)
print(f"关键字参数解包：{result}")  # foo - bar - baz

# ===== 7. 默认参数的陷阱 =====

def append_item(item, items=[]):
    """
    ⚠️ 默认参数陷阱：默认参数只在函数定义时创建一次
    """
    items.append(item)
    return items


def append_item_safe(item, items=None):
    """
    安全版本：每次调用都创建新的列表
    """
    if items is None:
        items = []
    items.append(item)
    return items


# ===== 8. 参数类型混合 =====

def mixed_params(a, b, c=10, d=20, *args, e=30, **kwargs):
    """
    参数顺序：
    1. 位置参数 (a, b)
    2. 默认位置参数 (c=10, d=20)
    3. *args - 收集额外位置参数
    4. 关键字参数 (e=30)
    5. **kwargs - 收集额外关键字参数
    """
    result = {
        'a': a,
        'b': b,
        'c': c,
        'd': d,
        'args': args,
        'e': e,
        'kwargs': kwargs
    }
    return result


# ===== 9. 实战应用 =====

def create_config_file(filename, *sections, **options):
    """
    创建配置文件，模拟写入.ini风格配置
    """
    print(f"\n创建配置文件：{filename}")
    for section in sections:
        print(f"\n[{section}]")
        for key, value in options.items():
            print(f"{key} = {value}")


# ===== 测试代码 =====

# 1. 基本调用
print("=== 1. 基本调用 ===")
print(greet("Alice"))          # Hello, Alice!
print(greet("Bob", "Hi", 2))   # Hi, Bob!\nHi, Bob!

# 2. *args 测试
print("\n=== 2. *args 测试 ===")
print(f"sum_all(1, 2, 3) = {sum_all(1, 2, 3)}")
print(f"sum_all(10, 20, 30, 40) = {sum_all(10, 20, 30, 40)}")

print_names("Alice", "Bob", "Charlie", "David")
print_names("Xiaoming", "Xiaohong")

# 3. **kwargs 测试
print("\n=== 3. **kwargs 测试 ===")
process_data(name="Alice", age=25, city="Beijing")
process_data(username="bob", level="admin")

create_user(name="张三", age=30, email="zhangsan@example.com")

# 4. 参数解包
print("\n=== 4. 参数解包 ===")
print(f"位置解包：{concat_str(*args)}")
print(f"关键字解包：{concat_str(**kwargs)}")

# 5. 默认参数陷阱
print("\n=== 5. 默认参数陷阱 ===")
print(f"append_item(1) = {append_item(1)}")   # [1]
print(f"append_item(2) = {append_item(2)}")   # [1, 2] ⚠️ 修改了之前的列表！
print(f"append_item_safe(1) = {append_item_safe(1)}")   # [1]
print(f"append_item_safe(2) = {append_item_safe(2)}")   # [2] ✅ 安全

# 6. 混合参数测试
print("\n=== 6. 混合参数测试 ===")
print(mixed_params(1, 2))       # 只传位置参数
print(mixed_params(1, 2, 3, 4))  # 3变成c，4进args
print(mixed_params(1, 2, e=100))  # e覆盖默认值

# 7. 实战应用
print("\n=== 7. 实战应用 ===")
create_config_file("config.ini", "database", host="localhost", port=5432)
create_config_file("settings.ini", "logging", level="DEBUG", file="app.log")
