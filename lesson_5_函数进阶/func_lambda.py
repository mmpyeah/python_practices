# Lesson 5.2 - Lambda 匿名函数
# ★ 参数收集：★ 核心概念，函数式编程的基础

"""
Lambda 是 Python 中创建匿名函数的简洁方式。
虽然我们通常用 def 定义函数，但 lambda 在某些场景下更方便。

本文档涵盖：
1. lambda 基本语法
2. map() 函数与 lambda
3. filter() 函数与 lambda
4. sorted() 的 key 参数
5. reduce() 函数（Python 3.6+ 需导入）
"""

# ===== 1. lambda 基本语法 =====

"""
lambda 参数列表: 表达式

lambda 不需要 return，最后一行的值自动返回
"""

# 等价的 def 函数
def add(x, y):
    return x + y

# lambda 版本
add_lambda = lambda x, y: x + y

# 嵌套 lambda
power = lambda x: lambda y: x ** y
square = power(2)  # 即 lambda y: 2**y

# 多个表达式（返回最后一个）
greet = lambda name: f"Hello {name}!" + f" How are you?"

# 带条件判断的 lambda
max_func = lambda a, b: a if a > b else b
is_even = lambda x: x % 2 == 0

# ===== 2. map() 函数与 lambda =====

"""
map(function, iterable)
对每个元素应用函数，返回迭代器
"""

# 简单的数字平方
numbers = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x ** 2, numbers))
print(f"squares = {squares}")  # [1, 4, 9, 16, 25]

# 大写化字符串
words = ["hello", "world", "python"]
upper_words = list(map(lambda s: s.upper(), words))
print(f"upper_words = {upper_words}")  # ['HELLO', 'WORLD', 'PYTHON']

# 多个可迭代对象（对应位置相加）
nums1 = [1, 2, 3]
nums2 = [10, 20, 30]
sum_pairs = list(map(lambda x, y: x + y, nums1, nums2))
print(f"sum_pairs = {sum_pairs}")  # [11, 22, 33]

# ===== 3. filter() 函数与 lambda =====

"""
filter(function, iterable)
过滤元素，只保留返回 True 的项
"""

# 过滤偶数
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(f"even_numbers = {even_numbers}")  # [2, 4]

# 过滤大于3的数字
greater_than_3 = list(filter(lambda x: x > 3, numbers))
print(f"greater_than_3 = {greater_than_3}")  # [4, 5]

# 过滤长单词
short_words = list(filter(lambda s: len(s) < 5, words))
print(f"short_words = {short_words}")  # ['hello', 'world']

# 过滤非空字符串
strings = ["", "hello", "", "world", ""]
non_empty = list(filter(lambda s: s != "", strings))
print(f"non_empty = {non_empty}")  # ['hello', 'world']

# ===== 4. sorted() 的 key 参数 =====

"""
sorted() 可以指定 key 函数，lambda 用于定义排序规则
"""

# 按字符串长度排序
words = ["apple", "banana", "cherry", "date"]
sorted_by_length = sorted(words, key=lambda s: len(s))
print(f"sorted_by_length = {sorted_by_length}")  # ['date', 'apple', 'banana', 'cherry']

# 按数字排序
numbers = [5, 2, 9, 1, 5, 6]
sorted_numbers = sorted(numbers, key=lambda x: x)
print(f"sorted_numbers = {sorted_numbers}")  # [1, 2, 5, 5, 6, 9]

# 按第二个元素排序（元组列表）
pairs = [(1, 3), (2, 1), (3, 2)]
sorted_by_second = sorted(pairs, key=lambda p: p[1])
print(f"sorted_by_second = {sorted_by_second}")  # [(2, 1), (3, 2), (1, 3)]

# 倒序排序
sorted_reverse = sorted(words, key=lambda s: s, reverse=True)
print(f"sorted_reverse = {sorted_reverse}")  # ['world', 'python', 'banana', 'apple']

# ===== 5. reduce() 函数（需从 functools 导入） =====

"""
reduce(function, sequence)
将序列累积为一个值
"""

from functools import reduce

# 累加所有数字
sum_all = reduce(lambda x, y: x + y, numbers)
print(f"sum_all = {sum_all}")  # 28

# 累乘
product = reduce(lambda x, y: x * y, numbers)
print(f"product = {product}")  # 5400

# 找出最大值
max_val = reduce(lambda x, y: x if x > y else y, numbers)
print(f"max_val = {max_val}")  # 9

# 拼接字符串
concat = reduce(lambda x, y: x + "-" + y, ["hello", "world", "python"])
print(f"concat = {concat}")  # hello-world-python

