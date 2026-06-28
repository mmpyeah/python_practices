# Lesson 6.4 - 异常处理基础
# ★★★ 核心概念，Python 程序健壮性的保证

"""
异常处理是 Python 程序健壮性的核心。
本文档涵盖：
1. try/except/else/finally 结构
2. 捕获多个异常
3. 异常链
4. 抛出异常
5. 自定义异常类
6. 异常的常见类型
"""

# ===== 1. try/except 基本结构 =====

"""
try-except-finally 是 Python 异常处理的核心结构
try: 尝试执行的代码
except: 捕获异常
else: 没有异常时执行
finally: 无论是否异常都执行
"""

print("=== 1. try/except 基本结构 ===")

# 简单的 try-except
try:
    result = 10 / 2
    print(f"10 / 2 = {result}")
except ZeroDivisionError:
    print("除数不能为 0")

# 包含 else 和 finally
try:
    number = int(input("请输入一个数字: "))
    result = 100 / number
    print(f"100 / {number} = {result}")
except ZeroDivisionError:
    print("错误：除数不能为 0")
except ValueError:
    print("错误：请输入有效的数字")
except Exception as e:
    print(f"发生未知错误: {e}")
else:
    print("计算成功，没有异常！")
finally:
    print("无论是否异常都会执行这段代码")


# ===== 2. 多个 except 分支 =====

"""
可以捕获多个不同类型的异常
"""

print("\n=== 2. 多个 except 分支 ===")

def process_data(data):
    """处理数据，可以捕获多种异常"""
    try:
        if not isinstance(data, str):
            raise TypeError("输入必须是字符串")

        number = int(data)
        result = 100 / number
        print(f"计算结果: {result}")
        return result

    except TypeError as e:
        print(f"类型错误: {e}")
        return None
    except ValueError as e:
        print(f"值错误: {e}")
        return None
    except ZeroDivisionError as e:
        print(f"除零错误: {e}")
        return None
    except Exception as e:
        print(f"未知错误: {type(e).__name__}: {e}")
        return None


# 测试不同输入
process_data("10")
process_data("abc")
process_data(123)
process_data("0")


# ===== 3. 捕获所有异常 =====

"""
使用 Exception 类捕获所有异常（但不包括 SystemExit、KeyboardInterrupt）
"""

print("\n=== 3. 捕获所有异常 ===")

def safe_divide(a, b):
    """安全的除法"""
    try:
        return a / b
    except Exception as e:
        print(f"发生异常: {type(e).__name__}: {e}")
        return None

print(f"safe_divide(10, 2) = {safe_divide(10, 2)}")
print(f"safe_divide(10, 0) = {safe_divide(10, 0)}")
print(f"safe_divide('10', 2) = {safe_divide('10', 2)}")


# ===== 4. except 中再捕获 =====

"""
可以在 except 块中捕获异常，实现多层捕获
"""

print("\n=== 4. except 中再捕获 ===")

def nested_exception_handling():
    try:
        try:
            # 尝试读取文件
            with open("nonexistent.txt", 'r') as f:
                content = f.read()
        except FileNotFoundError as e:
            print(f"文件不存在: {e}")
            # 尝试创建文件
            try:
                with open("nonexistent.txt", 'w') as f:
                    f.write("测试内容")
                print("文件已创建")
            except PermissionError:
                print("没有文件写入权限")
                return None
        return "成功"
    except Exception as e:
        print(f"捕获到异常: {e}")
        return None


nested_exception_handling()


# ===== 5. 异常链 =====

"""
使用 raise from 保留原始异常信息
"""

print("\n=== 5. 异常链 ===")

class CustomError(Exception):
    """自定义异常"""
    pass

