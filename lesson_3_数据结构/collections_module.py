# collections 模块
# Python 内置，提供比普通 dict/list 更强大的容器类型
# 运维脚本高频使用：Counter 词频、defaultdict 分组、deque 队列

from collections import Counter, defaultdict, OrderedDict, deque, ChainMap

# ============================================================
# ★★ Counter — 计数器（词频统计神器）
# ============================================================
def counter_usage():
    # 统计字符频率
    text = 'hello world python programming'
    c = Counter(text.replace(' ', ''))
    print('字符频率:', c)
    print('最常见3个:', c.most_common(3))   # [('o', 3), ('l', 3), ...]

    # 统计列表元素频率
    logs_levels = ['ERROR', 'INFO', 'ERROR', 'WARN', 'INFO', 'ERROR', 'INFO']
    level_count = Counter(logs_levels)
    print('日志级别统计:', level_count)
    print('ERROR 次数:', level_count['ERROR'])
    print('DEBUG 次数:', level_count['DEBUG'])  # 不存在返回 0，不报错 ★

    # Counter 支持算术运算
    c1 = Counter({'a': 3, 'b': 2})
    c2 = Counter({'a': 1, 'b': 5, 'c': 2})
    print('相加:', c1 + c2)     # {'b':7, 'a':4, 'c':2}
    print('相减:', c1 - c2)     # {'a':2}  结果为负的会被丢弃
    print('交集:', c1 & c2)     # 取最小值 {'a':1, 'b':2}
    print('并集:', c1 | c2)     # 取最大值 {'b':5, 'a':3, 'c':2}

    # ★ 运维场景：统计各服务器的错误日志数量
    error_logs = [
        'web01', 'db01', 'web01', 'web02',
        'web01', 'db01', 'cache01', 'web02'
    ]
    server_errors = Counter(error_logs)
    print('\n服务器错误排名:')
    for server, count in server_errors.most_common():
        bar = '█' * count
        print(f'  {server:<10} {bar} ({count})')


# ============================================================
# ★★ defaultdict — 带默认值的字典（分组利器）
# ============================================================
def defaultdict_usage():
    # 普通字典分组需要先判断键是否存在
    # defaultdict 自动创建默认值，省去判断

    # 分组日志
    logs = [
        ('ERROR', 'disk full'),
        ('INFO',  'backup done'),
        ('ERROR', 'network timeout'),
        ('WARN',  'cpu high'),
        ('INFO',  'service start'),
        ('ERROR', 'memory leak'),
    ]

    # ★ defaultdict(list) — 值默认为空列表
    grouped = defaultdict(list)
    for level, msg in logs:
        grouped[level].append(msg)   # 不需要先判断 level 是否在字典里

    print('分组日志:')
    for level, msgs in grouped.items():
        print(f'  {level}: {msgs}')

    # defaultdict(int) — 值默认为 0（计数用）
    word_count = defaultdict(int)
    for word in 'the quick brown fox jumps over the lazy dog the'.split():
        word_count[word] += 1
    print('\n词频:', dict(word_count))

    # defaultdict(set) — 值默认为空集合（存唯一值）
    server_ips = defaultdict(set)
    connections = [
        ('web01', '10.0.0.1'), ('web01', '10.0.0.2'),
        ('db01',  '10.0.0.1'), ('web01', '10.0.0.1'),
    ]
    for server, ip in connections:
        server_ips[server].add(ip)   # 自动去重
    print('\n服务器连接IP:', dict(server_ips))


# ============================================================
# deque — 双端队列（高效的头尾操作）
# ============================================================
def deque_usage():
    # list 在头部插入/删除是 O(n)，deque 是 O(1)
    dq = deque([1, 2, 3, 4, 5])

    dq.append(6)        # 右侧追加
    dq.appendleft(0)    # ★ 左侧追加（list 没有高效方法）
    print('追加后:', dq)

    dq.pop()            # 右侧弹出
    dq.popleft()        # ★ 左侧弹出
    print('弹出后:', dq)

    dq.rotate(2)        # 向右旋转 2 步（负数向左）
    print('右旋2步:', dq)

    # ★ maxlen — 固定长度队列（自动丢弃旧数据）
    # 实用场景：保留最近 N 条日志
    recent_logs = deque(maxlen=3)
    for i in range(1, 7):
        recent_logs.append(f'log_{i}')
        print(f'加入log_{i}，当前队列: {list(recent_logs)}')


# ============================================================
# ChainMap — 多字典链式查找
# ============================================================
def chainmap_usage():
    # 场景：配置优先级（命令行 > 环境变量 > 默认配置）
    defaults = {'color': 'red',  'timeout': 30,   'debug': False}
    env_vars = {'timeout': 60,   'debug': True}
    cli_args = {'color': 'blue'}

    # ★ ChainMap 按顺序查找，找到第一个就返回
    config = ChainMap(cli_args, env_vars, defaults)

    print('color:  ', config['color'])    # blue   (cli_args 优先)
    print('timeout:', config['timeout'])  # 60     (env_vars 覆盖)
    print('debug:  ', config['debug'])    # True   (env_vars 覆盖)

    # 修改只影响第一个字典
    config['new_key'] = 'new_value'
    print('cli_args:', dict(cli_args))    # new_key 加进了 cli_args


# ============================================================
# OrderedDict — 有序字典（Python 3.7+ 后普通 dict 也保序，但它有额外功能）
# ============================================================
def ordereddict_usage():
    od = OrderedDict()
    od['first']  = 1
    od['second'] = 2
    od['third']  = 3

    # move_to_end — 把某个键移到末尾或开头
    od.move_to_end('first')         # 移到末尾
    od.move_to_end('third', last=False)  # 移到开头
    print('调整顺序后:', list(od.keys()))

    # ★ LRU 缓存简单实现（最近最少使用）
    class LRUCache:
        def __init__(self, capacity):
            self.cache = OrderedDict()
            self.capacity = capacity

        def get(self, key):
            if key not in self.cache:
                return -1
            self.cache.move_to_end(key)   # 访问后移到末尾（最近使用）
            return self.cache[key]

        def put(self, key, value):
            if key in self.cache:
                self.cache.move_to_end(key)
            self.cache[key] = value
            if len(self.cache) > self.capacity:
                self.cache.popitem(last=False)  # 删除最久未使用的（头部）

    lru = LRUCache(3)
    for k, v in [('a',1),('b',2),('c',3),('d',4)]:
        lru.put(k, v)
        print(f'put {k}={v}, cache: {list(lru.cache.keys())}')


if __name__ == '__main__':
    print('=' * 45)
    print('★★ Counter 计数器')
    counter_usage()

    print('=' * 45)
    print('★★ defaultdict 默认字典')
    defaultdict_usage()

    print('=' * 45)
    print('deque 双端队列')
    deque_usage()

    print('=' * 45)
    print('ChainMap 链式字典')
    chainmap_usage()

    print('=' * 45)
    print('OrderedDict 有序字典')
    ordereddict_usage()
