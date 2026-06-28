# for 循环
# 遍历任意可迭代对象：list、tuple、str、dict、range、文件...

# ============================================================
# 基础 for 遍历
# ============================================================
def basic_for():
    # 遍历列表
    fruits = ['apple', 'banana', 'cherry']
    for fruit in fruits:
        print(fruit)

    # 遍历字符串
    for ch in 'Python':
        print(ch, end=' ')
    print()

    # 遍历 range
    for i in range(5):          # 0 1 2 3 4
        print(i, end=' ')
    print()

    for i in range(1, 6):       # 1 2 3 4 5
        print(i, end=' ')
    print()

    for i in range(0, 10, 2):   # 0 2 4 6 8（步长2）
        print(i, end=' ')
    print()

    for i in range(5, 0, -1):   # 5 4 3 2 1（倒序）
        print(i, end=' ')
    print()


# ============================================================
# ★★ enumerate — 带索引遍历（高频使用）
# ============================================================
def enumerate_usage():
    fruits = ['apple', 'banana', 'cherry']

    # 传统写法（不推荐）
    for i in range(len(fruits)):
        print(f'{i}: {fruits[i]}')

    print('---')

    # ★ enumerate 写法（推荐）
    for i, fruit in enumerate(fruits):
        print(f'{i}: {fruit}')

    print('---')

    # start 参数：从指定数字开始计数
    for i, fruit in enumerate(fruits, start=1):
        print(f'第{i}个: {fruit}')

    # 实用场景：给列表加序号
    tasks = ['备份数据库', '重启服务', '检查日志', '发送报告']
    for no, task in enumerate(tasks, 1):
        print(f'  [{no}] {task}')


# ============================================================
# ★★ zip — 并行遍历多个序列
# ============================================================
def zip_usage():
    names  = ['Alice', 'Bob', 'Carol']
    scores = [92, 85, 97]
    cities = ['Beijing', 'Shanghai', 'Guangzhou']

    # 同时遍历两个列表
    for name, score in zip(names, scores):
        print(f'{name}: {score}')

    print('---')

    # 同时遍历三个
    for name, score, city in zip(names, scores, cities):
        print(f'{name}({city}): {score}')

    # ★ zip 遇到最短的停止（不报错）
    long  = [1, 2, 3, 4, 5]
    short = ['a', 'b', 'c']
    print(list(zip(long, short)))   # [(1,'a'), (2,'b'), (3,'c')]

    # zip_longest → 补 None 到最长（需要 import）
    from itertools import zip_longest
    print(list(zip_longest(long, short, fillvalue='-')))

    # ★ zip 转字典
    keys   = ['host', 'port', 'db']
    values = ['localhost', 5432, 'myapp']
    config = dict(zip(keys, values))
    print('config:', config)


# ============================================================
# 遍历字典
# ============================================================
def dict_iteration():
    server = {'host': '10.0.0.1', 'port': 22, 'user': 'root'}

    for key in server:               # 遍历键
        print(key)

    for val in server.values():      # 遍历值
        print(val)

    for k, v in server.items():      # ★ 遍历键值对（最常用）
        print(f'{k} = {v}')

    # 遍历时不能修改字典大小，可以先拷贝
    config = {'a': 1, 'b': None, 'c': 3, 'd': None}
    cleaned = {k: v for k, v in config.items() if v is not None}
    print('清理None后:', cleaned)


# ============================================================
# break / continue / else
# ============================================================
def loop_control():
    # break → 跳出整个循环
    print('break 示例:')
    for i in range(10):
        if i == 5:
            break
        print(i, end=' ')
    print()

    # continue → 跳过本次迭代，继续下一次
    print('continue 示例（跳过偶数）:')
    for i in range(10):
        if i % 2 == 0:
            continue
        print(i, end=' ')
    print()

    # ★ for...else：循环正常结束（没有被 break）才执行 else
    print('for...else 示例:')
    targets = [3, 7, 2, 9, 5]
    search  = 6

    for item in targets:
        if item == search:
            print(f'找到 {search}')
            break
    else:
        print(f'{search} 不存在')    # 没有 break，执行这里

    # 实用场景：查找并验证
    servers = ['web01', 'db01', 'cache01']
    target  = 'db01'
    for s in servers:
        if s == target:
            print(f'找到服务器: {target}')
            break
    else:
        print(f'服务器 {target} 不在清单中')


# ============================================================
# ★ 运维实战：遍历日志文件（模拟）
# ============================================================
def ops_log_scan():
    # 模拟日志行
    log_lines = [
        '2024-06-27 10:00:01 INFO  service started',
        '2024-06-27 10:01:15 ERROR disk usage 95%',
        '2024-06-27 10:02:30 INFO  backup running',
        '2024-06-27 10:03:44 ERROR network timeout',
        '2024-06-27 10:04:10 WARN  cpu usage 80%',
        '2024-06-27 10:05:00 ERROR memory leak detected',
        '2024-06-27 10:06:00 INFO  cleanup done',
    ]

    errors = []
    for i, line in enumerate(log_lines, 1):
        parts = line.split(None, 3)   # 最多分 4 段
        date, time, level, msg = parts
        if level == 'ERROR':
            errors.append({'line': i, 'time': time, 'msg': msg})

    print(f'共扫描 {len(log_lines)} 行，发现 {len(errors)} 个 ERROR：')
    for e in errors:
        print(f'  第{e["line"]}行 [{e["time"]}] {e["msg"]}')


if __name__ == '__main__':
    print('=' * 45)
    print('基础 for 遍历')
    basic_for()

    print('=' * 45)
    print('★★ enumerate 带索引遍历')
    enumerate_usage()

    print('=' * 45)
    print('★★ zip 并行遍历')
    zip_usage()

    print('=' * 45)
    print('遍历字典')
    dict_iteration()

    print('=' * 45)
    print('break / continue / else')
    loop_control()

    print('=' * 45)
    print('★ 运维实战：日志扫描')
    ops_log_scan()
