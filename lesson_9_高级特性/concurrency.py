# Lesson 9.2 - 并发编程
# ★★ 核心概念，Python 多线程和多进程

"""
并发编程可以同时执行多个任务，提高程序性能。
Python 支持两种并发模型：多线程和多进程。
本文档涵盖：
1. threading 多线程
2. multiprocessing 多进程
3. GIL（全局解释器锁）说明
4. 适用场景对比
"""

import threading
import time
import concurrent.futures
import random

# ===== 1. threading 多线程 =====

"""
多线程：在同一个进程中创建多个线程
线程之间共享内存空间，但 GIL 限制性能
"""

# ===== 1.1 基本线程 =====

print("=== 1. threading 多线程 ===")

# 创建线程
def hello_thread(name):
    """线程函数"""
    time.sleep(1)  # 模拟耗时操作
    print(f"你好，{name}！")

# 创建线程对象
t1 = threading.Thread(target=hello_thread, args=("张三",))
t2 = threading.Thread(target=hello_thread, args=("李四",))
t3 = threading.Thread(target=hello_thread, args=("王五",))

# 启动线程
print("启动线程...")
t1.start()
t2.start()
t3.start()

# 等待线程完成
t1.join()
t2.join()
t3.join()
print("所有线程完成！")

# ===== 1.2 线程同步 =====

"""
使用线程锁（Lock）同步线程访问共享资源
"""

print("\n=== 1.2 线程同步 ===")

lock = threading.Lock()
shared_resource = 0

def increment_value():
    """增加共享资源"""
    global shared_resource
    for _ in range(1000000):
        with lock:  # 获取锁
            shared_resource += 1

# 创建多个线程
threads = []
for i in range(10):
    t = threading.Thread(target=increment_value)
    threads.append(t)
    t.start()

# 等待所有线程完成
for t in threads:
    t.join()

print(f"共享资源: {shared_resource} (预期: 10000000)")

# ===== 1.3 线程通信 =====

"""
使用 threading.Event 实现线程间通信
"""

print("\n=== 1.3 线程通信 ===")

event = threading.Event()
print("事件已创建")

# 线程1：等待事件
def wait_for_event():
    print("线程1：等待事件...")
    event.wait()
    print("线程1：事件被触发！")

# 线程2：设置事件
def set_event():
    time.sleep(2)
    print("线程2：设置事件")
    event.set()

# 启动线程
t1 = threading.Thread(target=wait_for_event)
t2 = threading.Thread(target=set_event)

t1.start()
t2.start()

t1.join()
t2.join()

# ===== 1.4 线程局部数据 =====

"""
使用 threading.local() 实现线程局部数据
"""

print("\n=== 1.4 线程局部数据 ===")

# 线程局部变量
thread_data = threading.local()
thread_data.value = 0

def update_value(thread_id):
    """更新线程局部变量"""
    thread_data.value = thread_id * 10
    print(f"线程 {thread_id}: value = {thread_data.value}")

# 创建线程
threads = []
for i in range(5):
    t = threading.Thread(target=update_value, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"所有线程完成，当前值: {thread_data.value}")

# ===== 2. multiprocessing 多进程 =====

"""
多进程：创建多个进程
每个进程有独立的内存空间，不受 GIL 限制
"""

# ===== 2.1 基本进程 =====

print("\n=== 2. multiprocessing 多进程 ===")

from multiprocessing import Process

def process_function(name):
    """进程函数"""
    time.sleep(1)
    print(f"进程 {name} 完成")

# 创建进程
p1 = Process(target=process_function, args=("进程1",))
p2 = Process(target=process_function, args=("进程2",))

# 启动进程
print("启动进程...")
p1.start()
p2.start()

# 等待进程完成
p1.join()
p2.join()
print("所有进程完成！")

# ===== 2.2 进程池 =====

"""
使用 ProcessPoolExecutor 管理进程池
自动管理进程创建和销毁
"""

print(f"\n=== 2.2 进程池 ===")

def task(name):
    """任务函数"""
    time.sleep(random.uniform(0.1, 0.5))
    return f"结果 {name}"

# 创建进程池
with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
    # 提交任务
    futures = []
    for i in range(10):
        futures.append(executor.submit(task, f"任务{i}"))

    # 获取结果
    for future in concurrent.futures.as_completed(futures):
        print(f"  {future.result()}")

# ===== 2.3 进程间通信 =====

"""
使用 Queue 进行进程间通信
"""

print("\n=== 2.3 进程间通信 ===")

from multiprocessing import Queue, Process

def producer(q):
    """生产者"""
    for i in range(5):
        q.put(f"消息 {i}")
        print(f"生产者: 放入 {q.qsize()} 个消息")

def consumer(q):
    """消费者"""
    while True:
        try:
            msg = q.get(timeout=1)
            print(f"消费者: 读取 {msg}")
            q.task_done()
        except Exception as e:
            print(f"消费者: {e}")
            break

# 创建队列
q = Queue()

# 启动进程
p1 = Process(target=producer, args=(q,))
p2 = Process(target=consumer, args=(q,))

p1.start()
p2.start()

p1.join()
p2.join()

# ===== 3. GIL（全局解释器锁）=====

"""
GIL 是 Python 解释器的锁
每次只能执行一个线程执行 Python 字节码
影响多线程的性能
"""

print("\n=== 3. GIL（全局解释器锁）===")

print("GIL 特性:")
print("  - Python 每次只能执行一个线程的字节码")
print("  - 多线程在 CPU 密集型任务中性能受限")
print("  - I/O 密集型任务可以受益于多线程")
print("  - 多进程不受 GIL 限制")

# ===== 4. 适用场景对比 =====

