# Lesson 9.3 - 异步编程
# ★★ 核心概念，Python 异步编程

"""
异步编程（Async Programming）使用事件循环实现并发。
本文档涵盖：
1. async/await 基础语法
2. 事件循环（Event Loop）
3. asyncio.gather - 并发执行
4. asyncio 任务
5. 异步 HTTP（aiohttp 简介）
"""

import asyncio
import aiohttp
import time

# ===== 1. async/await 基础语法 =====

"""
async - 定义异步函数
await - 暂停异步函数，等待结果
事件循环 - 调度和执行异步任务
"""

# ===== 1.1 异步函数 =====

print("=== 1. async/await 基础语法 ===")

async def simple_async():
    """简单的异步函数"""
    print("  异步函数开始")
    await asyncio.sleep(1)  # 模拟 I/O 操作
    print("  异步函数完成")
    return "完成"

# 执行异步函数
asyncio.run(simple_async())

# ===== 1.2 协程 vs 线程 =====

"""
协程（Coroutine）是单线程并发
线程是多线程并发
协程性能更高，但受限于单线程
"""

async def coroutine_example():
    """协程示例"""
    print("  协程函数开始")
    await asyncio.sleep(0.5)
    print("  协程函数完成")

print("\n协程执行:")
asyncio.run(coroutine_example())


# ===== 2. 事件循环（Event Loop）=====

"""
事件循环是异步编程的核心
负责调度和执行协程
"""

async def example_event_loop():
    """事件循环示例"""
    print("  事件循环开始")

    # 创建任务
    task1 = asyncio.create_task(simple_async())
    task2 = asyncio.create_task(simple_async())

    # 等待任务完成
    await task1
    await task2

    print("  事件循环结束")

asyncio.run(example_event_loop())


# ===== 3. asyncio.gather - 并发执行 =====

"""
asyncio.gather() 可以并发执行多个协程
等待所有协程完成后返回结果
"""

print("\n=== 3. asyncio.gather - 并发执行 ===")

async def task1():
    """任务1"""
    print("  任务1: 开始")
    await asyncio.sleep(1)
    print("  任务1: 完成")
    return "任务1 完成"

async def task2():
    """任务2"""
    print("  任务2: 开始")
    await asyncio.sleep(0.5)
    print("  任务2: 完成")
    return "任务2 完成"

async def task3():
    """任务3"""
    print("  任务3: 开始")
    await asyncio.sleep(2)
    print("  任务3: 完成")
    return "任务3 完成"

async def concurrent_tasks():
    """并发任务"""
    print("启动并发任务...")

    # 并发执行所有任务
    results = await asyncio.gather(task1(), task2(), task3())

    print(f"任务结果: {results}")

asyncio.run(concurrent_tasks())

# ===== 4. asyncio 任务 =====

"""
asyncio.create_task() 创建任务
任务可以取消、等待
"""

async def example_task():
    """任务示例"""
    print("  任务创建")
    await asyncio.sleep(2)
    print("  任务完成")
    return "完成"

print("\n=== 4. asyncio 任务 ===")

async def task_management():
    """任务管理"""
    print("创建任务...")

    # 创建任务
    task = asyncio.create_task(example_task())

    # 等待任务完成
    await task

    print(f"任务完成: {task.result()}")

asyncio.run(task_management())


# ===== 5. 多个 asyncio 事件循环 =====

"""
可以使用 asyncio.gather 并发运行多个协程
"""

async def task_a():
    """任务 A"""
    print("  任务 A: 开始")
    await asyncio.sleep(0.5)
    print("  任务 A: 完成")
    return "A"

async def task_b():
    """任务 B"""
    print("  任务 B: 开始")
    await asyncio.sleep(0.5)
    print("  任务 B: 完成")
    return "B"

async def task_c():
    """任务 C"""
    print("  任务 C: 开始")
    await asyncio.sleep(0.5)
    print("  任务 C: 完成")
    return "C"

async def example_multiple():
    """多个协程"""
    print("多个协程:")

    # 并发运行多个协程
    results = await asyncio.gather(task_a(), task_b(), task_c())

    print(f"结果: {results}")

asyncio.run(example_multiple())


# ===== 6. 异步上下文管理器 =====

"""
async with 语句用于异步上下文管理器
"""

class AsyncContextManager:
    """异步上下文管理器"""

    def __init__(self):
        print("初始化")

    async def __aenter__(self):
        print("进入上下文")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("退出上下文")
        return False

print("\n=== 6. 异步上下文管理器 ===")

async def context_example():
    """上下文管理器示例"""
    async with AsyncContextManager() as manager:
        print("  上下文内")
        await asyncio.sleep(0.5)
        print("  上下文内继续")

asyncio.run(context_example())


# ===== 7. 错误处理 =====

"""
异步函数中的错误处理
使用 try/except/finally
"""

async def failing_task():
    """会失败的异步任务"""
    print("  任务: 开始")
    await asyncio.sleep(0.5)
    raise ValueError("模拟错误")
    print("  任务: 完成")  # 不会执行

async def handle_errors():
    """处理错误"""
    print("启动任务...")

    try:
        await failing_task()
    except ValueError as e:
        print(f"捕获错误: {e}")

asyncio.run(handle_errors())

# ===== 8. 超时控制 =====

"""
使用 asyncio.wait_for() 设置超时
超时后抛出 TimeoutError
"""

async def long_running_task():
    """长时间运行的任务"""
    print("  长时间任务: 开始")
    await asyncio.sleep(5)  # 5秒
    print("  长时间任务: 完成")
    return "完成"

print("\n=== 8. 超时控制 ===")

