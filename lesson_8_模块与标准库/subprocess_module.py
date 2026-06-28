# Lesson 8.3 - subprocess 模块
# ★★ 核心概念，Python 运维中执行外部命令

"""
subprocess 模块用于生成子进程、执行系统命令。
本文档涵盖：
1. subprocess.run() 基础用法
2. subprocess.Popen() 高级用法
3. 捕获输出（stdout/stderr）
4. 管道
5. 超时控制
6. shell=True 的安全陷阱
"""

import subprocess
import shlex

# ===== 1. subprocess.run() 基础用法 =====

"""
subprocess.run() 是最常用的函数
执行命令并返回 CompletedProcess 对象
"""

print("=== 1. subprocess.run() 基础用法 ===")

# 执行简单的系统命令
result = subprocess.run(["echo", "Hello, World!"])
print(f"命令: echo Hello, World!")
print(f"返回码: {result.returncode}")

# 执行带参数的命令
result = subprocess.run(["python", "--version"])
print(f"\nPython 版本:")
print(f"  命令: python --version")
print(f"  返回码: {result.returncode}")
print(f"  标准输出: {result.stdout.decode().strip()}")

# 执行有返回值的命令
result = subprocess.run(["python", "-c", "print('Hello from Python')"])
print(f"\n命令: python -c 'print(\"Hello from Python\")'")
print(f"  返回码: {result.returncode}")
print(f"  输出: {result.stdout.decode().strip()}")

# ===== 2. 捕获标准输出和错误 =====

"""
使用 capture_output=True 捕获输出
stderr=subprocess.PIPE 捕获错误输出
"""

print("\n=== 2. 捕获标准输出和错误 ===")

# 捕获标准输出
result = subprocess.run(
    ["python", "-c", "print('标准输出'); print('错误输出', file=sys.stderr)"],
    capture_output=True,
    text=True
)

print(f"命令: python -c 'print(标准输出); print(错误输出, file=sys.stderr)'")
print(f"  返回码: {result.returncode}")
print(f"  标准输出: {result.stdout}")
print(f"  错误输出: {result.stderr}")

# 捕获错误（模拟）
result = subprocess.run(
    ["python", "-c", "import nonexistent_module"],
    capture_output=True,
    text=True
)

print(f"\n命令: import nonexistent_module")
print(f"  返回码: {result.returncode}")
print(f"  标准输出: {result.stdout}")
print(f"  错误输出: {result.stderr}")

# 获取 stdout 和 stderr
result = subprocess.run(
    ["ls", "-la"],
    capture_output=True,
    text=True
)

print(f"\n命令: ls -la")
print(f"  输出行数: {len(result.stdout.splitlines())}")
print(f"  错误输出: {result.stderr if result.stderr else '(无)'}")


# ===== 3. subprocess.Popen() 高级用法 =====

"""
subprocess.Popen() 提供更灵活的控制
可以实时读取输出
"""

print("\n=== 3. subprocess.Popen() 高级用法 ===")

