# 字符串切片（Slicing）
# 语法：str[start:stop:step]
# start  → 起始索引（含），默认 0
# stop   → 结束索引（不含），默认到末尾
# step   → 步长，默认 1；负数 = 反向

# ============================================================
# 基础切片
# ============================================================
def basic_slice():
    s = 'Hello, Python!'
    #    0123456789...
    #    负索引从 -1 开始往左数

    print(s[0:5])       # Hello      → 索引 0~4
    print(s[7:])        # Python!    → 从 7 到末尾
    print(s[:5])        # Hello      → 从头到 4
    print(s[-7:])       # Python!    → 倒数第 7 个到末尾
    print(s[:-1])       # Hello, Python  → 去掉最后一个字符
    print(s[:])         # Hello, Python! → 完整复制


# ============================================================
# 步长切片
# ============================================================
def step_slice():
    s = 'abcdefghij'

    print(s[::2])       # acegi  → 每隔一个取一个
    print(s[1::2])      # bdfhj  → 从索引 1 开始，每隔一个
    print(s[::-1])      # jihgfedcba  ★ 反转字符串的最简写法
    print(s[8:2:-1])    # ihgfed → 从索引 8 倒退到 3
    print(s[::3])       # adgj   → 每 3 个取一个


# ============================================================
# ★ 重点：切片的实际应用场景
# ============================================================
def practical_slice():
    # 1. 反转字符串（面试常考）
    text = 'Python'
    print('反转：', text[::-1])         # nohtyP

    # 2. 去掉首尾特定字符（比 strip 更灵活）
    url = 'https://example.com/'
    print('去协议头：', url[8:])         # example.com/
    print('去末尾斜杠：', url[:-1])      # https://example.com

    # 3. 提取固定格式字段（日志/配置解析常用）
    log = '2024-06-27 ERROR database timeout'
    date = log[:10]
    level = log[11:16].strip()
    msg = log[17:]
    print(f'日期: {date}, 级别: {level}, 信息: {msg}')

    # 4. 判断回文（两种写法）
    word = 'racecar'
    print('是回文:', word == word[::-1])  # True

    # 5. 切片赋值（列表可以，字符串不行——字符串不可变）
    lst = list('abcde')
    lst[1:3] = ['X', 'Y']
    print('列表切片赋值:', lst)           # ['a', 'X', 'Y', 'd', 'e']


# ============================================================
# 索引越界不会报错（切片安全）
# ============================================================
def safe_slice():
    s = 'Hi'
    print(s[0:100])     # Hi    → 不报错，自动截断到末尾
    print(s[50:100])    # ''    → 空字符串，不报错


if __name__ == '__main__':
    print('=' * 45)
    print('基础切片')
    basic_slice()

    print('=' * 45)
    print('步长切片')
    step_slice()

    print('=' * 45)
    print('★ 实际应用')
    practical_slice()

    print('=' * 45)
    print('切片越界安全性')
    safe_slice()
