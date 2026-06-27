# 字符串常用方法
# 字符串是不可变对象，所有方法都返回新字符串，不修改原始值

# ============================================================
# 大小写转换
# ============================================================
def case_methods():
    s = 'hello WORLD python'

    print(s.upper())        # HELLO WORLD PYTHON
    print(s.lower())        # hello world python
    print(s.title())        # Hello World Python   → 每个单词首字母大写
    print(s.capitalize())   # Hello world python   → 仅第一个词首字母大写
    print(s.swapcase())     # HELLO world PYTHON   → 大小写互换

    # ★ 常用场景：用户输入标准化
    user_input = '  YeS  '
    if user_input.strip().lower() == 'yes':
        print('用户确认')


# ============================================================
# 查找与判断
# ============================================================
def find_methods():
    s = 'Python is great, Python is fun'

    # find → 找不到返回 -1（安全）
    print(s.find('Python'))      # 0    → 第一次出现的索引
    print(s.find('Python', 5))   # 17   → 从索引 5 开始找
    print(s.find('Java'))        # -1   → 找不到返回 -1

    # index → 找不到抛 ValueError（谨慎用）
    print(s.index('great'))      # 10

    # rfind → 从右边开始找
    print(s.rfind('Python'))     # 17

    # count → 统计出现次数
    print(s.count('Python'))     # 2
    print(s.count('is'))         # 2

    # ★ 判断系列（返回 True/False）
    print('abc123'.isalnum())    # True  → 全字母或数字
    print('abc'.isalpha())       # True  → 全字母
    print('123'.isdigit())       # True  → 全数字
    print('   '.isspace())       # True  → 全空白
    print('Hello'.istitle())     # True  → 标题格式
    print('HELLO'.isupper())     # True
    print('hello'.islower())     # True


# ============================================================
# 替换
# ============================================================
def replace_methods():
    s = 'I like cats. Cats are cute.'

    # replace(old, new, count=-1)  count 指定最多替换几次
    print(s.replace('cats', 'dogs'))          # I like dogs. Cats are cute.（区分大小写）
    print(s.replace('cats', 'dogs', 1))       # 只替换第一个
    print(s.lower().replace('cats', 'dogs'))  # ★ 不区分大小写的替换技巧

    # ★ 运维常用：批量替换配置文件中的占位符
    template = 'HOST={host}, PORT={port}, DB={db}'
    config = template.replace('{host}', '127.0.0.1') \
                     .replace('{port}', '5432') \
                     .replace('{db}', 'myapp')
    print(config)


# ============================================================
# 分割与合并
# ============================================================
def split_join_methods():
    # split(sep, maxsplit=-1)
    s = 'a,b,c,d,e'
    print(s.split(','))          # ['a', 'b', 'c', 'd', 'e']
    print(s.split(',', 2))       # ['a', 'b', 'c,d,e']  → 最多分割 2 次

    # 不传参数 → 按任意空白分割，自动去掉多余空白
    s2 = '  hello   world  python  '
    print(s2.split())            # ['hello', 'world', 'python']

    # splitlines → 按换行符分割
    text = 'line1\nline2\rline3\r\nline4'
    print(text.splitlines())     # ['line1', 'line2', 'line3', 'line4']

    # partition → 分成 3 部分 (前, 分隔符, 后)
    url = 'https://www.example.com/path'
    scheme, sep, rest = url.partition('://')
    print(scheme, rest)          # https   www.example.com/path

    # join → 合并列表（上节重点，这里配合 split 使用）
    words = ['Python', 'is', 'awesome']
    print(' '.join(words))       # Python is awesome

    # ★ 实用技巧：去重并重组
    data = 'a,b,,c,,d'
    cleaned = ','.join(x for x in data.split(',') if x)
    print(cleaned)               # a,b,c,d


# ============================================================
# 去除空白 / 填充对齐
# ============================================================
def strip_pad_methods():
    # strip / lstrip / rstrip
    s = '   hello world   '
    print(repr(s.strip()))       # 'hello world'   两端去空白
    print(repr(s.lstrip()))      # 'hello world   '
    print(repr(s.rstrip()))      # '   hello world'

    # 可以指定要去除的字符集（不是前缀/后缀，而是字符集）
    s2 = '***hello***'
    print(s2.strip('*'))         # hello
    s3 = 'xxhelloxx'
    print(s3.strip('x'))         # hello

    # ★ Python 3.9+ 新增：removeprefix / removesuffix（精确去除前后缀）
    filename = 'report_2024.csv'
    print(filename.removesuffix('.csv'))    # report_2024
    print(filename.removeprefix('report_')) # 2024.csv

    # 填充对齐（输出报表时常用）
    print('name'.ljust(10))        # 'name      '  左对齐
    print('name'.rjust(10))        # '      name'  右对齐
    print('name'.center(10))       # '   name   '  居中
    print('name'.center(10, '-'))  # ---name---    指定填充字符
    print('42'.zfill(6))           # 000042        数字左补零


# ============================================================
# ★★ 重点：startswith / endswith（运维脚本高频使用）
# ============================================================
def starts_ends_with():
    filename = 'backup_server01.tar.gz'

    # 判断前后缀
    print(filename.startswith('backup'))     # True
    print(filename.endswith('.gz'))          # True
    print(filename.endswith('.zip'))         # False

    # ★ 传入元组 → 一次判断多个
    files = ['log.txt', 'data.csv', 'image.png', 'report.py']
    for f in files:
        if f.endswith(('.txt', '.csv')):
            print(f'文本文件：{f}')
        elif f.endswith('.py'):
            print(f'Python脚本：{f}')

    # 运维场景：过滤日志文件
    logs = ['app.log', 'app.log.1', 'app.log.2', 'error.txt', 'config.yaml']
    log_files = [f for f in logs if f.startswith('app.log')]
    print('日志文件：', log_files)


if __name__ == '__main__':
    print('=' * 45)
    print('大小写转换')
    case_methods()

    print('=' * 45)
    print('查找与判断')
    find_methods()

    print('=' * 45)
    print('替换')
    replace_methods()

    print('=' * 45)
    print('分割与合并')
    split_join_methods()

    print('=' * 45)
    print('去除空白 & 填充')
    strip_pad_methods()

    print('=' * 45)
    print('★ startswith / endswith')
    starts_ends_with()
