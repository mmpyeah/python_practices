# 第一个python函数

"""
    这是多行注释
"""
long_str = '''这是第一行
这是第二行
这是第三行
这是第四行'''



def print_str(str):
    print(str)

def function1():
    inputStr = input("请输入文本内容")
    print_str(inputStr)

def function2():
    float_num = '23.5'
    print(type(float_num))
    float_num = float(float_num)
    int_num = int(float_num)
    print(int_num)

def function3():
    yaowei_num = input("请输入你的腰围：")
    weight_num = input("请输入你的体重：")

def calc_fat_rate():
    weight_num = float(input("请输入你的体重："))
    yaowei_num = float(input("请输入你的腰围："))
    num_a = float(yaowei_num * 0.74)
    num_b = float(weight_num * 0.082 + 44.74)

    weight_num = (num_a - num_b) / weight_num * 100
    return weight_num

def function4():
    bytes_str = b'hahaha'
    print(type(bytes_str))
    print(bytes_str)

    str1 = '哈哈'
    print(str1)
    print(str1.encode())
    print(bytes_str.decode())

def function5():
    a = '你好'
    b = 'Python'
    print(a + b)
    print(b * 100)


if __name__ == '__main__':
    # fat_rate = str('%.2f' % calc_fat_rate())
    # print_str('您的体脂率为：' + fat_rate + '%')

    function5()




