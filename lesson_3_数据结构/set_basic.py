# 集合（Set）
# 无序、不重复、可变
# 核心用途：去重、集合运算（交集/并集/差集）

# ============================================================
# 创建集合
# ============================================================
def create_set():
    s1 = {1, 2, 3, 4, 5}
    s2 = set([1, 2, 2, 3, 3, 4])   # 自动去重
    s3 = set('hello')               # {'h', 'e', 'l', 'o'}  l 只保留一个
    empty = set()                   # ★ 注意：{} 是空字典，不是空集合！

    print(s1)
    print('去重:', s2)              # {1, 2, 3, 4}
    print('字符串转集合:', s3)
    print('空集合类型:', type(empty))


# ============================================================
# 增删操作
# ============================================================
def set_modify():
    s = {1, 2, 3}

    s.add(4)            # 添加单个元素（已存在则无效）
    s.update([5, 6, 6]) # 批量添加（等价于 |=）
    print('增加后:', s)

    s.remove(6)         # 删除，不存在报 KeyError
    s.discard(99)       # ★ 删除，不存在不报错（推荐）
    popped = s.pop()    # 随机删除一个元素并返回（集合无序）
    print('删除后:', s, '| pop取出:', popped)

    s.clear()
    print('清空:', s)


# ============================================================
# ★★ 集合运算（最核心的用法）
# ============================================================
def set_operations():
    a = {1, 2, 3, 4, 5}
    b = {4, 5, 6, 7, 8}

    # 交集：两个集合都有的
    print('交集  a & b :', a & b)           # {4, 5}
    print('交集  方法   :', a.intersection(b))

    # 并集：两个集合合并（去重）
    print('并集  a | b :', a | b)           # {1,2,3,4,5,6,7,8}
    print('并集  方法   :', a.union(b))

    # 差集：在 a 中但不在 b 中
    print('差集  a - b :', a - b)           # {1, 2, 3}
    print('差集  方法   :', a.difference(b))

    # 对称差：只在其中一个集合里的（不在交集里的）
    print('对称差 a ^ b:', a ^ b)           # {1, 2, 3, 6, 7, 8}
    print('对称差 方法  :', a.symmetric_difference(b))

    # 子集 / 超集判断
    c = {1, 2}
    print('{1,2} 是 a 的子集:', c.issubset(a))     # True
    print('a 是 {1,2} 的超集:', a.issuperset(c))   # True
    print('a 和 b 有无交集:', not a.isdisjoint(b)) # True（有交集）

    # ★ 运维场景：对比两批服务器清单
    servers_expected = {'web01', 'web02', 'db01', 'cache01'}
    servers_actual   = {'web01', 'db01', 'cache01', 'monitor01'}

    missing  = servers_expected - servers_actual    # 应有但没有
    extra    = servers_actual - servers_expected    # 多出来的
    ok       = servers_expected & servers_actual    # 正常的

    print(f'\n缺少的服务器: {missing}')
    print(f'多余的服务器: {extra}')
    print(f'正常的服务器: {ok}')


# ============================================================
# ★ 去重场景（集合最常见用途）
# ============================================================
def dedup_usage():
    # 列表去重
    ips = ['10.0.0.1', '10.0.0.2', '10.0.0.1', '10.0.0.3', '10.0.0.2']
    unique_ips = list(set(ips))
    print('去重IP:', sorted(unique_ips))

    # 找出重复元素
    lst = [1, 2, 3, 2, 4, 3, 5]
    seen = set()
    duplicates = set()
    for x in lst:
        if x in seen:
            duplicates.add(x)
        seen.add(x)
    print('重复元素:', duplicates)    # {2, 3}

    # 快速判断元素是否已处理（比 list 的 in 快得多）
    processed = set()
    tasks = ['task1', 'task2', 'task1', 'task3', 'task2']
    for task in tasks:
        if task not in processed:
            print(f'处理: {task}')
            processed.add(task)


# ============================================================
# frozenset → 不可变集合（可以做字典的键）
# ============================================================
def frozenset_usage():
    fs = frozenset([1, 2, 3])
    print(type(fs), fs)

    # frozenset 可以作字典的键
    network_map = {
        frozenset(['web01', 'web02']): 'web-cluster',
        frozenset(['db01', 'db02']):   'db-cluster',
    }
    key = frozenset(['web01', 'web02'])
    print(network_map[key])    # web-cluster


# ============================================================
# 集合推导式
# ============================================================
def set_comprehension():
    # 提取字符串中的唯一字母（自动去重）
    text = 'hello world python'
    unique_chars = {c for c in text if c != ' '}
    print('唯一字符:', sorted(unique_chars))

    # 从日志提取唯一IP
    logs = [
        '192.168.1.1 GET /index.html',
        '192.168.1.2 POST /login',
        '192.168.1.1 GET /about.html',
        '10.0.0.1 GET /api/data',
    ]
    unique_ips = {line.split()[0] for line in logs}
    print('访问IP集合:', unique_ips)


if __name__ == '__main__':
    print('=' * 45)
    print('创建集合')
    create_set()

    print('=' * 45)
    print('增删操作')
    set_modify()

    print('=' * 45)
    print('★★ 集合运算')
    set_operations()

    print('=' * 45)
    print('★ 去重场景')
    dedup_usage()

    print('=' * 45)
    print('frozenset')
    frozenset_usage()

    print('=' * 45)
    print('集合推导式')
    set_comprehension()
