# Lesson 5.4 - 生成器
# ★★★ 核心概念，函数式编程和内存优化的重要特性

"""
生成器是 Python 中强大的工具，用于处理大数据集而不占用大量内存。
生成器通过 yield 关键字实现，可以逐项产生数据。

本文档涵盖：
1. yield 基本概念
2. 生成器函数 vs 普通函数
3. yield from 语法
4. 生成器表达式
5. send/throw/close 方法
6. yield 的不同模式
7. itertools 模块
"""

# ===== 1. yield 基本概念 =====

"""
yield 关键字让函数变成生成器函数
生成器函数不会立即返回，而是返回一个生成器对象
每次调用 next() 时才会计算下一个值
"""

def simple_generator():
    """简单的生成器函数"""
    print("生成器开始")
    yield 1
    print("第一次 yield 后")
    yield 2
    print("第二次 yield 后")
    yield 3
    print("生成器结束")


gen = simple_generator()
print("=== 1. yield 基本测试 ===")
print(f"gen = {gen}")  # <generator object simple_generator at ...>

print("\n获取值:")
print(f"next(gen) = {next(gen)}")  # 1
print(f"next(gen) = {next(gen)}")  # 2
print(f"next(gen) = {next(gen)}")  # 3

try:
    next(gen)  # StopIteration 异常
except StopIteration:
    print("生成器已耗尽")

print("\n使用 for 循环遍历:")
for value in simple_generator():
    print(f"  {value}")


# ===== 2. 生成器 vs 普通函数 =====

def normal_function():
    """普通函数：一次性返回所有值"""
    result = []
    for i in range(1, 6):
        result.append(i)
    return result


def generator_function():
    """生成器函数：逐个产生值"""
    for i in range(1, 6):
        yield i


print("=== 2. 普通函数 vs 生成器 ===")
print(f"normal_function() 返回: {normal_function()}")
print(f"generator_function() 返回: {generator_function()}")

print("\n内存占用对比:")
import sys

data = normal_function()
gen = generator_function()
print(f"普通函数数据大小: {sys.getsizeof(data)} 字节")
print(f"生成器对象大小: {sys.getsizeof(gen)} 字节")
print(f"生成器只保存迭代器状态，不保存所有数据")

# 生成器使用场景：处理大数据集
def read_large_file(filename):
    """模拟读取大文件，逐行处理"""
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            yield line.strip()


# ===== 3. yield from 语法 =====

"""
yield from 用于将生成器委托给其他生成器
"""

def base_generator():
    """基础生成器"""
    yield 1
    yield 2


def extended_generator():
    """扩展生成器，使用 yield from"""
    yield "start"
    yield from base_generator()  # 委托给基础生成器
    yield "end"


print("\n=== 3. yield from 测试 ===")
for value in extended_generator():
    print(f"  {value}")


def combine_generators(*generators):
    """组合多个生成器"""
    for gen in generators:
        yield from gen


print("\n组合多个生成器:")
for value in combine_generators([1, 2], [3, 4], [5, 6]):
    print(f"  {value}")


# ===== 4. 生成器表达式 =====

"""
类似列表推导式，但用 () 而不是 []
返回生成器对象，内存效率高
"""

# 列表推导式
squares = [x ** 2 for x in range(5)]
print(f"列表推导式: {squares}")

# 生成器表达式
squares_gen = (x ** 2 for x in range(5))
print(f"生成器表达式: {squares_gen}")

# 使用
print("遍历生成器表达式:")
for sq in squares_gen:
    print(f"  {sq}")

# 嵌套生成器表达式
nested = (x ** 2 for x in (y ** 2 for y in range(3)))
print(f"嵌套生成器: {list(nested)}")

# 条件过滤
evens = (x for x in range(10) if x % 2 == 0)
print(f"偶数生成器: {list(evens)}")

# 带更多逻辑
transformed = (x * 2 + 1 for x in range(5))
print(f"转换后: {list(transformed)}")


