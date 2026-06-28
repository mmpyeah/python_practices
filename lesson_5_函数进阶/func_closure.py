# Lesson 5.5 - 闭包
# ★ 核心概念，函数式编程和高级编程的基础

"""
闭包是 Python 中一个非常强大的特性。
闭包 = 函数 + 环境变量（即函数定义时的作用域）

闭包应用场景：
1. 函数工厂 - 创建特定功能的函数
2. 数据隐藏 - 创建私有变量
3. 状态保持 - 维护函数调用之间的状态
4. 装饰器基础
"""

import time

# ===== 1. 闭包基本原理 =====

"""
闭包是指一个函数能够访问它定义时所在作用域的变量。
即使外部函数已经返回，闭包仍然可以访问这些变量。
"""

def outer_function():
    """外部函数"""
    x = 10  # 自由变量

    def inner_function():
        """内部函数（闭包）"""
        print(f"x = {x}")

    return inner_function  # 返回内部函数


closure = outer_function()
closure()  # 输出: x = 10


# ===== 2. 闭包的三个要素 =====

"""
1. 嵌套函数
2. 内部函数引用外部变量
3. 外部函数返回内部函数
"""

def create_multiplier(n):
    """函数工厂：创建乘法函数"""

    def multiply(x):
        """内部函数：实际执行乘法"""
        return x * n

    return multiply


# 创建不同的乘法函数
multiply_by_2 = create_multiplier(2)
multiply_by_3 = create_multiplier(3)
multiply_by_5 = create_multiplier(5)

print(f"multiply_by_2(4) = {multiply_by_2(4)}")   # 8
print(f"multiply_by_3(4) = {multiply_by_3(4)}")   # 12
print(f"multiply_by_5(4) = {multiply_by_5(4)}")   # 20


# ===== 3. nonlocal 关键字 =====

"""
nonlocal 用于修改外部函数中的变量
相当于"外部作用域的变量"

注：Python 中只能读取外部函数的变量，不能直接修改
必须使用 nonlocal 关键字
"""

def counter():
    """计数器闭包"""
    count = 0  # 自由变量

    def increment():
        nonlocal count  # 声明要修改外部变量
        count += 1
        return count

    def get_count():
        return count

    return increment, get_count


increment, get_count = counter()

print(f"increment() = {increment()}")  # 1
print(f"increment() = {increment()}")  # 2
print(f"get_count() = {get_count()}")  # 2

# 重置计数器
def counter_with_reset():
    count = 0

    def increment():
        nonlocal count
        count += 1
        return count

    def reset():
        nonlocal count
        count = 0
        return count

    return increment, reset


inc, reset = counter_with_reset()
print(f"increment() = {inc()}")  # 1
print(f"reset() = {reset()}")   # 0


# ===== 4. 闭包 vs 全局变量 =====

"""
闭包可以替代全局变量，但更安全
闭包可以保护变量不被外部访问和修改
"""

global_var = 100  # 全局变量

def use_global():
    return global_var

def use_closure():
    x = 100
    def inner():
        return x
    return inner

print(f"use_global() = {use_global()}")  # 100
print(f"use_closure()() = {use_closure()}()")  # 100

# 全局变量的问题：
# 1. 容易被意外修改
# 2. 污染全局命名空间
# 3. 难以追踪和调试

# 闭包的优势：
# 1. 数据封装
# 2. 更好的作用域控制
# 3. 避免全局变量污染


# ===== 5. 数据隐藏 =====

"""
闭包可以创建私有变量
外部无法直接访问和修改
"""

def create_secure_bank():
    """创建银行账户闭包"""
    balance = 0  # 私有变量

    def deposit(amount):
        nonlocal balance
        if amount > 0:
            balance += amount
            return f"存入 ${amount}，当前余额: ${balance}"
        return "存入金额必须为正数"

    def withdraw(amount):
        nonlocal balance
        if amount <= balance:
            balance -= amount
            return f"取出 ${amount}，当前余额: ${balance}"
        return "余额不足"

    def get_balance():
        return balance  # 但提供了获取方法

    return deposit, withdraw, get_balance


deposit, withdraw, get_balance = create_secure_bank()

print("=== 银行账户测试 ===")
print(deposit(1000))  # 存入 $1000，当前余额: $1000
print(withdraw(200))  # 取出 $200，当前余额: $800
print(get_balance())  # 800

# 无法直接访问 balance
# print(balance)  # NameError


# ===== 6. 状态保持 =====

"""
闭包可以保存函数调用之间的状态
适合需要持久化状态的场景
"""

def create_cache():
    """缓存装饰器（简化版）"""
    cache = {}

    def get_or_compute(key, compute_func):
        if key in cache:
            print(f"[CACHE] 命中缓存: {key}")
            return cache[key]
        result = compute_func()
        cache[key] = result
        print(f"[CACHE] 添加缓存: {key}")
        return result

    return get_or_compute


cached = create_cache()


def expensive_computation():
    """模拟耗时计算"""
    print("[COMPUTE] 执行计算...")
    return 42


print("\n=== 缓存测试 ===")
print(cached("result1", expensive_computation))
print(cached("result1", expensive_computation))  # 命中缓存


# ===== 7. 闭包的循环陷阱 =====

"""
闭包中使用循环变量时要注意陷阱
"""

