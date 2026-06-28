# 字典（Dict）
# 键值对集合，有序（Python 3.7+）、可变、键唯一
# 运维脚本最常用的数据结构，没有之一

# ============================================================
# 创建字典
# ============================================================
def create_dict():
    # 字面量
    d1 = {'name': 'Alice', 'age': 30, 'city': 'Beijing'}

    # dict() 构造
    d2 = dict(name='Bob', age=25)           # 关键字参数
    d3 = dict([('a', 1), ('b', 2)])         # 键值对列表
    d4 = dict(zip(['x', 'y'], [10, 20]))    # zip 构造

    # ★ 字典推导式
    squares = {i: i**2 for i in range(1, 6)}
    print('平方字典:', squares)             # {1:1, 2:4, 3:9, 4:16, 5:25}

    even_sq = {k: v for k, v in squares.items() if k % 2 == 0}
    print('偶数平方:', even_sq)

    # fromkeys → 用同一个值初始化多个键
    keys = ['host', 'port', 'status']
    d5 = dict.fromkeys(keys, None)
    print('fromkeys:', d5)


# ============================================================
# 访问 & 安全取值
# ============================================================
def dict_access():
    server = {'host': '192.168.1.1', 'port': 22, 'status': 'online'}

    # 直接访问（键不存在会 KeyError）
    print(server['host'])

    # ★ get(key, default) → 键不存在返回默认值，不报错
    print(server.get('port'))           # 22
    print(server.get('timeout', 30))    # 30

    print('host' in server)             # True

    for key, val in server.items():     # ★ 推荐：同时遍历键值
        print(f'  {key}: {val}')

    print(list(server.keys()))
    print(list(server.values()))


# ============================================================
# 增删改
# ============================================================
def dict_modify():
    d = {'a': 1, 'b': 2}

    d['c'] = 3          # 新增
    d['a'] = 100        # 修改
    print('增改后:', d)

    d.update({'d': 4, 'e': 5})   # 批量更新
    print('update后:', d)

    # ★ Python 3.9+ 合并运算符
    config_default = {'timeout': 30, 'retry': 3, 'debug': False}
    config_user    = {'timeout': 60, 'debug': True}
    merged = config_default | config_user   # 后者覆盖前者
    print('合并:', merged)

    del d['e']
    val  = d.pop('d')               # 删除并返回值
    val2 = d.pop('z', 'not found')  # 键不存在返回默认值
    print('pop:', val, val2)

    d.clear()
    print('清空:', d)


# ============================================================
# ★★ setdefault → 键不存在时设置默认值并返回
# ============================================================
def setdefault_usage():
    logs = [
        ('ERROR', 'disk full'),
        ('INFO',  'backup done'),
        ('ERROR', 'network timeout'),
        ('WARN',  'cpu high'),
        ('INFO',  'service start'),
    ]

    # ★ setdefault 分组写法
    grouped = {}
    for level, msg in logs:
        grouped.setdefault(level, []).append(msg)

    print('分组结果:')
    for level, msgs in grouped.items():
        print(f'  {level}: {msgs}')


# ============================================================
# ★ 嵌套字典（服务器配置管理）
# ============================================================
def nested_dict():
    servers = {
        'web01': {'ip': '192.168.1.10', 'services': ['nginx', 'php-fpm'], 'disk_usage': 72},
        'db01':  {'ip': '192.168.1.20', 'services': ['mysql'],            'disk_usage': 88},
        'cache01':{'ip': '192.168.1.30', 'services': ['redis'],           'disk_usage': 45},
    }

    print(servers['web01']['ip'])
    print(servers['db01']['services'][0])

    # 找出磁盘使用超过 80% 的服务器
    print('磁盘告警:')
    for name, info in servers.items():
        if info['disk_usage'] > 80:
            print(f'  ⚠ {name} ({info["ip"]}) 磁盘: {info["disk_usage"]}%')

    # 安全访问深层嵌套
    usage = servers.get('web99', {}).get('disk_usage', 'N/A')
    print('不存在的服务器磁盘:', usage)    # N/A


# ============================================================
# 字典排序
# ============================================================
def dict_sort():
    scores = {'Alice': 92, 'Bob': 85, 'Carol': 97, 'Dave': 78}

    by_key = dict(sorted(scores.items()))
    print('按键排序:', by_key)

    # ★ 按值降序
    by_val = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))
    print('按值降序:', by_val)

    top2 = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True)[:2])
    print('Top2:', top2)


if __name__ == '__main__':
    print('=' * 45)
    print('创建字典')
    create_dict()

    print('=' * 45)
    print('访问 & 安全取值')
    dict_access()

    print('=' * 45)
    print('增删改')
    dict_modify()

    print('=' * 45)
    print('★★ setdefault 分组')
    setdefault_usage()

    print('=' * 45)
    print('★ 嵌套字典（服务器配置）')
    nested_dict()

    print('=' * 45)
    print('字典排序')
    dict_sort()
