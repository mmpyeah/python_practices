def dict_function():
    dict1 = dict(a=1, b=2, c=3)
    dict2 = dict([('a', 1), ('b', 2), ('c', 3)])
    dict3 = dict(zip(['a', 'b', 'c'], [1, 2, 3]))

    print(dict1)
    print(dict2)
    print(dict3)

def dict_function2():
    serverInfo = {'host': 'localhost', 'user': 'admin', 'password': '123456'}

    print(serverInfo)
    print(serverInfo['host'])

    print(serverInfo.get('host'))
    print(serverInfo.get('host1'))

    for k, v in serverInfo.items():
        print(k, v)

    print(list(serverInfo.keys()))
    print(list(serverInfo.values()))

def dict_function3():
    dict_number = {'a': 1, 'b': 2, 'c': 3}
    dict_number['d'] = 4
    print('增加一个元素', dict_number)

    dict_number.update({'d': 5})
    print('修改一个元素', dict_number)

    d1 = {'a': 1, 'b': 2, 'c': 3}
    d2 = {'a': 4, 'e': 5}
    merged = d1 | d2
    print('合并值：', merged)

    del merged['a']
    print('删除了一个值：', merged)

    val = merged.pop('b')
    print(f"删除了一个值%s" % val)
    print(f"删除了一个值{val}")

    val2 = merged.pop('x', 'not_found')
    print(f"删除了一个不存在的值{val2}")

    merged.clear()
    print(f"清空了{merged}")
    print('清空', merged)

if __name__ == '__main__':
    dict_function3()

