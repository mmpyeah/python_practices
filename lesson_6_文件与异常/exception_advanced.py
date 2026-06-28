# Lesson 6.5 - 异常处理高级
# ★★★ 核心概念，Python 程序健壮性的进阶技巧

"""
高级异常处理涉及更复杂的场景和工具。
本文档涵盖：
1. contextlib 上下文管理器
2. 自定义协议
3. 资源安全释放实战
4. 上下文变量（Python 3.7+）
5. 带异常上下文管理器的装饰器
"""

import os
import time
import traceback
from contextlib import contextmanager, ExitStack
import threading
import logging

# ===== 1. contextlib 上下文管理器 =====

"""
contextlib 提供了多种上下文管理器的实现方式
比自定义类更简洁
"""

# ===== 1.1 @contextmanager 装饰器 =====

"""
@contextmanager 定义简单的上下文管理器
使用 yield 关键字标记资源的入口和退出
"""

@contextmanager
def timer_context(name="操作"):
    """计时上下文管理器"""
    start_time = time.time()
    print(f"[开始] {name}")

    try:
        yield  # 执行需要计时的代码
        end_time = time.time()
        elapsed = end_time - start_time
        print(f"[完成] {name} (耗时 {elapsed:.4f} 秒)")
    except Exception as e:
        end_time = time.time()
        elapsed = end_time - start_time
        print(f"[失败] {name} (耗时 {elapsed:.4f} 秒)")
        raise


def process_with_timer():
    """使用计时器"""
    with timer_context("文件读取"):
        time.sleep(0.1)
        print("  读取文件完成")

    with timer_context("数据处理"):
        time.sleep(0.05)
        print("  数据处理完成")


# ===== 1.2 重定向输出 =====

"""
重定向 stdout 和 stderr 到文件或自定义流
"""

@contextmanager
def redirect_stdout(filename):
    """重定向标准输出到文件"""
    original_stdout = sys.stdout
    try:
        with open(filename, 'w') as f:
            sys.stdout = f
            yield
    finally:
        sys.stdout = original_stdout
        print(f"已重定向输出到 {filename}")


@contextmanager
def redirect_stderr_to_stdout():
    """重定向标准错误到标准输出"""
    original_stderr = sys.stderr
    try:
        sys.stderr = sys.stdout
        yield
    finally:
        sys.stderr = original_stderr


def log_function_with_redirect():
    """使用重定向的函数"""
    print("这条消息将写入文件")
    print("另一条消息", file=sys.stderr)  # 这条消息会写入 stdout


# ===== 1.3 多资源管理 =====

"""
使用 ExitStack 同时管理多个上下文管理器
"""

@contextmanager
def managed_resources(*resources):
    """同时管理多个资源"""
    stack = ExitStack()

    # 进入所有资源
    for resource in resources:
        stack.enter_context(resource)

    try:
        yield  # 执行需要管理的代码
    finally:
        # 退出所有资源（自动关闭）
        stack.close()


# ===== 2. with 自定义协议 =====

"""
自定义 __enter__ 和 __exit__ 方法实现上下文管理器
"""

