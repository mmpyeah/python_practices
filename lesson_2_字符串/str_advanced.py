# 字符串高级技巧
# 本文件覆盖 f-string 高级特性、多行字符串、
# 字符串性能对比和一些运维实用技巧

# ============================================================
# f-string 高级特性（Python 3.6+，推荐写法）
# ============================================================
def fstring_advanced():
    # 基础已在 str_concat.py 覆盖，这里讲进阶用法

    import datetime

    pi = 3.14159265358979

    # 数字格式化
    print(f'{pi:.2f}')          # 3.14       → 保留 2 位小数
    print(f'{pi:10.3f}')        # _____3.142  → 总宽 10，右对齐
    print(f'{pi:<10.3f}')       # 3.142_____  → 左对齐
    print(f'{1234567:,}')       # 1,234,567   → 千位分隔符
    print(f'{0.857:.1%}')       # 85.7%       → 百分比格式
    print(f'{255:#x}')          # 0xff        → 十六进制（带前缀）
    print(f'{255:08b}')         # 11111111    → 8位二进制（补零）
    print(f'{255:08X}')         # 000000FF    → 十六进制大写

    # 日期时间格式化
    now = datetime.datetime(2024, 6, 27, 10, 30, 0)
    print(f'{now:%Y-%m-%d %H:%M:%S}')     # 2024-06-27 10:30:00
    print(f'{now:%Y/%m/%d}')              # 2024/06/27

    # ★ f-string 内直接写表达式
    items = ['apple', 'banana', 'cherry']
    print(f'共 {len(items)} 个水果: {", ".join(items)}')
    print(f'列表反转: {items[::-1]}')

    # ★ = 号调试技巧（Python 3.8+）
    x = 42
    y = x * 2
    print(f'{x=}, {y=}')        # x=42, y=84  → 自动显示变量名和值（调试神器）

    # 嵌套引号
    name = "Alice"
    print(f"{'Hello':>10}")               # _____Hello
    print(f'{name!r}')                    # 'Alice'  → !r 调用 repr()
    print(f'{name!s}')                    # Alice    → !s 调用 str()
    print(f'{name!a}')                    # 'Alice'  → !a 调用 ascii()


# ============================================================
# 多行字符串处理
# ============================================================
def multiline_strings():
    # 三引号多行
    text = """
    第一行
    第二行
    第三行
    """
    print(repr(text))           # 注意首尾有 \n

    # textwrap.dedent → 去掉统一的缩进（模板里常用）
    import textwrap
    sql = textwrap.dedent("""
        SELECT *
        FROM users
        WHERE active = 1
        ORDER BY created_at DESC
    """).strip()
    print(sql)

    # 反斜杠续行（不推荐，难维护）
    long_str = 'This is a very ' \
               'long string that ' \
               'spans multiple lines'
    print(long_str)

    # ★ 推荐：括号内隐式续行
    long_str2 = (
        'This is a very '
        'long string that '
        'spans multiple lines'
    )
    print(long_str2)


# ============================================================
# ★ 字符串性能：大量拼接时用 join 而不是 +
# ============================================================
def performance_tips():
    import time

    n = 50000

    # 方法1：+ 拼接（慢，每次创建新对象）
    t0 = time.time()
    result = ''
    for i in range(n):
        result += str(i)
    t1 = time.time()
    print(f'+ 拼接耗时:   {(t1-t0)*1000:.2f} ms，长度 {len(result)}')

    # 方法2：join（快，一次分配内存）
    t2 = time.time()
    result2 = ''.join(str(i) for i in range(n))
    t3 = time.time()
    print(f'join 耗时:    {(t3-t2)*1000:.2f} ms，长度 {len(result2)}')

    # 方法3：列表预收集再 join（最推荐的循环内拼接写法）
    t4 = time.time()
    parts = []
    for i in range(n):
        parts.append(str(i))
    result3 = ''.join(parts)
    t5 = time.time()
    print(f'list+join 耗时:{(t5-t4)*1000:.2f} ms，长度 {len(result3)}')


# ============================================================
# 实用小技巧汇总
# ============================================================
def practical_tips():
    # 1. 检查字符串包含关系用 in（比 find 更 Pythonic）
    s = 'Hello, Python World'
    print('Python' in s)                # True
    print('Java' not in s)              # True

    # 2. 字符串乘法生成分隔线
    print('-' * 40)
    print('=' * 20 + ' 标题 ' + '=' * 20)

    # 3. translate + maketrans → 批量字符替换（比多次 replace 高效）
    table = str.maketrans('aeiou', '12345')
    print('hello world'.translate(table))   # h2ll4 w4rld

    # 删除指定字符（第三个参数是要删除的字符）
    table2 = str.maketrans('', '', ' \t\n')
    print('h e l l o'.translate(table2))    # hello

    # 4. 字符串模板 Template（防注入，比 format 安全）
    from string import Template
    t = Template('Hello, $name! You have $count messages.')
    print(t.substitute(name='Alice', count=5))
    # safe_substitute → 缺少变量不报错，保留占位符
    print(t.safe_substitute(name='Bob'))

    # 5. 统计字符频率
    from collections import Counter
    text = 'hello world'
    freq = Counter(text.replace(' ', ''))
    print('字符频率:', freq.most_common(3))   # 前 3 名

    # 6. 字符串比较（字典序）
    print('apple' < 'banana')   # True
    print('Z' < 'a')             # True（大写 ASCII 比小写小）
    print(sorted(['banana', 'Apple', 'cherry'], key=str.lower))


if __name__ == '__main__':
    print('=' * 45)
    print('f-string 高级特性')
    fstring_advanced()

    print('=' * 45)
    print('多行字符串')
    multiline_strings()

    print('=' * 45)
    print('★ 性能对比（大量拼接）')
    performance_tips()

    print('=' * 45)
    print('实用技巧汇总')
    practical_tips()
