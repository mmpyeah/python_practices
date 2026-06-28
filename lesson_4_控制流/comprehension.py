# 推导式（Comprehension）
# Python 最具特色的语法之一，让代码更简洁、更快
# 四种：列表推导式、字典推导式、集合推导式、生成器表达式

# ============================================================
# ★★ 列表推导式
# 语法：[表达式 for 变量 in 可迭代 if 条件]
# ============================================================
def list_comp():
    # 基础：生成平方列表
    squares = [x**2 for x in range(1, 11)]
    print('平方:', squares)

    # 带过滤条件
    even_squares = [x**2 for x in range(1, 11) if x % 2 == 0]
    print('偶数平方:', even_squares)

    # 字符串处理
    words   = ['  Hello  ', '  world  ', '  PYTHON  ']
    cleaned = [w.strip().lower() for w in words]
    print('清理:', cleaned)

    # 条件表达式在左边（不是过滤，是转换）
    nums    = [-3, -1, 0, 2, 5, -4]
    signs   = ['负' if x < 0 else ('零' if x == 0 else '正') for x in nums]
    print('符号:', signs)

    # 嵌套循环推导式（展平矩阵）
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    flat   = [x for row in matrix for x in row]
    print('展平:', flat)

    # 笛卡尔积
    colors = ['红', '绿', '蓝']
    sizes  = ['S', 'M', 'L']
    skus   = [f'{c}-{s}' for c in colors for s in sizes]
    print('SKU:', skus)


# ============================================================
# ★★ 字典推导式
# 语法：{键表达式: 值表达式 for 变量 in 可迭代 if 条件}
# ============================================================
def dict_comp():
    # 基础：反转键值
    original = {'a': 1, 'b': 2, 'c': 3}
    reversed_d = {v: k for k, v in original.items()}
    print('反转键值:', reversed_d)

    # 过滤字典（只保留值 > 1 的项）
    filtered = {k: v for k, v in original.items() if v > 1}
    print('过滤:', filtered)

    # 批量处理值
    prices = {'apple': 5.5, 'banana': 3.2, 'cherry': 8.0}
    discounted = {k: round(v * 0.9, 1) for k, v in prices.items()}
    print('打九折:', discounted)

    # 两个列表合并成字典
    keys   = ['host', 'port', 'db']
    values = ['localhost', 5432, 'prod']
    config = {k: v for k, v in zip(keys, values)}
    print('配置:', config)

    # ★ 运维场景：从服务器列表提取关键字段
    servers = [
        {'name': 'web01', 'ip': '192.168.1.10', 'status': 'online',  'cpu': 45},
        {'name': 'db01',  'ip': '192.168.1.20', 'status': 'online',  'cpu': 82},
        {'name': 'web02', 'ip': '192.168.1.11', 'status': 'offline', 'cpu': 0},
    ]
    # 只取在线服务器的 name → ip 映射
    online_map = {s['name']: s['ip'] for s in servers if s['status'] == 'online'}
    print('在线服务器:', online_map)

    # CPU > 80 的服务器告警字典
    cpu_alert = {s['name']: s['cpu'] for s in servers if s['cpu'] > 80}
    print('CPU告警:', cpu_alert)


# ============================================================
# ★ 集合推导式
# 语法：{表达式 for 变量 in 可迭代 if 条件}
# ============================================================
def set_comp():
    # 基础：提取唯一首字母
    words = ['apple', 'banana', 'avocado', 'cherry', 'blueberry']
    initials = {w[0] for w in words}
    print('首字母集合:', initials)

    # 过滤后去重
    nums = [1, -2, 3, -3, 2, -1, 4]
    positive_set = {abs(n) for n in nums}
    print('绝对值集合（自动去重）:', positive_set)

    # 从日志提取唯一 IP
    logs = [
        '192.168.1.1 GET /index',
        '10.0.0.1 POST /login',
        '192.168.1.1 GET /about',
        '10.0.0.2 GET /api',
    ]
    unique_ips = {line.split()[0] for line in logs}
    print('访问IP（唯一）:', unique_ips)


# ============================================================
# ★★ 生成器表达式（内存友好的推导式）
# 语法：(表达式 for 变量 in 可迭代 if 条件)
# 区别：列表推导式立即生成所有元素；生成器按需生成，节省内存
# ============================================================
def generator_expr():
    # 外层是 () 而不是 []
    gen = (x**2 for x in range(10))
    print('生成器对象:', gen)           # 不是列表，是生成器
    print('第一个:', next(gen))         # 0
    print('第二个:', next(gen))         # 1
    print('转列表:', list(gen))         # 剩余的 [4,9,16,...,81]

    # ★ 直接传给函数时可以省略外层括号
    total = sum(x**2 for x in range(1, 101))
    print('1~100平方和:', total)        # 338350

    max_val = max(len(w) for w in ['apple', 'banana', 'fig'])
    print('最长单词长度:', max_val)

    # 内存对比
    import sys
    lst_comp = [x**2 for x in range(10000)]
    gen_expr = (x**2 for x in range(10000))
    print(f'列表推导式内存: {sys.getsizeof(lst_comp):,} bytes')
    print(f'生成器表达式内存: {sys.getsizeof(gen_expr):,} bytes')
    # ★ 数据量大时用生成器，节省大量内存


# ============================================================
# 推导式 vs 普通循环：性能 & 可读性
# ============================================================
def comp_vs_loop():
    import time

    data = list(range(100000))

    # 普通循环
    t0 = time.time()
    result1 = []
    for x in data:
        if x % 2 == 0:
            result1.append(x * 2)
    t1 = time.time()

    # 推导式
    t2 = time.time()
    result2 = [x * 2 for x in data if x % 2 == 0]
    t3 = time.time()

    print(f'普通循环: {(t1-t0)*1000:.2f} ms')
    print(f'列表推导式: {(t3-t2)*1000:.2f} ms')
    print('结果一致:', result1 == result2)

    print('''
    推导式使用原则：
    ✓ 逻辑简单（1~2个条件）→ 用推导式，更简洁快速
    ✗ 逻辑复杂（多重嵌套、副作用）→ 用普通循环，更清晰
    ✓ 大数据量 → 用生成器表达式，节省内存
    ''')


if __name__ == '__main__':
    print('=' * 45)
    print('★★ 列表推导式')
    list_comp()

    print('=' * 45)
    print('★★ 字典推导式')
    dict_comp()

    print('=' * 45)
    print('★ 集合推导式')
    set_comp()

    print('=' * 45)
    print('★★ 生成器表达式')
    generator_expr()

    print('=' * 45)
    print('推导式 vs 普通循环')
    comp_vs_loop()
