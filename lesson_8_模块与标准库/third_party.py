# Lesson 8.6 - 第三方库
# ★★ 核心概念，Python 生态和外部工具

"""
Python 有丰富的第三方库生态。
本文档涵盖：
1. pip - 包管理器
2. 虚拟环境
3. requirements.txt - 依赖管理
4. requests - HTTP 请求库
"""

import subprocess
import sys
import json
import os

# ===== 1. pip - 包管理器 =====

"""
pip 是 Python 的包管理器
用于安装、卸载、更新第三方库
"""

print("=== 1. pip - 包管理器 ===")

# 查看已安装的包
print(f"\nPython 版本: {sys.version}")
print(f"pip 版本: {subprocess.run(['pip', '--version'], capture_output=True, text=True).stdout.strip()}")

# 列出已安装的包
print(f"\n已安装的包 ({len(sys.modules)} 个):")
for module_name in sorted(sys.modules.keys())[:10]:
    print(f"  - {module_name}")
if len(sys.modules) > 10:
    print(f"  ... (共 {len(sys.modules)} 个)")

# 搜索包
print(f"\n搜索包 (requests):")
result = subprocess.run(
    ["pip", "search", "requests"],
    capture_output=True,
    text=True,
    timeout=10
)
if result.returncode == 0:
    print(result.stdout[:200])
else:
    print("pip search 可能已被禁用")

# 安装包（示例）
print(f"\n安装包 (示例):")
print("pip install requests")

# 卸载包
print(f"\n卸载包 (示例):")
print("pip uninstall requests")

# 升级包
print(f"\n升级包 (示例):")
print("pip install --upgrade requests")

# ===== 2. 虚拟环境 =====

"""
虚拟环境可以隔离项目依赖
避免不同项目的依赖冲突
"""

print("\n=== 2. 虚拟环境 ===")

# 检查虚拟环境
if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
    print("当前处于虚拟环境")
    print(f"虚拟环境路径: {sys.prefix}")
else:
    print("当前不在虚拟环境中")
    print("虚拟环境路径: 无")

# 创建虚拟环境
print(f"\n创建虚拟环境:")
print("python -m venv myenv")

# 激活虚拟环境
print(f"激活虚拟环境:")
print("Windows: myenv\\Scripts\\activate")
print("Linux/macOS: source myenv/bin/activate")

# 在虚拟环境中安装包
print(f"\n在虚拟环境中安装包:")
print("pip install requests")

# 退出虚拟环境
print(f"\n退出虚拟环境:")
print("deactivate")

# ===== 3. requirements.txt - 依赖管理 =====

"""
requirements.txt 文件列出了项目的所有依赖
可以使用 pip install -r requirements.txt 安装所有依赖
"""

print("\n=== 3. requirements.txt - 依赖管理 ===")

# 创建 requirements.txt
requirements_content = """# 项目依赖列表
# 格式: 包名==版本 或 包名>=版本

# 核心依赖
requests==2.31.0
numpy==1.24.3
pandas==2.0.3

# 开发依赖
pytest==7.4.0
black==23.7.0
mypy==1.5.0

# 可选依赖
pytest-cov==4.1.0
sphinx==6.2.1
"""

requirements_file = "requirements.txt"
with open(requirements_file, 'w') as f:
    f.write(requirements_content)

print(f"已创建 {requirements_file}")
print(f"内容:\n{requirements_content}")

# 生成 requirements.txt（从当前环境）
print(f"\n生成 requirements.txt:")
print("pip freeze > requirements.txt")

# 从 requirements.txt 安装依赖
print(f"\n从 requirements.txt 安装:")
print("pip install -r requirements.txt")

# 生成依赖列表（包含版本）
print(f"\n生成依赖列表（包含版本）:")
result = subprocess.run(
    ["pip", "list", "--format=freeze"],
    capture_output=True,
    text=True
)
requirements_freeze = result.stdout
print(requirements_freeze)

# 清理测试文件
os.remove(requirements_file)


# ===== 4. requests - HTTP 请求库 =====

"""
requests 是一个流行的 HTTP 库
比标准库的 urllib 更简单易用
"""

print("\n=== 4. requests - HTTP 请求库 ===")