class DatabaseConnection:
    """自定义数据库连接类"""

    def __init__(self, host, database):
        self.host = host
        self.database = database
        self.connection = None

    def __enter__(self):
        """进入上下文，建立连接"""
        print(f"连接到数据库: {self.host}/{self.database}")
        # 模拟连接
        self.connection = f"数据库连接对象"
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文，关闭连接"""
        if self.connection:
            print(f"关闭数据库连接: {self.database}")
            self.connection = None
            if exc_type:
                print(f"连接出错: {exc_val}")
                return False  # 不抑制异常
        return True

    def query(self, sql):
        """执行查询"""
        print(f"执行查询: {sql}")
        return f"查询结果: {sql}"


def use_database_connection():
    """使用自定义数据库连接"""
    try:
        with DatabaseConnection("localhost", "mydb") as db:
            result = db.query("SELECT * FROM users")
            print(f"查询结果: {result}")
    except Exception as e:
        print(f"数据库操作失败: {e}")


class FileHandler:
    """文件处理器"""

    def __init__(self, filename, mode='r'):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        """打开文件"""
        self.file = open(self.filename, self.mode, encoding='utf-8')
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        """关闭文件"""
        if self.file:
            self.file.close()
            print(f"文件 {self.filename} 已关闭")


def use_file_handler():
    """使用文件处理器"""
    try:
        with FileHandler("test.txt", 'w') as f:
            f.write("测试内容\n")
            f.write("更多内容\n")
            # 如果这里抛出异常，文件仍然会被关闭
            # raise ValueError("测试异常")
    except Exception as e:
        print(f"操作失败: {e}")


# ===== 3. 资源安全释放实战 =====

"""
确保资源（文件、数据库连接、网络连接等）总是被正确关闭
"""

class SafeResourceManager:
    """安全的资源管理器"""

    def __init__(self, resource_type, resource_id):
        self.resource_type = resource_type
        self.resource_id = resource_id
        self.resource = None
        self.closed = False

    def __enter__(self):
        """初始化资源"""
        print(f"初始化 {self.resource_type} {self.resource_id}")
        self.resource = f"{self.resource_type}_{self.resource_id}"
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """清理资源"""
        if not self.closed and self.resource:
            print(f"清理 {self.resource_type} {self.resource_id}")
            self.resource = None
            self.closed = True

        # 返回 False 表示不抑制异常
        # 返回 True 表示抑制异常
        return False


def multiple_resource_cleanup():
    """多个资源的安全清理"""
    resources = []

    try:
        # 创建多个资源
        db = SafeResourceManager("数据库", "conn1")
        files = [SafeResourceManager("文件", f"file{i}") for i in range(3)]
        resources.extend(files)

        # 进入上下文
        with db:
            with managed_resources(*files):
                # 执行操作
                print("执行操作...")
                # 模拟异常
                raise RuntimeError("操作失败")

    except Exception as e:
        print(f"捕获异常: {e}")

    print(f"资源数量: {len(resources)}")
    print(f"已清理: {sum(1 for r in resources if r.closed)}")


# ===== 4. 上下文变量 =====

"""
ContextVar 用于在多线程环境中共享变量
Python 3.7+ 支持
"""

from contextvars import ContextVar

# 定义上下文变量
request_id = ContextVar('request_id', default=None)
user = ContextVar('user', default=None)


def process_request(request_id, user_id):
    """处理请求"""
    # 设置上下文变量
    request_id_var = request_id
    user_var = user_id

    def inner_task():
        """内部任务"""
        req_id = request_id_var.get()
        u = user_var.get()
        print(f"  任务处理中: 请求ID={req_id}, 用户ID={u}")

    # 模拟并发
    task1 = threading.Thread(target=inner_task)
    task2 = threading.Thread(target=inner_task)

    task1.start()
    task2.start()
    task1.join()
    task2.join()


def threaded_processing():
    """线程中的上下文变量处理"""
    print("=== 线程上下文变量 ===")

    # 线程1
    request_id.set("req-001")
    user.set("user-001")
    process_request("req-001", "user-001")

    # 线程2
    request_id.set("req-002")
    user.set("user-002")
    process_request("req-002", "user-002")


# ===== 5. 带异常上下文管理器的装饰器 =====

"""
创建带异常处理的装饰器
"""

def exception_handler(default=None, logger=None):
    """带异常处理的装饰器"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if logger:
                    logger.error(f"函数 {func.__name__} 执行失败: {e}")
                return default
        return wrapper
    return decorator


