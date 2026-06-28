# Lesson 5.3 - 装饰器
# ★★★ 核心概念，函数式编程和元编程的基础

"""
装饰器是一种特殊的函数，它可以修改其他函数的行为。
Python 中 @decorator_name 语法糖的本质就是函数包装器。

本文档涵盖：
1. 装饰器原理和语法
2. @wraps 装饰器
3. 带参数的装饰器
4. 计时器装饰器
5. 日志装饰器
6. 权限校验装饰器
7. 带返回值的装饰器
"""

# ===== 1. 装饰器基本原理 =====

"""
装饰器本质上是一个函数，它接收一个函数作为参数，并返回一个新函数
"""

def my_decorator(func):
    """简单装饰器示例"""
    def wrapper():
        print(f"正在调用函数: {func.__name__}")
        func()
        print("函数调用完成")
    return wrapper


@my_decorator
def greet():
    """需要被装饰的函数"""
    print("Hello, World!")


# 等价的 def 版本
def greet_without_decorator():
    print("Hello, World!")


# 手动调用装饰器
print("=== 手动调用装饰器 ===")
decorated_greet = my_decorator(greet_without_decorator)
decorated_greet()


# ===== 2. 保留函数元信息 =====

"""
问题：装饰器会修改函数的 __name__、__doc__ 等属性
解决方案：使用 functools.wraps 装饰器
"""

from functools import wraps

def log_decorator(func):
    """保留函数元信息的装饰器"""
    @wraps(func)  # 保留原始函数的元信息
    def wrapper(*args, **kwargs):
        print(f"[LOG] 调用 {func.__name__}，参数: {args}, {kwargs}")
        result = func(*args, **kwargs)
        print(f"[LOG] {func.__name__} 返回: {result}")
        return result
    return wrapper


@log_decorator
def add_numbers(a, b):
    """计算两个数的和"""
    return a + b


@log_decorator
def greet_user(name, greeting="Hello"):
    """问候用户"""
    return f"{greeting}, {name}!"


print(f"greet_user.__name__ = {greet_user.__name__}")
print(f"greet_user.__doc__ = {greet_user.__doc__}")


# ===== 3. 计时器装饰器 =====

"""
用于测量函数执行时间
"""

import time

def timer_decorator(func):
    """计时装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed = end_time - start_time
        print(f"[TIME] {func.__name__} 耗时 {elapsed:.6f} 秒")
        return result
    return wrapper


@timer_decorator
def slow_function():
    """模拟慢速函数"""
    time.sleep(0.1)  # 睡眠 0.1 秒
    return "完成"


@timer_decorator
def fast_function():
    """模拟快速函数"""
    return "立即完成"


# ===== 4. 日志装饰器 =====

"""
记录函数调用、入参、出参
"""

def log_calls(func):
    """详细日志装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"  [CALL] {func.__name__} 被 {func.__module__} 调用")
        print(f"  [CALL] 参数: {args}, {kwargs}")

        try:
            result = func(*args, **kwargs)
            print(f"  [CALL] 返回: {result}")
            return result
        except Exception as e:
            print(f"  [CALL] 异常: {type(e).__name__}: {e}")
            raise
    return wrapper


@log_calls
def divide(a, b):
    """除法函数"""
    if b == 0:
        raise ValueError("除数不能为 0")
    return a / b


# ===== 5. 权限校验装饰器 =====

"""
用于验证用户权限
"""

def require_permission(permission):
    """权限校验装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 模拟权限检查
            user_permissions = kwargs.get('permissions', [])
            if permission not in user_permissions:
                print(f"[PERMISSION] 拒绝访问: 需要 '{permission}' 权限")
                raise PermissionError(f"缺少 '{permission}' 权限")
            print(f"[PERMISSION] 允许访问: '{permission}'")
            return func(*args, **kwargs)
        return wrapper
    return decorator


@require_permission("admin")
def delete_user(user_id, permissions):
    """删除用户（需要 admin 权限）"""
    return f"用户 {user_id} 已删除"


@require_permission("user_read")
def read_user(user_id, permissions):
    """读取用户信息（需要 user_read 权限）"""
    return f"用户 {user_id} 信息: {user_id}"


# ===== 6. 重试装饰器 =====

"""
函数失败时自动重试
"""

def retry(times=3, delay=1):
    """重试装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == times:
                        raise  # 最后一次失败则抛出异常
                    print(f"[RETRY] 第 {attempt} 次失败: {e}，{delay} 秒后重试...")
                    time.sleep(delay)
        return wrapper
    return decorator


@retry(times=3, delay=0.5)
def unstable_operation():
    """模拟不稳定的操作"""
    import random
    if random.random() < 0.5:
        raise ValueError("操作失败")
    return "成功"


