# Lesson 9.4 - 函数工具库
# ★★ 核心概念，Python 函数式编程工具

"""
functools 和 itertools 是 Python 的标准库工具
本文档涵盖：
1. functools: lru_cache、partial、reduce
2. itertools: chain、product、groupby
"""

from functools import lru_cache, partial, reduce, wraps
import itertools

# ===== 1. functools - 缓存装饰器 =====

"""
lru_cache - 最近最少使用缓存
缓存函数调用结果，提高性能
"""

# ===== 1.1 lru_cache =====

print("=== 1. functools - lru_cache ===")

# 缓存函数调用结果
@lru_cache(maxsize=None)  # 无限缓存
def fibonacci(n):
    """计算斐波那契数列"""
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(f"计算斐波那契数列:")
for i in range(10):
    print(f"  fibonacci({i}) = {fibonacci(i)}")

# 验证缓存
print(f"\nfibonacci(10) = {fibonacci(10)}")
print(f"fibonacci(10) = {fibonacci(10)}")
print(f"fibonacci(10) = {fibonacci(10)}")
print(f"fibonacci(10) = {fibonacci(10)}")

print(f"\n缓存统计:")
print(f"  调用次数: {fibonacci.cache_info().hits}/{fibonacci.cache_info().misses}")

# 清除缓存
fibonacci.cache_clear()
print(f"\n清除缓存")
print(f"fibonacci.cache_info(): {fibonacci.cache_info()}")


# ===== 1.2 lru_cache 最佳实践 =====

"""
使用 lru_cache 优化性能
缓存无副作用的纯函数
避免缓存有副作用的函数
"""

@lru_cache(maxsize=128)
def expensive_computation(n):
    """昂贵的计算"""
    # 模拟昂贵的计算
    import time
    time.sleep(0.01)
    return n * n

print(f"\n=== 1.2 lru_cache 最佳实践 ===")

print(f"多次调用 expensive_computation:")
for i in range(5):
    result = expensive_computation(i)
    print(f"  expensive_computation({i}) = {result}")

print(f"\nlru_cache 统计:")
print(f"  调用: {expensive_computation.cache_info().hits} 次命中, {expensive_computation.cache_info().misses} 次未命中")

# ===== 2. functools - partial 偏函数 =====

"""
partial - 固定函数参数，创建新函数
"""

# ===== 2.1 partial 基础 =====

print("\n=== 2. functools - partial ===")

from functools import partial

def greet(name, greeting="Hello", age=None):
    """问候函数"""
    message = f"{greeting}, {name}"
    if age:
        message += f"！你{age}岁了"
    return message

# 创建偏函数
greet_hi = partial(greet, greeting="Hi")
greet_hi_25 = partial(greet, greeting="Hi", age=25)

print(f"partial 函数示例:")
print(f"  greet_hi('张三') = {greet_hi('张三')}")
print(f"  greet_hi_25('李四') = {greet_hi_25('李四')}")

# ===== 2.2 partial 应用 =====

print(f"\n=== 2.2 partial 应用 ===")

def calculate(a, b, operation="+"):
    """计算"""
    operations = {
        "+": lambda x, y: x + y,
        "-": lambda x, y: x - y,
        "*": lambda x, y: x * y,
        "/": lambda x, y: x / y
    }

    if operation not in operations:
        raise ValueError(f"未知操作: {operation}")

    return operations[operation](a, b)

# 使用 partial 创建特定的计算函数
add = partial(calculate, operation="+")
subtract = partial(calculate, operation="-")
multiply = partial(calculate, operation="*")

print(f"计算示例:")
print(f"  add(5, 3) = {add(5, 3)}")
print(f"  subtract(10, 4) = {subtract(10, 4)}")
print(f"  multiply(6, 7) = {multiply(6, 7)}")

# ===== 2.3 partial 与内置函数 =====

print(f"\n=== 2.3 partial 与内置函数 ===")

# 使用 partial 调整内置函数
def custom_format(template, *args):
    """自定义格式化"""
    return template.format(*args)

# 创建格式化函数
date_format = partial(custom_format, "{year}-{month:02d}-{day:02d}")
print(f"  日期格式化: {date_format(year=2024, month=1, day=15)}")