"""
多线程适合：
- I/O 密集型任务（网络请求、文件操作）
- 需要共享内存的场景
- 线程数量较少的场景

多进程适合：
- CPU 密集型任务（计算密集型）
- 需要充分利用多核 CPU
- 线程数量较多的场景
"""

# ===== 4.1 I/O 密集型任务 - 多线程 =====

print("\n=== 4. 适用场景对比 ===")

# 多线程处理 I/O 任务
def io_task(thread_id):
    """I/O 任务"""
    print(f"线程 {thread_id}: 开始 I/O")
    time.sleep(2)  # 模拟 I/O 操作
    print(f"线程 {thread_id}: 完成 I/O")

print("多线程处理 I/O 任务:")

start_time = time.time()

threads = []
for i in range(3):
    t = threading.Thread(target=io_task, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

elapsed = time.time() - start_time
print(f"总耗时: {elapsed:.2f} 秒")

# ===== 4.2 CPU 密集型任务 - 多进程 =====

print(f"\n多进程处理 CPU 密集型任务:")

start_time = time.time()

with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
    futures = []
    for i in range(10):
        futures.append(executor.submit(lambda: sum(range(1000000))))

    for future in concurrent.futures.as_completed(futures):
        future.result()

elapsed = time.time() - start_time
print(f"总耗时: {elapsed:.2f} 秒")

# ===== 5. 线程安全集合 =====

"""
使用 threading 的线程安全集合
"""

from threading import ThreadSafeDict, ThreadSafeList

print("\n=== 5. 线程安全集合 ===")

# 线程安全字典
safe_dict = ThreadSafeDict()
safe_dict["key1"] = "value1"
safe_dict["key2"] = "value2"

def thread_safe_put(key, value):
    """线程安全写入"""
    safe_dict[key] = value

def thread_safe_get(key):
    """线程安全读取"""
    return safe_dict.get(key)

# 创建线程写入
threads = []
for i in range(3):
    t = Thread(target=thread_safe_put, args=(f"key{i}", f"value{i}"))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"字典内容: {dict(safe_dict)}")

# ===== 6. 实战应用 - 并发下载 =====

class DownloadManager:
    """并发下载管理器"""

    def __init__(self, max_threads=4):
        """初始化下载管理器"""
        self.max_threads = max_threads

    def download_file(self, url, filename):
        """下载文件"""
        print(f"开始下载: {url} -> {filename}")
        time.sleep(1)  # 模拟下载
        print(f"完成下载: {filename}")
        return f"下载完成: {filename}"

    def download_files(self, urls, filenames):
        """并发下载多个文件"""
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            # 提交下载任务
            futures = []
            for url, filename in zip(urls, filenames):
                futures.append(executor.submit(self.download_file, url, filename))

            # 等待所有下载完成
            for future in concurrent.futures.as_completed(futures):
                print(f"  {future.result()}")


# 测试下载管理器
manager = DownloadManager(max_threads=4)

urls = [
    "http://example.com/file1.txt",
    "http://example.com/file2.txt",
    "http://example.com/file3.txt",
    "http://example.com/file4.txt",
    "http://example.com/file5.txt"
]

filenames = [f"downloaded_{i}.txt" for i in range(5)]

print(f"=== 6. 实战应用 - 并发下载 ===")
manager.download_files(urls, filenames)

# ===== 7. 并发控制 =====

"""
使用 concurrent.futures ThreadPoolExecutor 控制并发
"""

def concurrent_task(task_id):
    """并发任务"""
    print(f"任务 {task_id}: 开始")
    time.sleep(2)
    print(f"任务 {task_id}: 完成")
    return task_id

print("\n=== 7. 并发控制 ===")

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    # 提交任务
    futures = [executor.submit(concurrent_task, i) for i in range(6)]

    # 并发执行
    for future in concurrent.futures.as_completed(futures):
        print(f"  {future.result()} 完成")

# ===== 8. 性能对比 =====

"""
对比多线程和多进程的性能
"""

import multiprocessing as mp

def cpu_intensive_function(n):
    """CPU 密集型函数"""
    result = 0
    for i in range(n):
        result += i
    return result

def run_concurrent():
    """运行并发任务"""
    # 多线程
    print("多线程:")
    start = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(cpu_intensive_function, 1000000) for _ in range(4)]
        for future in concurrent.futures.as_completed(futures):
            future.result()

    elapsed = time.time() - start
    print(f"  耗时: {elapsed:.2f} 秒")

    # 多进程
    print("多进程:")
    start = time.time()

    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(cpu_intensive_function, 1000000) for _ in range(4)]
        for future in concurrent.futures.as_completed(futures):
            future.result()

    elapsed = time.time() - start
    print(f"  耗时: {elapsed:.2f} 秒")


# 运行性能对比
# print(f"=== 8. 性能对比 ===")
# run_concurrent()


# ===== 9. 并发编程最佳实践 =====

"""
最佳实践：
1. I/O 密集型任务使用多线程
2. CPU 密集型任务使用多进程
3. 使用线程锁同步共享资源
4. 使用线程池管理线程
5. 使用进程池管理进程
6. 避免过多线程（避免上下文切换开销）
7. 使用线程安全的数据结构
8. 避免全局变量，使用局部变量
"""

# 并发编程最佳实践示例
def concurrent_logger():
    """并发日志记录"""
    def log_message(msg):
        """日志函数"""
        time.sleep(0.1)  # 模拟日志写入
        print(f"[{time.strftime('%H:%M:%S')}] {msg}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        messages = [f"日志消息 {i}" for i in range(10)]
        for future in executor.map(log_message, messages):
            pass

print(f"\n=== 9. 并发编程最佳实践 ===")
print(f"测试并发日志:")
concurrent_logger()
