# 列表进阶：推导式 & 高阶函数
# 这是让代码更简洁、更 Pythonic 的核心技能

# ============================================================
# ★★ 列表推导式（List Comprehension）
# 语法：[表达式 for 变量 in 可迭代对象 if 条件]
# ============================================================
def list_comprehension():
    # 基础写法 vs 推导式
    # 传统写法
    squares_old = []
    for i in range(1, 6):
        squares_old.append(i ** 2)

    # ★ 推导式（推荐）
    squares = [i ** 2 for i in range(1, 6)]
    print('平方:', squares)            # [1, 4, 9, 16, 25]

    # 带条件过滤
    evens = [i for i in range(20) if i % 2 == 0]
    print('偶数:', evens)

    # 字符串处理
    words = ['  hello  ', '  world  ', '  python  ']
    cleaned = [w.strip().upper() for w in words]
    print('清理后:', cleaned)          # ['HELLO', 'WORLD', 'PYTHON']

    # 条件表达式（三元）放在表达式位置
    nums = [1, -2, 3, -4, 5]
    abs_vals = [x if x >= 0 else -x for x in nums]
    print('绝对值:', abs_vals)         # [1, 2, 3, 4, 5]

    # ★ 嵌套推导式（展平二维列表）
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    flat = [x for row in matrix for x in row]
    print('展平:', flat)               # [1, 2, 3, 4, 5, 6, 7, 8, 9]

    # 生成笛卡尔积
    pairs = [(x, y) for x in [1, 2] for y in ['a', 'b']]
    print('笛卡尔积:', pairs)


# ============================================================
# 嵌套列表（二维表）
# ============================================================
def nested_list():
    # 创建 3x3 矩阵
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]

    # 访问
    print(matrix[1][2])          # 6  → 第2行第3列

    # 遍历
    for row in matrix:
        print(row)

    # ★ 用推导式创建矩阵（注意陷阱）
    # 错误写法：所有行共享同一对象！
    wrong = [[0] * 3] * 3
    wrong[0][0] = 99
    print('错误写法:', wrong)    # 三行都变了！

    # 正确写法
    correct = [[0] * 3 for _ in range(3)]
    correct[0][0] = 99
    print('正确写法:', correct)  # 只有第一行变

    # 转置矩阵（行列互换）
    transposed = [[row[i] for row in matrix] for i in range(3)]
    print('转置:', transposed)


# ============================================================
# map / filter / zip / sorted 高阶函数
# ============================================================
def higher_order_functions():
    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # map(函数, 可迭代) → 对每个元素应用函数，返回迭代器
    doubled = list(map(lambda x: x * 2, nums))
    print('map 翻倍:', doubled)

    # filter(函数, 可迭代) → 过滤满足条件的元素
    odds = list(filter(lambda x: x % 2 != 0, nums))
    print('filter 奇数:', odds)

    # ★ 推导式通常比 map/filter 更可读
    doubled2 = [x * 2 for x in nums]
    odds2    = [x for x in nums if x % 2 != 0]
    print('推导式等效:', doubled2, odds2)

    # zip → 多序列合并
    keys   = ['name', 'age', 'city']
    values = ['Alice', 30, 'Beijing']
    d = dict(zip(keys, values))
    print('zip 转字典:', d)

    # zip 解包（unzip）
    pairs = [(1, 'a'), (2, 'b'), (3, 'c')]
    nums2, letters = zip(*pairs)
    print('解包:', list(nums2), list(letters))

    # ★ sorted 的 key 进阶用法
    people = [
        {'name': 'Bob',   'age': 30},
        {'name': 'Alice', 'age': 25},
        {'name': 'Carol', 'age': 35},
    ]
    # 按年龄排序
    by_age = sorted(people, key=lambda p: p['age'])
    print('按年龄:', [p['name'] for p in by_age])

    # 多字段排序（先按年龄，再按名字）
    data = [('Bob', 30), ('Alice', 25), ('Carol', 30)]
    multi = sorted(data, key=lambda x: (x[1], x[0]))
    print('多字段排序:', multi)


# ============================================================
# ★ 列表去重的几种方式（保留顺序 vs 不保留顺序）
# ============================================================
def dedup():
    lst = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]

    # 方式1：set（不保留顺序）
    print('set去重:', sorted(set(lst)))

    # 方式2：dict.fromkeys（Python 3.7+ 保留顺序）★ 推荐
    unique = list(dict.fromkeys(lst))
    print('保留顺序去重:', unique)

    # 方式3：手动（兼容旧版本）
    seen = []
    for x in lst:
        if x not in seen:
            seen.append(x)
    print('手动去重:', seen)


# ============================================================
# 运维实战：日志行解析
# ============================================================
def ops_practice():
    logs = [
        '2024-06-27 ERROR disk usage 95%',
        '2024-06-27 INFO  backup completed',
        '2024-06-27 ERROR memory usage 88%',
        '2024-06-27 WARN  cpu spike detected',
        '2024-06-27 INFO  service restarted',
        '2024-06-27 ERROR network timeout',
    ]

    # 提取所有 ERROR 行
    errors = [line for line in logs if 'ERROR' in line]
    print(f'ERROR 共 {len(errors)} 条:')
    for e in errors:
        print(' ', e)

    # 提取日志级别
    levels = [line.split()[1] for line in logs]
    print('级别列表:', levels)

    # 统计各级别数量
    from collections import Counter
    level_count = Counter(levels)
    print('级别统计:', dict(level_count))


if __name__ == '__main__':
    print('=' * 45)
    print('★★ 列表推导式')
    list_comprehension()

    print('=' * 45)
    print('嵌套列表（二维表）')
    nested_list()

    print('=' * 45)
    print('map / filter / zip / sorted')
    higher_order_functions()

    print('=' * 45)
    print('列表去重')
    dedup()

    print('=' * 45)
    print('运维实战：日志解析')
    ops_practice()