# ===== 5. send/throw/close 方法 =====

"""
生成器除了 next()，还支持：
- send(value): 向生成器发送值（需要 yield 接收）
- throw(exception): 抛出异常给生成器
- close(): 关闭生成器
"""

def accumulator():
    """可累加的生成器"""
    total = 0
    while True:
        value = yield total  # 接收 send 发送的值
        if value is None:
            break
        total += value


print("\n=== 5. 生成器控制方法测试 ===")
acc = accumulator()
print(f"初始值: {next(acc)}")  # 0

print(f"累加 10: {acc.send(10)}")  # 10
print(f"累加 20: {acc.send(20)}")  # 30
print(f"累加 30: {acc.send(30)}")  # 60

acc.close()  # 关闭生成器


def error_generator():
    """会抛出异常的生成器"""
    try:
        while True:
            yield "运行中"
            raise RuntimeError("模拟异常")
    except RuntimeError as e:
        print(f"[GENERATOR] 捕获异常: {e}")


# 异常测试：
# err_gen = error_generator()
# print(f"next(err_gen) = {next(err_gen)}")
# print(f"next(err_gen) = {next(err_gen)}")
# except RuntimeError as e:
#     print(f"外部捕获异常: {e}")
print("\n异常测试：跳过（已注释，避免 StopIteration）")


# ===== 6. yield 的三种模式 =====

"""
yield 可以用于：
1. 简单生成值
2. 接收输入
3. 既是输入又是输出
"""

# 模式1：简单生成
def simple_gen():
    yield 1
    yield 2
    yield 3


# 模式2：接收输入
def counter(start=0):
    while True:
        current = yield start
        if current is not None:
            start = current


# 模式3：双向通信
def chat():
    while True:
        msg = yield
        if msg == "quit":
            return
        yield f"收到: {msg}"


print("\n=== 6. yield 三种模式测试 ===")

# 模式1
print("模式1 - 简单生成:")
for val in simple_gen():
    print(f"  {val}")

# 模式2
print("\n模式2 - 接收输入:")
counter_gen = counter(0)
print(f"初始: {next(counter_gen)}")  # 0
print(f"发送10: {counter_gen.send(10)}")  # 10
print(f"发送20: {counter_gen.send(20)}")  # 20

# 模式3
print("\n模式3 - 双向通信:")
chat_gen = chat()
print(f"初始: {next(chat_gen)}")  # None
print(f"发送'Hello': {chat_gen.send('Hello')}")
print(f"发送'How are you': {chat_gen.send('How are you')}")
print(f"发送'quit': {chat_gen.send('quit')}")  # 退出


# ===== 7. itertools 模块 =====

"""
itertools 是 Python 的标准库模块，提供了大量生成器函数
"""

import itertools

# count() - 无限计数
count_gen = itertools.count(start=10, step=2)
print(f"count: {list(itertools.islice(count_gen, 5))}")

# cycle() - 无限循环
cycle_gen = itertools.cycle(['a', 'b'])
print(f"cycle: {list(itertools.islice(cycle_gen, 6))}")

# repeat() - 重复元素
repeat_gen = itertools.repeat(5, 3)
print(f"repeat: {list(repeat_gen)}")

# chain() - 链接多个可迭代对象
chain_gen = itertools.chain([1, 2], [3, 4], [5, 6])
print(f"chain: {list(chain_gen)}")

# compress() - 过滤
compress_gen = itertools.compress([1, 2, 3, 4, 5], [True, False, True, False, True])
print(f"compress: {list(compress_gen)}")

# islice() - 切片
slice_gen = itertools.islice(range(10), 3, 7)
print(f"islice: {list(slice_gen)}")

# dropwhile() - 跳过满足条件的项
drop_gen = itertools.dropwhile(lambda x: x < 3, range(5))
print(f"dropwhile: {list(drop_gen)}")

# takewhile() - 只取满足条件的项
take_gen = itertools.takewhile(lambda x: x < 4, range(5))
print(f"takewhile: {list(take_gen)}")