# 创建进程
process = subprocess.Popen(
    ["python", "-c", "import time; print('开始'); time.sleep(1); print('结束')"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

print(f"进程已启动: PID={process.pid}")

# 读取输出
while True:
    output = process.stdout.readline()
    if output == '' and process.poll() is not None:
        break
    if output:
        print(f"  {output.strip()}")

# 等待进程完成
returncode = process.wait()
print(f"进程完成，返回码: {returncode}")

# 使用 communicate() 一次性获取所有输出
result = subprocess.run(
    ["python", "-c", "print('Line 1'); print('Line 2'); print('Line 3')"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

print(f"\n命令: 多行输出")
print(f"  输出: {result.stdout}")
print(f"  错误: {result.stderr}")

# ===== 4. 管道和重定向 =====

"""
使用 subprocess.PIPE 创建管道
使用 > 和 2> 重定向输出
"""

print("\n=== 4. 管道和重定向 ===")

# 管道：一个命令的输出作为另一个命令的输入
result = subprocess.run(
    ["cat", "README.md"],  # 假设文件存在，实际需要创建
    stdout=subprocess.PIPE,
    text=True
)
print(f"cat README.md:")
print(f"  输出行数: {len(result.stdout.splitlines())}")

# 重定向：将输出写入文件
with open("output.txt", 'w') as f:
    subprocess.run(["ls", "-la"], stdout=f, stderr=subprocess.PIPE)

print(f"\n命令: ls -la > output.txt")
print(f"  文件已创建: {os.path.exists('output.txt')}")

# 读取输出文件
with open("output.txt", 'r') as f:
    lines = f.readlines()
    print(f"  输出行数: {len(lines)}")

# 重定向错误到文件
with open("error.txt", 'w') as f:
    subprocess.run(["python", "-c", "import nonexistent_module"], stderr=f)

print(f"\n命令: python -c import nonexistent_module 2> error.txt")
print(f"  错误文件已创建: {os.path.exists('error.txt')}")


# ===== 5. 超时控制 =====

"""
使用 timeout 参数设置超时
超时后抛出 subprocess.TimeoutExpired 异常
"""

print("\n=== 5. 超时控制 ===")

# 模拟长时间运行的命令
try:
    print("执行长时间运行的命令（5秒）...")
    result = subprocess.run(
        ["python", "-c", "import time; time.sleep(5); print('完成')"],
        timeout=2,  # 2秒超时
        capture_output=True,
        text=True
    )
    print(f"命令完成: {result.stdout}")
except subprocess.TimeoutExpired as e:
    print(f"命令超时！")
    print(f"  异常信息: {e}")
    print(f"  stdout: {e.stdout}")
    print(f"  stderr: {e.stderr}")

# 设置不同的超时时间
try:
    print("\n执行长时间运行的命令（3秒，设置10秒）...")
    result = subprocess.run(
        ["python", "-c", "import time; time.sleep(3); print('完成')"],
        timeout=10,  # 10秒超时
        capture_output=True,
        text=True
    )
    print(f"命令完成: {result.stdout}")
except subprocess.TimeoutExpired as e:
    print(f"命令超时！")

# ===== 6. shell=True 的安全陷阱 =====

"""
使用 shell=True 非常危险，容易受命令注入攻击
尽量使用列表形式调用命令
"""

print("\n=== 6. shell=True 的安全陷阱 ===")

# 危险：shell=True + 用户输入
user_input = "test; rm -rf /"  # 危险的输入

print(f"用户输入: {user_input}")

# 使用列表（安全）
result = subprocess.run(
    ["echo", user_input],  # 安全
    capture_output=True,
    text=True
)
print(f"\n安全方式（列表）:")
print(f"  命令: echo {user_input}")
print(f"  输出: {result.stdout}")

# 危险：shell=True + 用户输入
try:
    result = subprocess.run(
        f"echo {user_input}",  # 不安全
        shell=True,
        capture_output=True,
        text=True
    )
    print(f"\n危险方式（shell=True）:")
    print(f"  命令: echo {user_input}")
    print(f"  输出: {result.stdout}")
except Exception as e:
    print(f"错误: {e}")

# 使用 shlex.quote() 对用户输入进行转义（相对安全）
escaped_input = shlex.quote(user_input)
result = subprocess.run(
    f"echo {escaped_input}",
    shell=True,
    capture_output=True,
    text=True
)
print(f"\n使用 shlex.quote() 转义:")
print(f"  转义后: {escaped_input}")
print(f"  输出: {result.stdout}")

# ===== 7. 环境变量 =====

"""
可以设置子进程的环境变量
"""

print("\n=== 7. 环境变量 ===")

# 创建环境变量
env = os.environ.copy()
env["CUSTOM_VAR"] = "custom_value"

result = subprocess.run(
    ["python", "-c", "import os; print(os.environ.get('CUSTOM_VAR'))"],
    env=env,
    capture_output=True,
    text=True
)

print(f"设置自定义环境变量:")
print(f"  输出: {result.stdout}")

# 使用特定的环境变量
env = {"PATH": "/usr/bin:/bin"}
result = subprocess.run(
    ["echo", "Hello"],
    env=env,
    capture_output=True,
    text=True
)
print(f"\n使用自定义 PATH:")
print(f"  输出: {result.stdout}")

# ===== 8. 实战应用 - 系统监控 =====

class CommandRunner:
    """命令运行器"""

    def __init__(self):
        self.executed_commands = []

    def run_command(self, command, capture_output=True, timeout=10):
        """运行命令"""
        print(f"\n执行命令: {command}")

        try:
            result = subprocess.run(
                command,
                capture_output=capture_output,
                text=True,
                timeout=timeout
            )

            self.executed_commands.append({
                "command": command,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            })

            return {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            }

        except subprocess.TimeoutExpired as e:
            print(f"超时: {e}")
            return {
                "returncode": -1,
                "stdout": e.stdout,
                "stderr": e.stderr,
                "error": "Timeout"
            }

        except Exception as e:
            print(f"错误: {e}")
            return {
                "returncode": -1,
                "stdout": "",
                "stderr": str(e),
                "error": str(e)
            }

    def get_command_history(self):
        """获取命令历史"""
        return self.executed_commands

    def get_successful_commands(self):
        """获取成功的命令"""
        return [cmd for cmd in self.executed_commands if cmd["returncode"] == 0]

    def get_failed_commands(self):
        """获取失败的命令"""
        return [cmd for cmd in self.executed_commands if cmd["returncode"] != 0]


# 测试命令运行器
runner = CommandRunner()

# 执行成功命令
runner.run_command("echo '成功命令1'", timeout=5)

# 执行失败命令
runner.run_command("python -c 'import nonexistent'", timeout=5)

# 执行超时命令
runner.run_command("python -c 'import time; time.sleep(5); print(\"完成\")'", timeout=2)

# 执行多行命令
runner.run_command("python -c 'print(\"Line 1\"); print(\"Line 2\")'", timeout=5)

# 分析结果
print("\n=== 命令运行历史 ===")
print(f"总命令数: {len(runner.get_command_history())}")
print(f"成功命令: {len(runner.get_successful_commands())}")
print(f"失败命令: {len(runner.get_failed_commands())}")

# 显示成功的命令
print("\n成功的命令:")
for cmd in runner.get_successful_commands():
    print(f"  {cmd['command']}")
    print(f"    返回码: {cmd['returncode']}")
    print(f"    输出: {cmd['stdout'].strip()}")

# 显示失败的命令
print("\n失败的命令:")
for cmd in runner.get_failed_commands():
    print(f"  {cmd['command']}")
    print(f"  错误: {cmd.get('error', cmd['stderr']).strip()}")


# ===== 9. 执行计划任务 =====

class TaskExecutor:
    """任务执行器"""

    @staticmethod
    def execute_task(task_name, command, expected_output=None):
        """
        执行计划任务
        :param task_name: 任务名称
        :param command: 命令
        :param expected_output: 预期的输出
        """
        print(f"\n执行任务: {task_name}")
        print(f"  命令: {command}")

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=30
            )

            if expected_output and expected_output in result.stdout:
                print(f"  状态: 成功 ✅")
                print(f"  输出: {result.stdout.strip()}")
                return True
            elif result.returncode == 0:
                print(f"  状态: 成功 ✅")
                print(f"  输出: {result.stdout.strip()}")
                return True
            else:
                print(f"  状态: 失败 ❌")
                print(f"  错误: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            print(f"  状态: 超时 ❌")
            return False
        except Exception as e:
            print(f"  状态: 错误 ❌")
            print(f"  错误: {e}")
            return False


# 测试任务执行器
executor = TaskExecutor()

# 测试成功命令
executor.execute_task("列出当前目录", "ls -la")

# 测试失败命令
executor.execute_task("测试不存在的命令", "this-command-does-not-exist")

# 测试长时间运行的命令
executor.execute_task("等待5秒", "python -c 'import time; time.sleep(5)'")


# ===== 10. subprocess 模块最佳实践 =====

"""
最佳实践：
1. 优先使用 subprocess.run()，它更简单
2. 使用列表形式调用命令（安全）
3. 如果必须使用 shell=True，使用 shlex.quote() 转义输入
4. 始终设置 timeout
5. 捕获并检查返回码
6. 记录命令执行结果
"""

def safe_shell_command(command, input_data=None):
    """
    安全执行 shell 命令
    使用 shlex.quote() 转义输入
    """
    try:
        # 转义命令中的特殊字符
        escaped_command = shlex.quote(command)

        # 执行命令
        result = subprocess.run(
            escaped_command,
            shell=True,
            input=input_data,
            capture_output=True,
            text=True,
            timeout=30
        )

        return {
            "success": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except subprocess.TimeoutExpired as e:
        return {
            "success": False,
            "error": "Timeout",
            "stdout": e.stdout,
            "stderr": e.stderr
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


print("\n=== 10. subprocess 最佳实践 ===")

# 安全执行 shell 命令
result = safe_shell_command("ls -la | head -5")
print(f"安全执行: {result['success']}")
print(f"输出: {result['stdout'].strip()}")

# 清理测试文件
if os.path.exists("output.txt"):
    os.remove("output.txt")

if os.path.exists("error.txt"):
    os.remove("error.txt")