# ===== 6. lambda 与 list/dict/set 推导式对比 =====

# list 推导式（更直观）
squares = [x ** 2 for x in range(5)]

# lambda + map（功能相同但更复杂）
squares_lambda = list(map(lambda x: x ** 2, range(5)))

# filter 推导式
evens = [x for x in range(10) if x % 2 == 0]

# filter 推导式
evens_lambda = list(filter(lambda x: x % 2 == 0, range(10)))

# ===== 7. 实战应用 =====

def transform_data(data, transform_func):
    """
    接受数据和转换函数，返回转换后的列表
    """
    return list(map(transform_func, data))


def filter_logs(logs, condition):
    """
    过滤日志，只保留符合条件的
    """
    return list(filter(condition, logs))


# 字符串格式化
format_phone = lambda s: f"({s[:3]}) {s[3:6]}-{s[6:]}"
print(f"format_phone('13812345678') = {format_phone('13812345678')}")  # (138) 123-4567

# 字典键值转换
convert_to_dict = lambda items: {k.lower(): v for k, v in items.items()}
sample_dict = {'Name': 'Alice', 'Age': 25}
print(f"convert_to_dict = {convert_to_dict(sample_dict)}")  # {'name': 'Alice', 'age': 25}

# 获取前 n 个元素
get_first_n = lambda seq, n: list(seq)[:n]
print(f"get_first_n([1,2,3,4,5], 3) = {get_first_n([1,2,3,4,5], 3)}")  # [1, 2, 3]

# ===== 8. 常用 lambda 模式 =====

# 字符串处理
str_upper = lambda s: s.upper()
str_lower = lambda s: s.lower()
str_reverse = lambda s: s[::-1]
str_capitalize = lambda s: s.capitalize()

# 数字处理
is_positive = lambda x: x > 0
is_negative = lambda x: x < 0
abs_val = lambda x: abs(x)

# 元素判断
is_empty = lambda s: len(s) == 0
is_not_empty = lambda s: len(s) > 0

# 列表操作
sum_list = lambda lst: sum(lst)
count_items = lambda d: len(d)

# ===== 9. 性能考虑 =====

"""
Lambda 比 def 定义函数稍慢（可忽略）
但在性能敏感场景，lambda 的临时性更节省内存
"""

# 小规模数据处理，def 更好理解
def square(x):
    return x ** 2
squares_def = list(map(square, numbers))

# 大规模数据处理，lambda 更简洁
squares_lambda = list(map(lambda x: x ** 2, range(10000)))

print("\n=== 性能对比 ===")
print(f"squares_def = {squares_def}")
print(f"squares_lambda = {squares_lambda}")

# ===== 测试代码 =====

print("\n=== 1. lambda 基本语法 ===")
print(f"add_lambda(3, 4) = {add_lambda(3, 4)}")
print(f"power(2)(3) = {power(2)(3)}")  # 2^3 = 8
print(f"greet('Bob') = {greet('Bob')}")

# ===== 2. map() 测试 =====
print("\n=== 2. map() 测试 ===")
print(f"squares = {squares}")
print(f"upper_words = {upper_words}")
print(f"sum_pairs = {sum_pairs}")

# ===== 3. filter() 测试 =====
print("\n=== 3. filter() 测试 ===")
print(f"even_numbers = {even_numbers}")
print(f"greater_than_3 = {greater_than_3}")
print(f"short_words = {short_words}")

# ===== 4. sorted() 测试 =====
print("\n=== 4. sorted() 测试 ===")
print(f"sorted_by_length = {sorted_by_length}")
print(f"sorted_by_second = {sorted_by_second}")

# ===== 5. reduce() 测试 =====
print("\n=== 5. reduce() 测试 ===")
print(f"sum_all = {sum_all}")
print(f"product = {product}")
print(f"max_val = {max_val}")

# ===== 6. 实战测试 =====
print("\n=== 6. 实战测试 ===")
test_data = ["hello", "world", "python", "code"]
print(f"transform_data = {transform_data(test_data, str.upper)}")

test_logs = [
    {"level": "INFO", "msg": "Server started"},
    {"level": "ERROR", "msg": "Connection failed"},
    {"level": "WARNING", "msg": "Memory usage high"},
]
print(f"filter_logs = {filter_logs(test_logs, lambda log: log['level'] == 'ERROR')}")

# ===== 7. 常用 lambda 模式测试 =====
print("\n=== 7. 常用 lambda 模式测试 ===")
print(f"is_even(4) = {is_even(4)}")
print(f"is_even(5) = {is_even(5)}")
print(f"is_positive(10) = {is_positive(10)}")
print(f"is_positive(-5) = {is_positive(-5)}")
