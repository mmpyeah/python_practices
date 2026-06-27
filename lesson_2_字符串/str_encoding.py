# 字符串编码与字节
# Python 3 中 str 是 Unicode，bytes 是原始字节
# 两者通过 encode() / decode() 互转

# ============================================================
# encode / decode 基础
# ============================================================
def encode_decode():
    s = '你好，Python！'

    # str → bytes
    b_utf8  = s.encode('utf-8')     # 最常用，中文 3字节/字
    b_gbk   = s.encode('gbk')       # Windows 中文环境常见，中文 2字节/字
    b_ascii = 'hello'.encode('ascii')

    print('UTF-8 字节:', b_utf8)
    print('UTF-8 长度:', len(b_utf8))    # 字节数，不是字符数
    print('GBK  字节:', b_gbk)
    print('GBK  长度:', len(b_gbk))

    # bytes → str
    print('UTF-8 解码:', b_utf8.decode('utf-8'))
    print('GBK  解码:', b_gbk.decode('gbk'))

    # ★ 错误：用错编码会 UnicodeDecodeError
    try:
        b_utf8.decode('gbk')     # UTF-8 字节用 GBK 解码
    except UnicodeDecodeError as e:
        print(f'解码错误: {e}')


# ============================================================
# ★ 重点：errors 参数处理乱码
# ============================================================
def encode_errors():
    s = '中文 English 混合'

    # errors='ignore'   → 跳过无法编码的字符
    # errors='replace'  → 用 ? 或 \ufffd 替换
    # errors='xmlcharrefreplace' → 转义成 XML 字符引用

    b = s.encode('ascii', errors='ignore')
    print('ignore:', b)           # b' English '  中文被忽略

    b2 = s.encode('ascii', errors='replace')
    print('replace:', b2)         # b'?? English ???'

    # 处理从文件/网络拿到的未知编码字节流
    raw = b'\xd6\xd0\xce\xc4'    # GBK 编码的"中文"
    safe = raw.decode('gbk', errors='replace')
    print('安全解码:', safe)


# ============================================================
# 字符串与字节的互操作
# ============================================================
def bytes_operations():
    # bytes 字面量
    b = b'hello'
    print(type(b), b)            # <class 'bytes'>

    # bytes 支持索引（返回 int）和切片（返回 bytes）
    print(b[0])                  # 104   → 'h' 的 ASCII 值
    print(b[1:3])                # b'el'

    # bytearray → 可变的字节数组（bytes 不可变）
    ba = bytearray(b'hello')
    ba[0] = 72                   # 'H' 的 ASCII
    print(ba)                    # bytearray(b'Hello')

    # hex() / fromhex() → 网络/二进制协议常用
    data = b'\x48\x65\x6c\x6c\x6f'
    print(data.hex())            # 48656c6c6f
    print(bytes.fromhex('48656c6c6f'))   # b'Hello'


# ============================================================
# ★ 运维常用：chardet 检测未知编码（需 pip install chardet）
# ============================================================
def detect_encoding_demo():
    # 演示思路，实际使用需安装 chardet
    print('# 实际用法（需先 pip install chardet）：')
    print('''
import chardet
with open('unknown.txt', 'rb') as f:
    raw = f.read()
result = chardet.detect(raw)
encoding = result['encoding']   # 如 'utf-8', 'GBK', 'ISO-8859-1'
text = raw.decode(encoding)
print(text)
''')


# ============================================================
# Unicode 相关
# ============================================================
def unicode_basics():
    # ord() → 字符转 Unicode 码点
    # chr() → 码点转字符
    print(ord('A'))      # 65
    print(ord('中'))     # 20013
    print(chr(65))       # A
    print(chr(20013))    # 中

    # Unicode 转义
    s = '\u4e2d\u6587'   # 中文
    print(s)             # 中文

    # 字符串长度（字符数，不是字节数）
    s2 = '你好'
    print(len(s2))                  # 2（字符数）
    print(len(s2.encode('utf-8')))  # 6（字节数，中文 utf-8 各占 3 字节）
    print(len(s2.encode('gbk')))    # 4（中文 GBK 各占 2 字节）


if __name__ == '__main__':
    print('=' * 45)
    print('encode / decode 基础')
    encode_decode()

    print('=' * 45)
    print('★ errors 参数处理乱码')
    encode_errors()

    print('=' * 45)
    print('bytes 操作')
    bytes_operations()

    print('=' * 45)
    print('chardet 检测编码（演示）')
    detect_encoding_demo()

    print('=' * 45)
    print('Unicode 基础')
    unicode_basics()