# accumulate() - 累积
acc_gen = itertools.accumulate(range(5))
print(f"accumulate: {list(acc_gen)}")

# groupby() - 分组
people = [('Alice', 25), ('Bob', 30), ('Charlie', 25), ('David', 30)]
groups = itertools.groupby(people, key=lambda x: x[1])
print(f"groupby:")
for age, group in groups:
    print(f"  {age}: {list(group)}")


# ===== 8. 实战应用 =====

# 生成器 - 懒加载的大文件读取器
def file_chunk_reader(filename, chunk_size=1024):
    """分块读取文件，节省内存"""
    with open(filename, 'r', encoding='utf-8') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk


# 生成器 - 链式处理数据
def pipeline(*generators):
    """数据管道：链式处理"""
    current = generators[0]
    for gen in generators[1:]:
        current = map(gen, current)
    return current


def process_square(x):
    return x ** 2


def process_double(x):
    return x * 2


def process_add_10(x):
    return x + 10


# 生成器 - 无限斐波那契数列
def fibonacci(n=0):
    """生成斐波那契数列"""
    a, b = 0, 1
    while n == 0 or a < n:
        yield a
        a, b = b, a + b


# 生成器 - 实现简单协程
class Task:
    def __init__(self, func, *args):
        self.func = func
        self.args = args

    def run(self):
        gen = self.func(*self.args)
        try:
            while True:
                yield next(gen)
        except StopIteration:
            return


def printer(msg):
    """简单的协程示例"""
    for i in range(3):
        received = yield f"{msg} {i+1}"
        print(f"  收到: {received}")


# ===== 9. 性能对比 =====

"""
生成器 vs 列表的性能对比
"""

def list_vs_generator(size=1000000):
    """对比列表和生成器的性能"""

    # 创建列表
    start = time.time()
    list_data = [i ** 2 for i in range(size)]
    list_time = time.time() - start
    print(f"创建列表耗时: {list_time:.4f} 秒")

    # 创建生成器
    start = time.time()
    gen_data = (i ** 2 for i in range(size))
    gen_time = time.time() - start
    print(f"创建生成器耗时: {gen_time:.4f} 秒")

    # 内存占用
    import sys
    print(f"列表内存: {sys.getsizeof(list_data) / 1024 / 1024:.2f} MB")
    print(f"生成器内存: {sys.getsizeof(gen_data):.2f} 字节")

    # 迭代性能
    start = time.time()
    for i in list_data:
        pass
    list_iter_time = time.time() - start

    start = time.time()
    for i in gen_data:
        pass
    gen_iter_time = time.time() - start

    print(f"列表迭代耗时: {list_iter_time:.4f} 秒")
    print(f"生成器迭代耗时: {gen_iter_time:.4f} 秒")


# 使用生成器计算大数据集的平方和
def sum_squares_large():
    """处理大数据集的平方和"""
    return sum(i ** 2 for i in range(1000000))


# ===== 测试代码 =====

print("\n=== 7. itertools 模块测试 ===")
print(f"count: {list(itertools.islice(itertools.count(10, 2), 5))}")
print(f"cycle: {list(itertools.islice(itertools.cycle(['a', 'b']), 6))}")
print(f"chain: {list(itertools.chain([1, 2], [3, 4], [5, 6]))}")
print(f"accumulate: {list(itertools.accumulate(range(5)))}")


print("\n=== 8. 实战应用测试 ===")

# 测试斐波那契
print("斐波那契数列前10项:")
for i, fib in enumerate(fibonacci(100), 1):
    print(f"  {i}. {fib}")
    if i >= 10:
        break

# 测试协程
print("\n协程示例:")
task = Task(printer, "Hello")
for result in task.run():
    print(result)


print("\n生成器计算性能:")
import time
start = time.time()
result = sum_squares_large()
elapsed = time.time() - start
print(f"sum_squares_large() = {result}")
print(f"耗时: {elapsed:.4f} 秒")
