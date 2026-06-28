# while 循环
# 条件为真时反复执行，适合"不知道循环多少次"的场景

# ============================================================
# 基础 while
# ============================================================
def basic_while():
    # 计数
    i = 0
    while i < 5:
        print(i, end=' ')
        i += 1
    print()

    # 逐步缩减
    n = 16
    while n > 1:
        n //= 2
        print(n, end=' ')
    print()

    # 读取直到满足条件
    data = [10, 25, 3, 67, 42, 91, 8]
    total = 0
    idx   = 0
    while idx < len(data) and total < 100:
        total += data[idx]
        idx   += 1
    print(f'累加到 {total}，用了 {idx} 个数')


# ============================================================
# ★ while True + break（无限循环 + 主动退出）
# ============================================================
def infinite_loop():
    # 场景1：菜单交互（模拟，不用真正 input）
    def run_menu(commands):
        """模拟菜单循环，commands 是预设的输入列表"""
        idx = 0
        while True:
            cmd = commands[idx]; idx += 1
            print(f'> 输入: {cmd}')
            if cmd == 'quit':
                print('退出程序')
                break
            elif cmd == 'help':
                print('可用命令: help, status, quit')
            elif cmd == 'status':
                print('服务运行中...')
            else:
                print(f'未知命令: {cmd}')

    run_menu(['help', 'status', 'foo', 'quit'])

    print()

    # 场景2：重试机制（运维常用）
    import random
    random.seed(42)

    def try_connect(max_retries=5):
        attempt = 0
        while True:
            attempt += 1
            success = random.random() > 0.6   # 模拟40%失败率
            print(f'  第{attempt}次连接...', end=' ')
            if success:
                print('成功！')
                return True
            else:
                print('失败')
                if attempt >= max_retries:
                    print('超过最大重试次数，放弃')
                    return False

    try_connect()


# ============================================================
# while...else（和 for...else 一样，break 不触发 else）
# ============================================================
def while_else():
    # 查找第一个能被 7 整除的数
    n = 1
    while n <= 50:
        if n % 7 == 0:
            print(f'找到: {n}')
            break
        n += 1
    else:
        print('50以内没有')   # 没触发 break 才执行

    # 密码验证模拟
    passwords = ['wrong', 'wrong', 'correct']   # 模拟输入
    idx       = 0
    attempts  = 3

    while idx < attempts:
        pwd = passwords[idx]; idx += 1
        print(f'输入密码: {pwd}')
        if pwd == 'correct':
            print('验证通过')
            break
        print('密码错误，剩余次数:', attempts - idx)
    else:
        print('账号已锁定')


# ============================================================
# ★ 实用场景：轮询 / 等待
# ============================================================
def polling_demo():
    import time

    # 场景：等待某个条件满足（模拟，用计数代替真实等待）
    counter    = 0
    max_checks = 5

    print('轮询检查服务状态...')
    while counter < max_checks:
        counter += 1
        # 模拟：第3次检查时服务上线
        service_up = (counter == 3)
        print(f'  第{counter}次检查...', end=' ')
        if service_up:
            print('服务已上线 ✓')
            break
        print('未就绪，等待...')
        # 真实场景这里会 time.sleep(5)
    else:
        print('超时，服务未启动')


# ============================================================
# 常见陷阱：死循环
# ============================================================
def pitfalls():
    print('''
    常见死循环原因：

    1. 忘记更新循环变量
       i = 0
       while i < 10:
           print(i)
           # 忘记写 i += 1 → 死循环

    2. 条件永远为 True
       while True:
           do_something()
           # 忘记 break → 死循环

    3. 浮点数累加误差
       x = 0.0
       while x != 1.0:    # 可能永远不等于 1.0！
           x += 0.1
       # 正确做法：while x < 1.0

    调试技巧：
    - 加计数器限制最大循环次数
    - PyCharm 调试模式逐步执行
    - 打印循环变量观察变化
    ''')


if __name__ == '__main__':
    print('=' * 45)
    print('基础 while')
    basic_while()

    print('=' * 45)
    print('★ while True + break')
    infinite_loop()

    print('=' * 45)
    print('while...else')
    while_else()

    print('=' * 45)
    print('★ 轮询场景')
    polling_demo()

    print('=' * 45)
    print('常见陷阱')
    pitfalls()