# ===== 7. 带参数的装饰器 =====

"""
装饰器本身可以接受参数
"""

def repeat(times):
    """带参数的装饰器：指定重复次数"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            for i in range(times):
                print(f"[REPEAT] 第 {i+1}/{times} 次调用")
                result = func(*args, **kwargs)
                results.append(result)
            return results
        return wrapper
    return decorator


@repeat(times=3)
def say_hello(name="World"):
    """重复打招呼"""
    print(f"Hello, {name}!")
    return f"{name}"


def cache_decorator(ttl=None):
    """带参数的缓存装饰器：设置缓存过期时间"""
    from functools import lru_cache

    if ttl:
        # 带过期时间的简单实现
        cache = {}
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                cache_key = (args, tuple(sorted(kwargs.items())))
                if cache_key in cache:
                    print(f"[CACHE] 命中缓存: {func.__name__}")
                    return cache[cache_key]
                result = func(*args, **kwargs)
                cache[cache_key] = result
                return result
            return wrapper
    else:
        # 使用 lru_cache
        return lru_cache(maxsize=None)
    return decorator


# ===== 8. 多个装饰器叠加 =====

"""
Python 从下往上应用装饰器
"""

def uppercase_decorator(func):
    """大写化装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result.upper()
    return wrapper


def exclamation_decorator(func):
    """感叹号装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result + "!"
    return wrapper


@uppercase_decorator
@exclamation_decorator
def greet_person(name):
    """问候某个人"""
    return f"Hello {name}"


# ===== 9. 实战应用 =====

def validate_input(validation_func):
    """输入验证装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 从参数中提取输入
            if hasattr(args[0], '__dict__'):
                data = args[0].__dict__
            else:
                data = kwargs

            # 验证输入
            errors = validation_func(data)
            if errors:
                print(f"[VALIDATION] 输入验证失败: {errors}")
                raise ValueError(f"输入验证失败: {errors}")

            return func(*args, **kwargs)
        return wrapper
    return decorator


def validate_age(data):
    """年龄验证"""
    errors = []
    if 'age' in data:
        age = data['age']
        if not isinstance(age, int) or age < 0 or age > 150:
            errors.append(f"年龄必须是 0-150 之间的整数，得到: {age}")
    return errors


@validate_input(validate_age)
def register_user(user):
    """注册用户"""
    return f"用户 {user.name} 注册成功，年龄: {user.age}"


class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age


# ===== 10. 装饰器模式总结 =====

"""
装饰器模式的核心思想：
1. 将原函数包装在一个新函数中
2. 新函数可以添加前置/后置逻辑
3. 保持原函数的元信息
4. 支持嵌套和叠加

应用场景：
- 计时/性能分析
- 日志记录
- 缓存
- 权限验证
- 输入验证
- 重试机制
"""

# ===== 测试代码 =====

print("\n=== 1. 装饰器基本测试 ===")
greet()


print("\n=== 2. 保留元信息测试 ===")
print(f"greet_user.__name__ = {greet_user.__name__}")
print(f"greet_user.__doc__ = {greet_user.__doc__}")
print(f"greet_user(3, 4) = {greet_user(3, 4)}")


print("\n=== 3. 计时器测试 ===")
print(f"slow_function() 结果: {slow_function()}")
print(f"fast_function() 结果: {fast_function()}")


print("\n=== 4. 日志测试 ===")
divide(10, 2)
divide(5, 0)  # 会抛出异常


print("\n=== 5. 权限测试 ===")
try:
    delete_user(1, permissions=['user_read'])
except PermissionError as e:
    print(f"捕获异常: {e}")

try:
    read_user(1, permissions=['admin'])
except PermissionError as e:
    print(f"捕获异常: {e}")


print("\n=== 6. 重试测试 ===")
try:
    result = unstable_operation()
    print(f"unstable_operation() 结果: {result}")
except Exception as e:
    print(f"最终失败: {e}")


print("\n=== 7. 带参数装饰器测试 ===")
print("重复打招呼 3 次:")
say_hello("Alice")
say_hello("Bob")
say_hello("Charlie")


print("\n=== 8. 多装饰器叠加测试 ===")
print(f"greet_person('World') = {greet_person('World')}")


print("\n=== 9. 输入验证测试 ===")
try:
    user1 = User("Alice", 25)
    print(f"注册用户: {register_user(user1)}")
except Exception as e:
    print(f"错误: {e}")

try:
    user2 = User("Bob", 200)
    print(f"注册用户: {register_user(user2)}")
except Exception as e:
    print(f"错误: {e}")
