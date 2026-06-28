# 条件判断：if / elif / else
# 控制程序走哪条分支

# ============================================================
# 基础 if / elif / else
# ============================================================
def basic_if():
    score = 85

    if score >= 90:
        grade = 'A'
    elif score >= 80:
        grade = 'B'
    elif score >= 70:
        grade = 'C'
    elif score >= 60:
        grade = 'D'
    else:
        grade = 'F'

    print(f'分数 {score} → 等级 {grade}')


# ============================================================
# ★ 真值判断（Python 的"假值"要记住）
# ============================================================
def truthiness():
    # 以下全部被视为 False：
    falsy_values = [0, 0.0, '', [], {}, set(), None, False]
    for v in falsy_values:
        if not v:
            print(f'  {repr(v):<12} → False')

    # 其余均为 True
    print('非空字符串:', bool('hello'))    # True
    print('非零数字:',  bool(42))         # True
    print('非空列表:',  bool([1]))        # True

    # ★ 实用：直接用对象做布尔判断，不用 len() == 0
    items = []
    if not items:                          # 比 if len(items) == 0 更 Pythonic
        print('列表为空')

    name = ''
    if name:
        print(f'你好, {name}')
    else:
        print('名字为空')


# ============================================================
# ★ 三元表达式（条件表达式）
# ============================================================
def ternary():
    # 语法：值A if 条件 else 值B
    age = 20
    status = '成年' if age >= 18 else '未成年'
    print(status)

    # 赋值时常用
    x = 10
    abs_x = x if x >= 0 else -x
    print('绝对值:', abs_x)

    # 嵌套三元（不超过两层，否则可读性差）
    score = 75
    grade = 'A' if score >= 90 else ('B' if score >= 80 else 'C')
    print('等级:', grade)

    # ★ 列表/字典里也可以用
    nums = [-3, 0, 5, -1, 8]
    abs_nums = [n if n >= 0 else -n for n in nums]
    print('绝对值列表:', abs_nums)


# ============================================================
# ★ match-case（Python 3.10+，结构化模式匹配）
# ============================================================
def match_case():
    # 基础用法：类似其他语言的 switch
    def http_status(code):
        match code:
            case 200:
                return 'OK'
            case 404:
                return 'Not Found'
            case 500:
                return 'Internal Server Error'
            case _:           # _ 是通配符，相当于 default
                return f'Unknown status: {code}'

    for code in [200, 404, 500, 301]:
        print(f'  {code} → {http_status(code)}')

    # 匹配序列（元组/列表）
    def handle_command(cmd):
        match cmd.split():
            case ['quit']:
                return '退出程序'
            case ['go', direction]:
                return f'向 {direction} 移动'
            case ['go', direction, steps]:
                return f'向 {direction} 移动 {steps} 步'
            case _:
                return f'未知命令: {cmd}'

    for cmd in ['quit', 'go north', 'go east 5', 'fly']:
        print(f'  "{cmd}" → {handle_command(cmd)}')

    # 匹配字典
    def handle_event(event):
        match event:
            case {'type': 'click', 'x': x, 'y': y}:
                return f'点击坐标 ({x}, {y})'
            case {'type': 'key', 'key': k}:
                return f'按键: {k}'
            case _:
                return '未知事件'

    events = [
        {'type': 'click', 'x': 100, 'y': 200},
        {'type': 'key', 'key': 'Enter'},
    ]
    for e in events:
        print(f'  {handle_event(e)}')


# ============================================================
# 常见陷阱
# ============================================================
def common_pitfalls():
    # 陷阱1：== 和 is 的区别
    # is → 判断是否是同一个对象（内存地址）
    # == → 判断值是否相等
    a = [1, 2, 3]
    b = [1, 2, 3]
    c = a
    print(a == b)    # True  → 值相等
    print(a is b)    # False → 不是同一对象
    print(a is c)    # True  → 同一对象

    # ★ None 比较必须用 is，不用 ==
    val = None
    if val is None:          # 正确
        print('val 是 None')
    # if val == None:        # 不推荐，某些自定义类会重载 __eq__

    # 陷阱2：浮点数比较
    print(0.1 + 0.2 == 0.3)   # False！浮点精度问题
    import math
    print(math.isclose(0.1 + 0.2, 0.3))  # True ★ 正确做法

    # 陷阱3：链式比较（Python 支持，很多语言不支持）
    x = 5
    print(1 < x < 10)         # True  → Python 特有的链式比较
    print(1 < x and x < 10)   # 等价写法


if __name__ == '__main__':
    print('=' * 45)
    print('基础 if / elif / else')
    basic_if()

    print('=' * 45)
    print('★ 真值判断')
    truthiness()

    print('=' * 45)
    print('★ 三元表达式')
    ternary()

    print('=' * 45)
    print('★ match-case（Python 3.10+）')
    match_case()

    print('=' * 45)
    print('常见陷阱')
    common_pitfalls()