def process_with_retry():
    """带重试机制的函数"""
    try:
        # 第1次尝试
        result = divide_safe(10, 0)
        if result is None:
            # 第2次尝试
            result = divide_safe(10, 0)
            if result is None:
                # 第3次尝试
                result = divide_safe(10, 0)
                if result is None:
                    raise CustomError("重试3次后仍然失败") from None
    except ZeroDivisionError as e:
        print(f"原始异常: {e}")
        print(f"异常类型: {type(e).__name__}")
        print(f"异常位置: {e.__traceback__.tb_frame.f_code.co_filename}:{e.__traceback__.tb_lineno}")

    return result

def divide_safe(a, b):
    """安全的除法"""
    try:
        return a / b
    except ZeroDivisionError as e:
        print(f"除零错误: {e}")
        return None

process_with_retry()


# ===== 6. 抛出异常 =====

"""
使用 raise 抛出异常
可以使用 raise new_exception from old_exception 保留异常链
"""

print("\n=== 6. 抛出异常 ===")

def validate_age(age):
    """验证年龄"""
    if not isinstance(age, int):
        raise TypeError("年龄必须是整数")

    if age < 0:
        raise ValueError("年龄不能为负数")

    if age > 150:
        raise ValueError("年龄不合法")

    return age

try:
    validate_age(-5)
except ValueError as e:
    print(f"验证失败: {e}")

try:
    validate_age(200)
except ValueError as e:
    print(f"验证失败: {e}")

try:
    validate_age("25")
except TypeError as e:
    print(f"验证失败: {e}")

# 自定义异常示例
class FileReadError(Exception):
    """文件读取异常"""
    def __init__(self, filename, reason):
        self.filename = filename
        self.reason = reason
        super().__init__(f"无法读取文件 {filename}: {reason}")

def read_config_file(filename):
    """读取配置文件"""
    try:
        # 模拟文件不存在
        if not os.path.exists(filename):
            raise FileNotFoundError(f"文件 {filename} 不存在")

        # 模拟文件为空
        if os.path.getsize(filename) == 0:
            raise FileReadError(filename, "文件为空")

        # 读取文件
        with open(filename, 'r') as f:
            return f.read()

    except FileNotFoundError as e:
        raise FileReadError(e.filename, "文件不存在") from e
    except PermissionError as e:
        raise FileReadError(filename, "没有读取权限") from e
    except Exception as e:
        raise FileReadError(filename, str(e)) from e

try:
    read_config_file("nonexistent.txt")
except FileReadError as e:
    print(f"自定义异常: {e}")


# ===== 7. 自定义异常类 =====

"""
自定义异常可以让代码更清晰，提供更好的错误信息
"""

print("\n=== 7. 自定义异常类 ===")

# 基础异常
class CustomError(Exception):
    """自定义基础异常"""
    pass

# 特定异常
class DatabaseError(CustomError):
    """数据库相关异常"""
    pass

class ConnectionError(DatabaseError):
    """连接错误"""
    pass

class QueryError(DatabaseError):
    """查询错误"""
    pass

class ValidationError(Exception):
    """数据验证异常"""
    def __init__(self, field, message):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")

def validate_user_data(data):
    """验证用户数据"""
    errors = []

    if 'username' not in data:
        errors.append(ValidationError('username', '缺少用户名'))

    if 'email' not in data:
        errors.append(ValidationError('email', '缺少邮箱'))

    if not isinstance(data.get('age'), int):
        errors.append(ValidationError('age', '年龄必须是整数'))

    if errors:
        raise ValueError("数据验证失败", errors)

    return data

try:
    validate_user_data({'username': 'test'})
except ValueError as e:
    print(f"验证失败: {e}")
    for err in e.args[1]:
        print(f"  - {err}")

try:
    validate_user_data({'username': 'test', 'age': 'twenty'})
except ValueError as e:
    print(f"验证失败: {e}")
    for err in e.args[1]:
        print(f"  - {err}")


# ===== 8. 常见异常类型总结 =====

"""
常见异常类型：
- Exception: 所有异常的基类
- ValueError: 值不合法
- TypeError: 类型错误
- IndexError: 索引越界
- KeyError: 字典键不存在
- ZeroDivisionError: 除零错误
- FileNotFoundError: 文件不存在
- PermissionError: 没有权限
- AttributeError: 属性不存在
- AssertionError: 断言失败
"""