def log_errors(func):
    """日志记录装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__module__)
        logger.info(f"执行 {func.__name__}")
        try:
            result = func(*args, **kwargs)
            logger.info(f"{func.__name__} 执行成功")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} 执行失败: {e}")
            traceback.print_exc()
            raise
    return wrapper


# ===== 6. 错误恢复机制 =====

"""
实现自动错误恢复机制
"""

class RetryHandler:
    """重试处理器"""

    def __init__(self, max_retries=3, delay=1):
        self.max_retries = max_retries
        self.delay = delay

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            for attempt in range(self.max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == self.max_retries - 1:
                        raise

                    print(f"尝试 {attempt + 1}/{self.max_retries} 失败: {e}")
                    time.sleep(self.delay)
            return None
        return wrapper


@RetryHandler(max_retries=3, delay=0.5)
def unstable_operation():
    """不稳定的操作"""
    import random
    if random.random() < 0.6:  # 60% 概率失败
        raise RuntimeError("操作失败")
    return "成功"


def graceful_error_handling():
    """优雅的错误处理"""
    print("=== 优雅的错误处理 ===")
    result = unstable_operation()
    print(f"结果: {result}")


# ===== 7. 异常上下文管理器实战 =====

"""
综合使用各种异常处理技术
"""

class DatabaseTransaction:
    """数据库事务管理器"""

    def __init__(self, db):
        self.db = db
        self.connection = None

    def __enter__(self):
        """开始事务"""
        print("开始事务")
        self.connection = self.db.connect()
        self.connection.begin()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """提交或回滚事务"""
        if exc_type:
            print(f"事务失败，回滚: {exc_val}")
            self.connection.rollback()
            return False
        else:
            print("事务成功，提交")
            self.connection.commit()
            return True


class FileLogger:
    """文件日志记录器"""

    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        """打开文件"""
        self.file = open(self.filename, 'a', encoding='utf-8')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """写入错误信息"""
        if exc_type:
            error_msg = f"\n[ERROR] {exc_type.__name__}: {exc_val}\n"
            self.file.write(error_msg)
        self.file.close()

    def log(self, message):
        """记录日志"""
        self.file.write(message + '\n')


def complex_error_handling():
    """综合错误处理示例"""

    class Database:
        """模拟数据库"""
        def __init__(self):
            self.connections = []

        def connect(self):
            """连接"""
            conn = f"连接_{len(self.connections)}"
            self.connections.append(conn)
            return conn

        def begin(self):
            """开始事务"""
            print(f"  开始事务")

        def commit(self):
            """提交"""
            print(f"  提交事务")

        def rollback(self):
            """回滚"""
            print(f"  回滚事务")

    db = Database()

    with DatabaseTransaction(db) as tx:
        with FileLogger("error.log") as logger:
            logger.log("开始执行任务")

            # 执行任务
            try:
                # 模拟数据库操作
                conn = tx.connection
                print(f"  使用连接: {conn}")

                # 模拟成功
                print(f"  执行成功")

            except Exception as e:
                logger.log(f"执行失败: {e}")
                raise

            # 也可以在这里显式回滚
            # tx.connection.rollback()


# ===== 8. 异常处理最佳实践总结 =====

"""
最佳实践：
1. 始终使用上下文管理器（with 语句）
2. 捕获特定异常，不要捕获所有异常
3. 使用 finally 进行资源清理
4. 保留异常链信息
5. 自定义异常要继承 Exception
6. 考虑重试机制
7. 记录详细的错误日志
"""

def robust_api_call():
    """健壮的 API 调用示例"""
    from urllib.error import URLError
    import json

    def fetch_data(url):
        """获取数据"""
        try:
            # 模拟网络请求
            time.sleep(0.1)
            return {"status": "success", "data": "test"}

        except URLError as e:
            print(f"网络错误: {e}")
            raise ConnectionError("无法连接到服务器") from e
        except Exception as e:
            print(f"未知错误: {e}")
            raise

    with FileLogger("api_errors.log") as logger:
        try:
            logger.log("开始请求")
            result = fetch_data("http://api.example.com/data")
            logger.log(f"请求成功: {result}")
            return result
        except Exception as e:
            logger.log(f"请求失败: {e}")
            # 可以选择重试或返回默认值
            return {"status": "error", "message": str(e)}


# ===== 测试代码 =====

import sys
import functools

print("\n=== 1. 上下文管理器测试 ===")
process_with_timer()

print("\n=== 2. 自定义协议测试 ===")
use_database_connection()
use_file_handler()

print("\n=== 3. 资源清理测试 ===")
multiple_resource_cleanup()

print("\n=== 4. 上下文变量测试 ===")
threaded_processing()

print("\n=== 5. 错误恢复机制测试 ===")
graceful_error_handling()

print("\n=== 6. 综合错误处理测试 ===")
complex_error_handling()

print("\n=== 7. API 调用测试 ===")
result = robust_api_call()
print(f"API 调用结果: {result}")

# 清理测试文件
if os.path.exists("test.txt"):
    os.remove("test.txt")
if os.path.exists("error.log"):
    os.remove("error.log")
