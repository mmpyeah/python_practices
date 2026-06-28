# 列表基础操作
# list 是 Python 最常用的数据结构，有序、可变、允许重复元素

# ============================================================
# 创建列表
# ============================================================
def create_list():
    # 字面量
    nums = [1, 2, 3, 4, 5]
    mixed = [1, 'hello', 3.14, True, None]   # 可以混合类型
    empty = []

    # list() 构造
    from_str   = list('hello')          # ['h', 'e', 'l', 'l', 'o']
    from_range = list(range(1, 6))      # [1, 2, 3, 4, 5]
    from_tuple = list((1, 2, 3))        # [1, 2, 3]

    print(nums, mixed, empty)
    print(from_str, from_range, from_tuple)

    # ★ 浅拷贝陷阱
    a = [1, 2, 3]
    b = a          # 危险！b 和 a 指向同一对象
    c = a.copy()   # 正确的浅拷贝
    d = a[:]       # 切片也是浅拷贝
    b.append(99)
    print('a:', a)   # [1, 2, 3, 99]  b 改了 a 也变！
    print('c:', c)   # [1, 2, 3]      c 不受影响


# ============================================================
# 增加元素
# ============================================================
def list_add():
    lst = [1, 2, 3]

    lst.append(4)           # 末尾追加单个元素 → [1,2,3,4]
    lst.extend([5, 6])      # 末尾追加多个元素 → [1,2,3,4,5,6]
    lst.insert(0, 0)        # 在索引 0 处插入  → [0,1,2,3,4,5,6]

    # ★ append vs extend 区别
    a = [1, 2]
    a.append([3, 4])        # [1, 2, [3, 4]]  整个列表作为一个元素
    b = [1, 2]
    b.extend([3, 4])        # [1, 2, 3, 4]    逐个追加

    print('append:', a)
    print('extend:', b)

    # + 拼接（返回新列表，不修改原列表）
    c = [1, 2] + [3, 4]
    print('+ 拼接:', c)


# ============================================================
# 删除元素
# ============================================================
def list_remove():
    lst = [10, 20, 30, 20, 40]

    lst.remove(20)          # 删除第一个值为 20 的元素
    popped  = lst.pop()     # 删除并返回最后一个元素
    popped2 = lst.pop(0)    # 删除并返回索引 0 的元素
    del lst[0]              # 删除索引 0（无返回值）

    print('删除后:', lst, '| pop取出:', popped, popped2)

    lst.clear()             # 清空列表
    print('清空后:', lst)   # []


# ============================================================
# 查找 & 修改
# ============================================================
def list_query():
    lst = ['a', 'b', 'c', 'b', 'd']

    print(lst[1])               # b
    print(lst[-1])              # d
    print(lst[1:3])             # ['b', 'c']
    print(lst.index('b'))       # 1  → 第一次出现的索引
    print(lst.count('b'))       # 2  → 出现次数
    print('c' in lst)           # True

    lst[0] = 'A'                # 按索引修改
    lst[1:3] = ['X', 'Y', 'Z'] # 切片赋值（可改变列表长度）
    print('修改后:', lst)


# ============================================================
# 排序 & 反转
# ============================================================
def list_sort():
    nums = [3, 1, 4, 1, 5, 9, 2, 6]

    nums.sort()                       # 原地升序
    print('升序:', nums)
    nums.sort(reverse=True)           # 原地降序
    print('降序:', nums)

    original = [3, 1, 4, 1, 5]
    new_sorted = sorted(original)     # ★ sorted() 返回新列表，不改原列表
    print('原列表不变:', original)
    print('sorted 结果:', new_sorted)

    # key 参数
    words = ['banana', 'Apple', 'cherry', 'date']
    print(sorted(words, key=str.lower))   # 忽略大小写
    print(sorted(words, key=len))         # 按长度

    lst = [1, 2, 3, 4, 5]
    lst.reverse()
    print('reverse:', lst)
    print('切片反转:', lst[::-1])          # 不修改原列表


# ============================================================
# ★ 常用内置函数配合列表
# ============================================================
def builtin_functions():
    nums = [3, 1, 4, 1, 5, 9, 2, 6, 5]

    print('len:', len(nums))
    print('max:', max(nums))
    print('min:', min(nums))
    print('sum:', sum(nums))

    # zip → 多列表并行遍历
    names  = ['Alice', 'Bob', 'Carol']
    scores = [90, 85, 92]
    for name, score in zip(names, scores):
        print(f'  {name}: {score}')

    # ★ enumerate → 带索引遍历（比 range(len()) 更 Pythonic）
    for i, name in enumerate(names, start=1):
        print(f'  第{i}名: {name}')


if __name__ == '__main__':
    print('=' * 45)
    print('创建列表')
    create_list()

    print('=' * 45)
    print('增加元素')
    list_add()

    print('=' * 45)
    print('删除元素')
    list_remove()

    print('=' * 45)
    print('查找 & 修改')
    list_query()

    print('=' * 45)
    print('排序 & 反转')
    list_sort()

    print('=' * 45)
    print('★ 内置函数配合列表')
    builtin_functions()