def create_counter_functions():
    """创建多个计数器（常见错误）"""
    funcs = []

    for i in range(3):
        def counter():
            return i
        funcs.append(counter)

    return funcs


# 错误：所有计数器都返回最后的值
wrong_funcs = create_counter_functions()
for func in wrong_funcs:
    print(f"wrong_funcs counter() = {func()}")  # 都是 2

# 正确：使用默认参数
def create_counter_functions_correct():
    """创建多个计数器（正确方法）"""
    funcs = []

    for i in range(3):
        def counter(x=i):
            return x
        funcs.append(counter)

    return funcs


# 正确：使用闭包捕获当前值
def create_counter_functions_closure():
    """创建多个计数器（闭包方法）"""
    funcs = []

    for i in range(3):
        def make_counter(val=i):
            return lambda: val
        funcs.append(make_counter())

    return funcs


# ===== 8. 实战应用 =====

# 1. 装饰器基础
def timer_decorator(func):
    """计时装饰器（使用闭包）"""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        elapsed = end - start
        print(f"[TIMER] {func.__name__} 耗时 {elapsed:.4f} 秒")
        return result
    return wrapper


# 2. 数据验证器
def create_validator(validation_func):
    """创建验证器函数"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # 提取参数
            if hasattr(args[0], '__dict__'):
                data = args[0].__dict__
            else:
                data = kwargs

            # 验证
            errors = validation_func(data)
            if errors:
                raise ValueError(f"验证失败: {errors}")

            return func(*args, **kwargs)
        return wrapper
    return decorator


# 3. 限流器
def create_limiter(max_calls):
    """限流器：限制函数调用频率"""
    calls = [0]
    last_call = [0]

    def decorator(func):
        def wrapper(*args, **kwargs):
            current_time = time.time()

            # 检查是否超过时间限制
            if calls[0] >= max_calls:
                if current_time - last_call[0] < 1:  # 1秒内最多调用max_calls次
                    raise RuntimeError("调用过于频繁，请稍后再试")
                calls[0] = 0  # 重置计数

            calls[0] += 1
            last_call[0] = current_time
            return func(*args, **kwargs)
        return wrapper
    return decorator


# 4. HTTP 请求发送器
def create_request_sender():
    """创建发送请求的函数"""
    request_count = 0

    def send_request(url, method='GET'):
        nonlocal request_count
        request_count += 1
        print(f"[REQUEST #{request_count}] {method} {url}")
        return f"成功发送请求: {method} {url}"

    def get_count():
        return request_count

    return send_request, get_count


# ===== 9. 闭包链式调用 =====

"""
闭包可以创建链式调用的接口
"""

class Builder:
    """建造者模式"""
    def __init__(self):
        self.data = {}

    def set_name(self, name):
        self.data['name'] = name
        return self

    def set_age(self, age):
        self.data['age'] = age
        return self

    def set_email(self, email):
        self.data['email'] = email
        return self

    def build(self):
        return self.data


builder = Builder()
result = (Builder()
          .set_name("Alice")
          .set_age(25)
          .set_email("alice@example.com")
          .build())

print(f"Builder 结果: {result}")


# ===== 10. 闭包与类对比 =====

"""
在某些场景下，闭包比类更简单
"""

class CounterClass:
    """使用类实现计数器"""
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1
        return self.count

    def get_count(self):
        return self.count


def counter_closure():
    """使用闭包实现计数器"""
    count = 0

    def increment():
        nonlocal count
        count += 1
        return count

    def get_count():
        return count

    return increment, get_count


print("=== 类 vs 闭包 ===")
counter_obj = CounterClass()
for i in range(3):
    print(f"counter_obj.increment() = {counter_obj.increment()}")

inc, get_count = counter_closure()
for i in range(3):
    print(f"inc() = {inc()}")


# ===== 测试代码 =====

print("\n=== 1. 闭包基本测试 ===")
print(f"multiply_by_2(5) = {multiply_by_2(5)}")
print(f"multiply_by_3(5) = {multiply_by_3(5)}")

print("\n=== 2. 计数器测试 ===")
inc, get_count = counter()
print(f"inc() = {inc()}")
print(f"inc() = {inc()}")
print(f"get_count() = {get_count()}")

print("\n=== 3. 银行账户测试 ===")
deposit, withdraw, get_balance = create_secure_bank()
print(deposit(5000))
print(withdraw(1000))
print(get_balance())

print("\n=== 4. 缓存测试 ===")
print(cached("result2", expensive_computation))
print(cached("result2", expensive_computation))

print("\n=== 5. 闭包陷阱测试 ===")
print("错误版本（都是2）:")
for func in wrong_funcs:
    print(f"  {func()}")

print("\n正确版本:")
for func in create_counter_functions_correct():
    print(f"  {func()}")

print("\n闭包版本:")
for func in create_counter_functions_closure():
    print(f"  {func()}")

print("\n=== 6. 限流器测试 ===")
@create_limiter(3)
def limited_function():
    return "执行了操作"

for i in range(5):
    try:
        print(f"limited_function() 调用 {i+1}: {limited_function()}")
    except RuntimeError as e:
        print(f"调用 {i+1} 失败: {e}")

print("\n=== 7. 请求发送器测试 ===")
send, get_count = create_request_sender()
print(send("https://api.example.com/data", "GET"))
print(send("https://api.example.com/data", "POST"))
print(get_count())