print("\n=== 8. 常见异常类型 ===")

def demonstrate_exceptions():
    """演示常见异常"""
    errors = []

    try:
        # IndexError
        list_ = [1, 2, 3]
        x = list_[10]
    except IndexError as e:
        errors.append(("IndexError", str(e)))

    try:
        # KeyError
        dict_ = {'a': 1}
        x = dict_['b']
    except KeyError as e:
        errors.append(("KeyError", str(e)))

    try:
        # AttributeError
        obj = None
        x = obj.some_method()
    except AttributeError as e:
        errors.append(("AttributeError", str(e)))

    try:
        # TypeError
        x = "abc" + 123
    except TypeError as e:
        errors.append(("TypeError", str(e)))

    for error_type, message in errors:
        print(f"  {error_type}: {message}")


# ===== 9. finally 块 =====

"""
finally 块无论是否发生异常都会执行
常用于资源清理（文件关闭、数据库连接关闭等）
"""

print("\n=== 9. finally 块 ===")

def file_operation_with_cleanup(filename):
    """文件操作 + 资源清理"""

    file = None
    try:
        file = open(filename, 'r')
        content = file.read()
        print(f"读取到内容: {content[:50]}...")
        return content
    except FileNotFoundError:
        print("文件不存在")
        return None
    except Exception as e:
        print(f"读取文件出错: {e}")
        return None
    finally:
        # 无论是否异常都会执行
        if file:
            file.close()
            print("文件已关闭")

file_operation_with_cleanup("test.txt")


def db_operation_with_cleanup():
    """模拟数据库操作 + 资源清理"""

    connection = None
    try:
        # 模拟数据库连接
        connection = "数据库连接对象"
        print("数据库连接成功")

        # 模拟操作
        result = execute_query(connection)
        return result

    except Exception as e:
        print(f"数据库操作失败: {e}")
        return None
    finally:
        if connection:
            # 模拟关闭连接
            connection = None
            print("数据库连接已关闭")


def execute_query(connection):
    """执行查询"""
    # 模拟查询
    return "查询结果"


db_operation_with_cleanup()


# ===== 10. 异常处理最佳实践 =====

"""
1. 捕获特定的异常，不要捕获所有异常（除非必要）
2. 不要捕获异常后什么都不做
3. 使用 finally 块进行资源清理
4. 保留异常链信息（raise from）
5. 自定义异常要继承 Exception
6. 避免过多的异常处理
"""

def robust_function():
    """健壮的函数示例"""
    try:
        # 尝试操作
        result = risky_operation()
        return result

    except SpecificError1:
        # 处理特定错误
        print("处理错误1")
        return None

    except SpecificError2:
        # 处理特定错误
        print("处理错误2")
        return None

    except Exception as e:
        # 处理其他错误
        print(f"未知错误: {e}")
        return None

    finally:
        # 清理资源
        cleanup_resources()


def risky_operation():
    """有风险的操作"""
    if random.random() < 0.3:
        raise SpecificError1("模拟错误1")
    if random.random() < 0.3:
        raise SpecificError2("模拟错误2")
    return "成功"


def cleanup_resources():
    """清理资源"""
    pass


# ===== 测试代码 =====

print("\n=== 10. 测试代码 ===")

# 测试嵌套异常
nested_exception_handling()

# 测试异常链
process_with_retry()

# 测试自定义异常
try:
    read_config_file("nonexistent.txt")
except FileReadError as e:
    print(f"捕获自定义异常: {e}")

# 测试数据验证
try:
    validate_user_data({'username': 'test', 'age': 'twenty'})
except ValueError as e:
    print(f"捕获验证异常: {e}")

# 测试常见异常
demonstrate_exceptions()

# 测试 finally 块
file_operation_with_cleanup("test.txt")

# 清理测试文件
if os.path.exists("nonexistent.txt"):
    os.remove("nonexistent.txt")