# functools.wraps - 保留元信息
def decorator(func):
    """装饰器"""
    @wraps(func)  # 保留原始函数的元信息
    def wrapper(*args, **kwargs):
        print(f"调用函数: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@decorator
def my_function():
    """我的函数"""
    return "完成"

print(f"\nmy_function 的元信息:")
print(f"  __name__: {my_function.__name__}")
print(f"  __doc__: {my_function.__doc__}")
print(f"  my_function() = {my_function()}")


# ===== 3. functools - reduce =====

"""
reduce - 将序列 reduce 成单个值
从 functools 导入
"""

# ===== 3.1 reduce 基础 =====

print("\n=== 3. functools - reduce ===")

from functools import reduce

def reduce_example():
    """reduce 示例"""
    # 计算列表元素之和
    numbers = [1, 2, 3, 4, 5]
    result = reduce(lambda x, y: x + y, numbers)
    print(f"计算列表和: {numbers} = {result}")

    # 计算列表积
    result = reduce(lambda x, y: x * y, numbers)
    print(f"计算列表积: {numbers} = {result}")

    # 计算最大值
    result = reduce(lambda x, y: x if x > y else y, numbers)
    print(f"计算最大值: {numbers} = {result}")

    # 计算最小值
    result = reduce(lambda x, y: x if x < y else y, numbers)
    print(f"计算最小值: {numbers} = {result}")

reduce_example()

# ===== 3.2 reduce 应用 =====

print(f"\n=== 3.2 reduce 应用 ===")

# 连接字符串
words = ["Python", " ", "is", " ", "awesome"]
result = reduce(lambda x, y: x + y, words)
print(f"连接字符串: {result}")

# 统计字符出现次数
chars = "hello world"
char_count = reduce(lambda d, c: {**d, c: d.get(c, 0) + 1}, chars, {})
print(f"字符统计: {char_count}")

# 计算阶乘
def factorial(n):
    """计算阶乘"""
    return reduce(lambda x, y: x * y, range(1, n+1), 1)

print(f"\n阶乘计算:")
for i in range(1, 6):
    print(f"  factorial({i}) = {factorial(i)}")

# ===== 4. itertools - 组合工具 =====

"""
itertools 提供高效的迭代器工具
比列表推导式更节省内存
"""

# ===== 4.1 chain - 链接迭代器 =====

"""
chain - 将多个迭代器链接在一起
"""

print("\n=== 4. itertools - chain ===")

# 链接多个列表
list1 = [1, 2, 3]
list2 = [4, 5, 6]
list3 = [7, 8, 9]

combined = itertools.chain(list1, list2, list3)
print(f"链接多个列表:")
print(f"  {list(combined)}")

# 链接多个迭代器
iter1 = iter([1, 2])
iter2 = iter([3, 4])
iter3 = iter([5, 6])

combined = itertools.chain(iter1, iter2, iter3)
print(f"  {list(combined)}")

# ===== 4.2 product - 笛卡尔积 =====

"""
product - 计算多个可迭代对象的笛卡尔积
"""

print(f"\n=== 4.2 product 笛卡尔积 ===")

# 计算两个集合的笛卡尔积
fruits = ["苹果", "香蕉"]
colors = ["红", "黄", "绿"]

product = itertools.product(fruits, colors)
print(f"水果和颜色的笛卡尔积:")
for fruit, color in product:
    print(f"  {fruit} {color}")

# 计算三个集合的笛卡尔积
letters = ["A", "B"]
numbers = [1, 2, 3]
results = ["成功", "失败"]

product = itertools.product(letters, numbers, results)
print(f"\n笛卡尔积示例:")
for item in product:
    print(f"  {item}")

# ===== 4.3 groupby - 分组 =====

"""
groupby - 分组连续相同的元素
"""

print(f"\n=== 4.3 groupby 分组 ===")

# 按奇偶分组
numbers = [1, 3, 5, 2, 4, 6]

# 按奇偶分组
def odd_even(x):
    return x % 2 == 0

grouped = itertools.groupby(numbers, odd_even)
print(f"按奇偶分组: {numbers}")
for key, group in grouped:
    print(f"  {key} ({'偶数' if key else '奇数'}): {list(group)}")

# 按首字母分组
words = ["apple", "apricot", "banana", "berry", "cherry", "date"]

def group_by_first_letter(word):
    return word[0]

grouped = itertools.groupby(sorted(words), group_by_first_letter)
print(f"\n按首字母分组: {sorted(words)}")
for key, group in grouped:
    print(f"  {key}: {list(group)}")

# ===== 4.4 其他 itertools 工具 =====

print(f"\n=== 4.4 其他 itertools 工具 ===")

# count - 无限计数
counter = itertools.count(start=0, step=1)
print(f"无限计数 (前10个):")
for i in itertools.islice(counter, 10):
    print(f"  {i}")

# cycle - 无限循环
cycler = itertools.cycle([1, 2, 3])
print(f"\n无限循环 (前10个):")
for i in itertools.islice(cycler, 10):
    print(f"  {i}")

# repeat - 重复元素
repeater = itertools.repeat("hello", 5)
print(f"\n重复元素:")
print(f"  {list(repeater)}")

# takewhile - 条件获取
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
filtered = itertools.takewhile(lambda x: x < 6, numbers)
print(f"\ takewhile 条件获取 (x < 6):")
print(f"  {list(filtered)}")

# dropwhile - 条件跳过
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
filtered = itertools.dropwhile(lambda x: x < 6, numbers)
print(f"\n dropwhile 条件跳过 (x < 6):")
print(f"  {list(filtered)}")

# islice - 切片
numbers = range(10)
sliced = itertools.islice(numbers, 3, 7)  # 从3开始，到7-1
print(f"\n islice 切片 (3:7):")
print(f"  {list(sliced)}")

# ===== 5. 实战应用 - 排序 =====

class Sorter:
    """排序器"""

    @staticmethod
    def sort_by_key(data, key_func):
        """使用 key_func 排序"""
        return sorted(data, key=key_func)

    @staticmethod
    def sort_by_value(data, key_func):
        """按 value 排序"""
        return sorted(data, key=lambda d: d.get(key_func))

# 测试排序器
print(f"\n=== 5. 实战应用 - 排序 ===")

data = [
    {"name": "张三", "score": 85},
    {"name": "李四", "score": 92},
    {"name": "王五", "score": 78}
]

# 按名字排序
sorted_by_name = Sorter.sort_by_key(data, lambda x: x["name"])
print(f"按名字排序:")
for item in sorted_by_name:
    print(f"  {item}")

# 按分数排序
sorted_by_score = Sorter.sort_by_value(data, "score")
print(f"\n按分数排序:")
for item in sorted_by_score:
    print(f"  {item}")


# ===== 6. 函数式编程最佳实践 =====

"""
最佳实践：
1. 使用 lru_cache 缓存纯函数
2. 使用 partial 固定函数参数
3. 使用 reduce 进行聚合操作
4. 使用 itertools 代替列表推导式（节省内存）
5. 使用 chain 链接多个迭代器
6. 使用 product 计算笛卡尔积
7. 使用 groupby 进行分组
8. 选择适合场景的工具
"""

def process_data(numbers):
    """处理数据"""
    # 使用 reduce 聚合
    total = reduce(lambda x, y: x + y, numbers, 0)
    avg = total / len(numbers)
    max_val = reduce(lambda x, y: x if x > y else y, numbers)

    return {
        "总数": len(numbers),
        "和": total,
        "平均值": avg,
        "最大值": max_val
    }

print(f"\n=== 6. 函数式编程最佳实践 ===")

# 测试处理函数
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
result = process_data(numbers)
print(f"处理结果: {result}")


# ===== 7. 性能对比 =====

"""
functools 和 itertools 是惰性求值的
比列表推导式更节省内存

列表推导式 - 立即生成列表
生成器表达式 - 惰性求值
itertools - 惰性求值
"""

def process_data_expressions():
    """使用表达式处理数据"""

    # 列表推导式
    def list_comprehension():
        numbers = [i for i in range(1000000)]
        return sum(numbers)

    # 生成器表达式
    def generator_expression():
        numbers = sum(i for i in range(1000000))
        return numbers

    # itertools
    def itertools_version():
        numbers = sum(itertools.islice(itertools.count(), 1000000))
        return numbers

    import time

    print("性能对比:")
    print("  列表推导式:")
    start = time.time()
    result1 = list_comprehension()
    elapsed1 = time.time() - start
    print(f"    耗时: {elapsed1:.2f} 秒")

    print("  生成器表达式:")
    start = time.time()
    result2 = generator_expression()
    elapsed2 = time.time() - start
    print(f"    耗时: {elapsed2:.2f} 秒")

    print("  itertools:")
    start = time.time()
    result3 = itertools_version()
    elapsed3 = time.time() - start
    print(f"    耗时: {elapsed3:.2f} 秒")


# 运行性能对比
# print(f"\n=== 7. 性能对比 ===")
# process_data_expressions()


# ===== 8. 总结 =====

"""
functools 工具：
- lru_cache: 缓存函数调用结果
- partial: 固定函数参数
- reduce: 将序列 reduce 成单个值

itertools 工具：
- chain: 链接多个迭代器
- product: 计算笛卡尔积
- groupby: 分组连续元素
- count: 无限计数
- cycle: 无限循环
- repeat: 重复元素
- takewhile: 条件获取
- dropwhile: 条件跳过
- islice: 切片
"""

print("\n=== 8. 总结 ===")
print("functools 工具:")
print("  - lru_cache: 缓存函数")
print("  - partial: 固定参数")
print("  - reduce: 聚合操作")

print("\nitertools 工具:")
print("  - chain: 链接迭代器")
print("  - product: 笛卡尔积")
print("  - groupby: 分组")
print("  - count/cycle/repeat: 无限迭代")
print("  - takewhile/dropwhile: 过滤")
print("  - islice: 切片")