async def with_timeout():
    """带超时的任务"""
    print("启动带超时的任务...")

    try:
        result = await asyncio.wait_for(long_running_task(), timeout=2)  # 2秒超时
        print(f"结果: {result}")
    except asyncio.TimeoutError:
        print("任务超时！")

asyncio.run(with_timeout())

# ===== 9. 偏函数（partial）=====

"""
使用 functools.partial 创建偏函数
可以简化异步任务调用
"""

from functools import partial

print("\n=== 9. 偏函数 =====")

async def task(name, count):
    """任务函数"""
    print(f"  {name}: 开始")
    await asyncio.sleep(1)
    print(f"  {name}: 完成 ({count} 次)")
    return f"{name} 完成 ({count} 次)"

async def task_example():
    """任务示例"""
    print("任务1: 三次")
    await task("任务1", 3)

    print("\n任务2: 五次")
    await task("任务2", 5)

    print("\n任务3: 七次")
    await task("任务3", 7)

asyncio.run(task_example())

# 使用偏函数简化任务调用
async def task_partial_example():
    """偏函数示例"""
    print("简化任务调用...")

    # 创建偏函数
    task1 = partial(task, "任务1")
    task2 = partial(task, "任务2")
    task3 = partial(task, "任务3")

    # 并发执行
    results = await asyncio.gather(
        task1(5),
        task2(10),
        task3(15)
    )

    print(f"结果: {results}")

asyncio.run(task_partial_example())


# ===== 10. 实战应用 - 异步并发下载 =====

class AsyncDownloader:
    """异步下载器"""

    def __init__(self, max_concurrent=5):
        """初始化下载器"""
        self.max_concurrent = max_concurrent

    async def download_file(self, url, filename):
        """下载文件"""
        print(f"  开始下载: {filename}")
        await asyncio.sleep(1)  # 模拟下载
        print(f"  完成下载: {filename}")
        return f"下载完成: {filename}"

    async def download_files(self, urls):
        """并发下载多个文件"""
        print(f"并发下载 {len(urls)} 个文件...")

        async with aiohttp.ClientSession() as session:
            tasks = []
            for url, filename in zip(urls, urls):
                task = asyncio.create_task(self.download_file(url, filename))
                tasks.append(task)

                # 限制并发数
                if len(tasks) >= self.max_concurrent:
                    await asyncio.gather(*tasks)
                    tasks = []

            # 处理剩余的任务
            if tasks:
                await asyncio.gather(*tasks)

        print("所有文件下载完成！")


# 测试异步下载器
urls = [
    "http://example.com/file1.txt",
    "http://example.com/file2.txt",
    "http://example.com/file3.txt",
    "http://example.com/file4.txt",
    "http://example.com/file5.txt",
    "http://example.com/file6.txt",
    "http://example.com/file7.txt",
    "http://example.com/file8.txt",
    "http://example.com/file9.txt",
    "http://example.com/file10.txt"
]

print("\n=== 10. 实战应用 - 异步下载 ===")

downloader = AsyncDownloader(max_concurrent=3)
asyncio.run(downloader.download_files(urls))


# ===== 11. asyncio 与多线程对比 =====

"""
异步编程优势：
- 适合 I/O 密集型任务
- 资源占用更少
- 更好的并发性能
- 无需锁同步

劣势：
- 不能利用多核 CPU
- 编程更复杂
- 有限的支持

多线程优势：
- 能利用多核 CPU
- 编程简单
- 兼容性好

劣势：
- GIL 限制性能
- 资源占用高
- 需要锁同步
"""

# ===== 12. 异步编程最佳实践 =====

"""
最佳实践：
1. 适合 I/O 密集型任务
2. 使用 asyncio.gather 并发执行任务
3. 使用 asyncio.create_task 创建任务
4. 使用 try/except 处理错误
5. 使用 asyncio.wait_for 设置超时
6. 避免阻塞事件循环
7. 使用 aiohttp 进行异步 HTTP 请求
8. 限制并发数量
9. 使用异步上下文管理器
10. 捕获所有异常
"""

class AsyncLogger:
    """异步日志记录器"""

    async def log(self, message):
        """异步日志记录"""
        print(f"[{time.strftime('%H:%M:%S')}] {message}")
        await asyncio.sleep(0.1)  # 模拟日志写入

    async def process_logs(self, messages):
        """处理多条日志"""
        tasks = [self.log(msg) for msg in messages]
        await asyncio.gather(*tasks)


# 测试异步日志
async def async_logger_example():
    """异步日志示例"""
    logger = AsyncLogger()

    messages = [
        "应用启动",
        "连接数据库",
        "加载数据",
        "处理请求",
        "关闭连接",
        "应用关闭"
    ]

    await logger.process_logs(messages)

print(f"=== 12. 异步编程最佳实践 ===")
print(f"测试异步日志:")
asyncio.run(async_logger_example())


# ===== 13. 总结 =====

"""
asyncio 异步编程：
- 使用 async/await 语法
- 事件循环调度协程
- 适合 I/O 密集型任务
- 比 GIL 限制下的多线程性能更好
- 并发执行多个任务
- 处理异步 I/O 操作
"""

print("\n=== 13. 总结 ===")
print("asyncio 异步编程关键点:")
print("  1. 使用 async 定义异步函数")
print("  2. 使用 await 暂停异步函数")
print("  3. 使用 asyncio.gather 并发执行")
print("  4. 使用 asyncio.create_task 创建任务")
print("  5. 使用 asyncio.wait_for 设置超时")
print("  6. 使用 try/except 处理错误")
print("  7. 使用 aiohttp 进行异步 HTTP 请求")
print("  8. 使用异步上下文管理器")
