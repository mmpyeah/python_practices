# 元组（Tuple）
# 有序、不可变、允许重复元素
# 不可变 = 创建后不能增删改，适合存放不该被修改的数据

# ============================================================
# 创建元组
# ============================================================
def create_tuple():
    t1 = (1, 2, 3)
    t2 = 1, 2, 3            # 括号可以省略（不推荐，可读性差）
    t3 = (42,)              # ★ 单元素元组必须加逗号！
    t4 = (42)               # 这是 int，不是元组！
    t5 = tuple([1, 2, 3])   # list → tuple
    t6 = tuple('hello')     # ('h','e','l','l','o')
    empty = ()

    print(type(t3), t3)     # <class 'tuple'> (42,)
    print(type(t4), t4)     # <class 'int'>   42
    print(t6)


# ============================================================
# 访问 & 操作（只读）
# ============================================================
def tuple_access():
    t = (10, 20, 30, 20, 40)

    print(t[0])             # 10
    print(t[-1])            # 40
    print(t[1:3])           # (20, 30)
    print(t.index(20))      # 1   → 第一次出现的索引
    print(t.count(20))      # 2   → 出现次数
    print(len(t))           # 5
    print(20 in t)          # True

    # 元组拼接（返回新元组）
    t2 = (1, 2) + (3, 4)
    print(t2)               # (1, 2, 3, 4)

    # 元组重复
    print((0,) * 5)         # (0, 0, 0, 0, 0)


# ============================================================
# ★★ 解包赋值（Unpacking）
# ============================================================
def unpacking():
    # 基础解包
    point = (3, 5)
    x, y = point
    print(f'x={x}, y={y}')

    # 交换变量（Python 独有的优雅写法）
    a, b = 10, 20
    a, b = b, a             # ★ 不需要临时变量
    print(f'交换后 a={a}, b={b}')

    # 函数返回多值本质上是元组
    def min_max(lst):
        return min(lst), max(lst)

    lo, hi = min_max([3, 1, 4, 1, 5, 9])
    print(f'最小={lo}, 最大={hi}')

    # ★ 星号解包（*）收集剩余元素
    first, *rest = [1, 2, 3, 4, 5]
    print(f'first={first}, rest={rest}')    # first=1, rest=[2,3,4,5]

    *head, last = [1, 2, 3, 4, 5]
    print(f'head={head}, last={last}')      # head=[1,2,3,4], last=5

    first2, *middle, last2 = [1, 2, 3, 4, 5]
    print(f'first={first2}, middle={middle}, last={last2}')

    # 嵌套解包
    data = ('Alice', (25, 'Beijing'))
    name, (age, city) = data
    print(f'{name}, {age}岁, {city}')

    # 忽略不需要的值（用 _ 占位）
    _, month, day = (2024, 6, 27)
    print(f'月:{month} 日:{day}')


# ============================================================
# ★ namedtuple 具名元组（比普通元组可读性强）
# ============================================================
def named_tuple():
    from collections import namedtuple

    # 定义具名元组（类似轻量级类）
    Point  = namedtuple('Point', ['x', 'y'])
    Server = namedtuple('Server', ['host', 'port', 'status'])

    p = Point(3, 5)
    print(p.x, p.y)         # 既可以用属性名访问
    print(p[0], p[1])       # 也可以用索引访问
    print(p)                 # Point(x=3, y=5)

    s = Server('192.168.1.1', 22, 'online')
    print(f'{s.host}:{s.port} → {s.status}')

    # _asdict() → 转为字典
    print(s._asdict())

    # _replace() → 返回修改了某字段的新元组（原对象不变）
    s2 = s._replace(status='offline')
    print(s2)


# ============================================================
# 元组 vs 列表：什么时候用哪个？
# ============================================================
def tuple_vs_list():
    print('''
    使用元组的场景：
    1. 数据不应该被修改（坐标、RGB颜色、数据库记录）
    2. 函数返回多个值
    3. 字典的键（列表不能做键，元组可以）
    4. 比列表占用内存更少、访问速度更快

    使用列表的场景：
    1. 需要增删改元素
    2. 顺序可能变化
    3. 同类型元素的集合
    ''')

    # 元组可以作字典键，列表不行
    locations = {
        (39.9, 116.4): '北京',
        (31.2, 121.5): '上海',
    }
    print(locations[(39.9, 116.4)])   # 北京

    # 内存对比
    import sys
    lst = [1, 2, 3, 4, 5]
    tpl = (1, 2, 3, 4, 5)
    print(f'list 内存: {sys.getsizeof(lst)} bytes')
    print(f'tuple 内存: {sys.getsizeof(tpl)} bytes')


if __name__ == '__main__':
    print('=' * 45)
    print('创建元组')
    create_tuple()

    print('=' * 45)
    print('访问 & 操作')
    tuple_access()

    print('=' * 45)
    print('★★ 解包赋值')
    unpacking()

    print('=' * 45)
    print('★ namedtuple 具名元组')
    named_tuple()

    print('=' * 45)
    print('元组 vs 列表')
    tuple_vs_list()