try:
    import requests

    print(f"requests 库已安装: {requests.__version__}")

    # ===== 4.1 发送 GET 请求 =====

    # 发送 GET 请求
    response = requests.get("https://httpbin.org/get", params={"key": "value"})

    print(f"\n发送 GET 请求:")
    print(f"  URL: {response.url}")
    print(f"  状态码: {response.status_code}")
    print(f"  响应头: {dict(response.headers)}")

    # 解析 JSON 响应
    if response.status_code == 200:
        data = response.json()
        print(f"  JSON 响应: {data}")

    # ===== 4.2 发送 POST 请求 =====

    # 发送 POST 请求
    payload = {
        "name": "张三",
        "age": 30,
        "email": "zhangsan@example.com"
    }

    response = requests.post("https://httpbin.org/post", json=payload)

    print(f"\n发送 POST 请求:")
    print(f"  URL: {response.url}")
    print(f"  状态码: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"  JSON 响应: {data}")

    # ===== 4.3 处理响应 =====

    # 状态码检查
    if response.status_code == 200:
        print(f"\n请求成功!")
    elif response.status_code == 404:
        print(f"资源不存在 (404)")
    elif response.status_code == 500:
        print(f"服务器错误 (500)")

    # 获取文本响应
    text = response.text
    print(f"\n响应文本长度: {len(text)}")

    # 获取 JSON
    json_data = response.json()
    print(f"JSON 数据: {json_data}")

    # ===== 4.4 处理错误 =====

    # 处理异常
    try:
        response = requests.get("https://httpbin.org/status/404")
        response.raise_for_status()  # 如果状态码不是 200，抛出异常
    except requests.exceptions.HTTPError as e:
        print(f"\nHTTP 错误: {e}")

    except requests.exceptions.ConnectionError as e:
        print(f"\n连接错误: {e}")

    except requests.exceptions.Timeout as e:
        print(f"\n超时错误: {e}")

    except requests.exceptions.RequestException as e:
        print(f"\n请求错误: {e}")

    # ===== 4.5 其他功能 =====

    # 设置请求头
    headers = {
        "User-Agent": "My Python Script/1.0",
        "Accept": "application/json"
    }
    response = requests.get("https://httpbin.org/headers", headers=headers)
    print(f"\n带请求头的响应: {response.json()}")

    # 设置超时
    try:
        response = requests.get("https://httpbin.org/delay/2", timeout=1)
    except requests.exceptions.Timeout:
        print(f"\n请求超时")

    # 文件上传
    files = {
        'file': ('test.txt', '这是一些测试内容', 'text/plain')
    }
    response = requests.post("https://httpbin.org/post", files=files)
    print(f"\n文件上传: {response.json()}")

    # ===== 4.6 会话 =====

    # 使用 Session
    session = requests.Session()
    session.headers.update({"User-Agent": "My Session/1.0"})
    response = session.get("https://httpbin.org/headers")
    print(f"\nSession 响应: {response.json()}")

except ImportError:
    print("requests 库未安装")
    print("安装: pip install requests")


# ===== 5. 第三方库最佳实践 =====

"""
最佳实践：
1. 使用虚拟环境隔离项目依赖
2. 使用 requirements.txt 管理依赖
3. 定期更新依赖库
4. 使用 pip-check 检查依赖冲突
5. 使用环境变量存储敏感信息
6. 只安装必要的库
7. 避免全局安装不必要的库
"""

def install_dependencies(package_names, upgrade=False):
    """安装依赖包"""
    print(f"\n安装依赖包: {package_names}")
    for pkg in package_names:
        print(f"  - {pkg}")

def check_dependencies():
    """检查依赖"""
    print(f"\n检查依赖:")
    print("pip check")

def update_dependencies():
    """更新依赖"""
    print(f"\n更新所有依赖:")
    print("pip install --upgrade -r requirements.txt")


# ===== 6. 实战应用 - HTTP 请求示例 =====

class HttpClient:
    """HTTP 客户端"""

    def __init__(self, base_url, timeout=10):
        """初始化 HTTP 客户端"""
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Python HTTP Client/1.0",
            "Accept": "application/json"
        })

    def get(self, endpoint, params=None):
        """发送 GET 请求"""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"GET 请求失败: {e}")
            return None

    def post(self, endpoint, data=None, json_data=None):
        """发送 POST 请求"""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = self.session.post(url, json=json_data, data=data, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"POST 请求失败: {e}")
            return None

    def close(self):
        """关闭会话"""
        self.session.close()


# 测试 HTTP 客户端
try:
    client = HttpClient("https://httpbin.org", timeout=5)

    print(f"\n=== 6. 实战应用 - HTTP 客户端 ===")

    # GET 请求
    response = client.get("get", params={"key": "value"})
    if response:
        print(f"GET 请求结果: {response['args']}")

    # POST 请求
    payload = {
        "name": "测试",
        "data": "测试数据"
    }
    response = client.post("post", json_data=payload)
    if response:
        print(f"POST 请求结果: {response['json']}")

    client.close()

except ImportError:
    print("requests 库未安装")


# ===== 7. 第三方库版本管理 =====

class PackageManager:
    """包管理器"""

    @staticmethod
    def list_installed_packages():
        """列出已安装的包"""
        print("pip list")

    @staticmethod
    def list_outdated_packages():
        """列出过期的包"""
        print("pip list --outdated")

    @staticmethod
    def freeze_packages():
        """冻结包版本"""
        result = subprocess.run(["pip", "freeze"], capture_output=True, text=True)
        print(result.stdout)

    @staticmethod
    def check_conflicts():
        """检查依赖冲突"""
        result = subprocess.run(["pip", "check"], capture_output=True, text=True)
        if result.stdout:
            print(f"依赖冲突:\n{result.stdout}")
        else:
            print("无依赖冲突")


# 测试包管理器
manager = PackageManager()

print(f"\n=== 7. 第三方库版本管理 ===")

manager.list_installed_packages()
print(f"\n过期的包:")
manager.list_outdated_packages()
print(f"\n包版本:")
manager.freeze_packages()
print(f"\n检查依赖冲突:")
manager.check_conflicts()


# ===== 8. 第三方库推荐 =====

"""
常用的 Python 第三方库：

数据处理：
- pandas: 数据分析
- numpy: 数值计算
- scipy: 科学计算

Web 开发：
- Flask: Web 框架
- Django: 全栈 Web 框架
- FastAPI: 现代 API 框架

爬虫：
- requests: HTTP 请求
- BeautifulSoup: HTML 解析
- Scrapy: 爬虫框架

数据可视化：
- matplotlib: 绘图
- seaborn: 统计可视化
- plotly: 交互式图表

测试：
- pytest: 测试框架
- unittest: 单元测试

数据库：
- SQLAlchemy: ORM
- psycopg2: PostgreSQL
- pymysql: MySQL
"""

print("\n=== 8. 第三方库推荐 ===")

recommended = [
    ("pandas", "数据处理和分析"),
    ("numpy", "数值计算"),
    ("requests", "HTTP 请求"),
    ("Flask", "Web 框架"),
    ("pytest", "测试框架"),
    ("beautifulsoup4", "HTML 解析"),
]

print("推荐安装的库:")
for name, desc in recommended:
    print(f"  {name}: {desc}")
