# 正则表达式 re 模块
# 正则是"描述字符串规律"的一种微型语言
# import re 即可使用，Python 内置，无需安装

import re

# ============================================================
# 元字符速查（注释里的规律，跑代码前先读一遍）
# ============================================================
# .      → 任意单个字符（除换行）
# \d     → 数字 [0-9]          \D → 非数字
# \w     → 字母/数字/下划线    \W → 非 \w
# \s     → 空白字符            \S → 非空白
# ^      → 字符串开头
# $      → 字符串结尾
# *      → 0次或多次
# +      → 1次或多次
# ?      → 0次或1次
# {n}    → 恰好 n 次
# {n,m}  → n 到 m 次
# []     → 字符集，如 [aeiou] [a-z] [0-9]
# [^]    → 排除字符集，如 [^0-9]
# |      → 或，如 cat|dog
# ()     → 分组，捕获子串
# \b     → 单词边界


# ============================================================
# 四个核心函数
# ============================================================
def core_functions():
    text = 'My phone is 138-1234-5678, backup: 021-87654321'

    # 1. re.search() → 找第一个匹配，返回 Match 对象或 None
    m = re.search(r'\d{3}-\d{4}-\d{4}', text)
    if m:
        print('search 找到:', m.group())    # 138-1234-5678
        print('位置:', m.start(), m.end())  # 12 25

    # 2. re.findall() → 找所有匹配，返回列表（最常用）
    phones = re.findall(r'\d[\d-]+\d', text)
    print('findall:', phones)               # ['138-1234-5678', '021-87654321']

    # 3. re.match() → 只匹配字符串开头（注意和 search 的区别）
    result = re.match(r'My', text)
    print('match My:', result.group() if result else None)   # My
    result2 = re.match(r'phone', text)
    print('match phone:', result2)          # None（不在开头）

    # 4. re.fullmatch() → 必须整个字符串都匹配
    print(re.fullmatch(r'\d+', '12345'))    # Match
    print(re.fullmatch(r'\d+', '123abc'))   # None


# ============================================================
# 分割与替换
# ============================================================
def split_sub():
    # re.split() → 比 str.split() 更灵活，支持多种分隔符
    text = 'one,two;three|four'
    parts = re.split(r'[,;|]', text)
    print('多分隔符分割:', parts)   # ['one', 'two', 'three', 'four']

    # re.sub(pattern, repl, string, count=0) → 替换
    log = '2024-06-27 ERROR: disk usage 95%'
    # 把日期格式从 YYYY-MM-DD 换成 YYYY/MM/DD
    new_log = re.sub(r'(\d{4})-(\d{2})-(\d{2})', r'\1/\2/\3', log)
    print('日期格式替换:', new_log)

    # 脱敏：把手机号中间4位替换成 ****
    phone = '用户手机：13812345678'
    masked = re.sub(r'(\d{3})\d{4}(\d{4})', r'\1****\2', phone)
    print('手机脱敏:', masked)   # 用户手机：138****5678


# ============================================================
# ★ 重点：分组 () 捕获子串
# ============================================================
def groups():
    # 不带分组 → 只返回整个匹配
    text = 'name: Alice, age: 30'
    print(re.findall(r'\w+:\s*\w+', text))   # ['name: Alice', 'age: 30']

    # 带分组 → findall 返回元组列表
    pairs = re.findall(r'(\w+):\s*(\w+)', text)
    print('分组匹配:', pairs)    # [('name', 'Alice'), ('age', '30')]
    for key, val in pairs:
        print(f'  {key} = {val}')

    # 命名分组（更清晰）
    log = '2024-06-27 10:30:00 ERROR disk full'
    pattern = r'(?P<date>\d{4}-\d{2}-\d{2}) (?P<time>\d{2}:\d{2}:\d{2}) (?P<level>\w+) (?P<msg>.+)'
    m = re.search(pattern, log)
    if m:
        print('日期:', m.group('date'))
        print('级别:', m.group('level'))
        print('消息:', m.group('msg'))


# ============================================================
# ★ 重点：编译 re.compile()（重复使用时性能更好）
# ============================================================
def compile_pattern():
    # 把正则编译成对象，后续反复使用不用重新解析
    ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')

    logs = [
        'Connected from 192.168.1.100',
        'Failed login from 10.0.0.255',
        'No IP in this line',
        'Request from 172.16.254.1 OK',
    ]

    for line in logs:
        m = ip_pattern.search(line)
        if m:
            print(f'IP地址: {m.group():<20} | 来源行: {line}')


# ============================================================
# re.IGNORECASE / re.MULTILINE 标志位
# ============================================================
def flags():
    text = 'Error: disk full\nerror: memory low\nERROR: cpu spike'

    # IGNORECASE → 不区分大小写
    errors = re.findall(r'error', text, re.IGNORECASE)
    print('不区分大小写:', errors)   # ['Error', 'error', 'ERROR']

    # MULTILINE → ^ $ 匹配每一行的开头/结尾
    lines = re.findall(r'^error.*', text, re.IGNORECASE | re.MULTILINE)
    print('多行匹配:', lines)


# ============================================================
# 常用实战正则模板（直接复制用）
# ============================================================
def useful_patterns():
    samples = {
        'email':    r'^[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}$',
        '手机号':   r'^1[3-9]\d{9}$',
        'IP地址':   r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
        '日期':     r'\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])',
        '中文':     r'[\u4e00-\u9fff]+',
        '纯数字':   r'^\d+$',
    }

    tests = {
        'email':    'user@example.com',
        '手机号':   '13812345678',
        'IP地址':   '192.168.0.1',
        '日期':     '2024-06-27',
        '中文':     '你好世界',
        '纯数字':   '98765',
    }

    for name, pattern in samples.items():
        val = tests[name]
        matched = bool(re.search(pattern, val))
        print(f'{name:<8} pattern: {matched}  样本: {val}')


if __name__ == '__main__':
    print('=' * 45)
    print('四个核心函数')
    core_functions()

    print('=' * 45)
    print('分割与替换')
    split_sub()

    print('=' * 45)
    print('★ 分组捕获')
    groups()

    print('=' * 45)
    print('★ compile 编译')
    compile_pattern()

    print('=' * 45)
    print('标志位 flags')
    flags()

    print('=' * 45)
    print('实战正则模板')
    useful_patterns()
