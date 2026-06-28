# Lesson 8.4 - logging 模块
# ★★ 核心概念，Python 日志管理

"""
logging 模块提供了强大的日志记录功能。
本文档涵盖：
1. logging 基础配置
2. 日志级别
3. FileHandler 文件处理
4. RotatingFileHandler 日志轮转
5. 格式化输出
"""

import logging
import logging.handlers
import os

# ===== 1. logging 基础配置 =====

"""
logging 是 Python 内置的日志记录模块
默认配置：WARNING 及以上级别才记录
"""

print("=== 1. logging 基础配置 ===")

# 使用 logging.basicConfig() 配置
logging.basicConfig(
    level=logging.INFO,  # 设置日志级别
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # 格式化
    datefmt='%Y-%m-%d %H:%M:%S'  # 日期格式
)

logger = logging.getLogger(__name__)
print(f"日志记录器: {logger.name}")

# 记录不同级别的日志
logger.debug("这是一条 DEBUG 级别的日志")
logger.info("这是一条 INFO 级别的日志")
logger.warning("这是一条 WARNING 级别的日志")
logger.error("这是一条 ERROR 级别的日志")
logger.critical("这是一条 CRITICAL 级别的日志")

# ===== 2. 日志级别 =====

"""
日志级别（从低到高）：
DEBUG - 调试信息
INFO - 一般信息
WARNING - 警告信息
ERROR - 错误信息
CRITICAL - 严重错误
"""

print("\n=== 2. 日志级别 ===")

# 设置不同的日志级别
for level, name in [
    (logging.DEBUG, "DEBUG"),
    (logging.INFO, "INFO"),
    (logging.WARNING, "WARNING"),
    (logging.ERROR, "ERROR"),
    (logging.CRITICAL, "CRITICAL")
]:
    # 临时设置日志级别
    logging.basicConfig(level=level, force=True)

    logger = logging.getLogger(f"test_{name}")
    logger.log(level, f"测试 {name} 级别的日志")

# ===== 3. 自定义日志配置 =====

"""
创建多个日志记录器
每个记录器可以有不同的配置
"""

print("\n=== 3. 自定义日志配置 ===")

# 创建根日志记录器
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

# 创建文件处理器
file_handler = logging.FileHandler('application.log')
file_handler.setLevel(logging.DEBUG)

# 创建控制台处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# 创建格式化器
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# 添加处理器到根日志记录器
root_logger.addHandler(file_handler)
root_logger.addHandler(console_handler)

# 创建特定模块的日志记录器
app_logger = logging.getLogger('myapp')
app_logger.setLevel(logging.INFO)

# 添加处理器
app_logger.addHandler(file_handler)
app_logger.addHandler(console_handler)

# 记录日志
app_logger.info("应用启动")
app_logger.warning("检测到系统负载较高")
app_logger.error("数据库连接失败")

# 清理处理器
root_logger.removeHandler(file_handler)
root_logger.removeHandler(console_handler)


# ===== 4. FileHandler 文件处理 =====

"""
FileHandler 将日志写入文件
可以指定文件模式和编码
"""

print("\n=== 4. FileHandler 文件处理 ===")

# 创建文件处理器
file_handler = logging.FileHandler('test.log', mode='a', encoding='utf-8')
file_handler.setLevel(logging.INFO)

# 创建格式化器
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# 创建日志记录器
logger = logging.getLogger('file_handler_test')
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

# 记录日志
logger.info("这是第一条日志")
logger.warning("这是第二条日志")
logger.error("这是第三条日志")

# 验证文件已创建
if os.path.exists('test.log'):
    print(f"日志文件已创建: test.log")
    with open('test.log', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        print(f"日志行数: {len(lines)}")
        for line in lines:
            print(f"  {line.strip()}")

# 清理
logger.removeHandler(file_handler)
if os.path.exists('test.log'):
    os.remove('test.log')


# ===== 5. RotatingFileHandler 日志轮转 =====

"""
RotatingFileHandler 可以设置日志文件大小限制
超过限制后自动轮转日志文件
"""

print("\n=== 5. RotatingFileHandler 日志轮转 ===")

# 创建轮转日志处理器
rotating_handler = logging.handlers.RotatingFileHandler(
    'rotating.log',
    maxBytes=1024,  # 最大 1KB
    backupCount=3   # 保留 3 个备份
)

rotating_handler.setLevel(logging.INFO)
rotating_handler.setFormatter(logging.Formatter('%(message)s'))

logger = logging.getLogger('rotating_test')
logger.setLevel(logging.INFO)
logger.addHandler(rotating_handler)

# 记录多条日志
for i in range(10):
    logger.info(f"日志消息 {i+1}")

print(f"\n日志轮转测试完成，生成文件:")
print(f"  rotating.log - 当前日志")
print(f"  rotating.log.1 - 备份 1")
print(f"  rotating.log.2 - 备份 2")
print(f"  rotating.log.3 - 备份 3")

# 检查生成的文件
for i in range(4):
    filename = f"rotating.log.{i}" if i > 0 else "rotating.log"
    if os.path.exists(filename):
        size = os.path.getsize(filename)
        print(f"  {filename}: {size} 字节")

# 清理
logger.removeHandler(rotating_handler)
for i in range(4):
    filename = f"rotating.log.{i}" if i > 0 else "rotating.log"
    if os.path.exists(filename):
        os.remove(filename)


# ===== 6. 日志格式化 =====

"""
自定义日志格式
使用 %(levelname)s, %(message)s, %(asctime)s 等占位符
"""

print("\n=== 6. 日志格式化 ===")

# 自定义格式
format1 = '%(asctime)s [%(levelname)s] %(message)s'
format2 = '%(name)s - %(funcName)s - %(lineno)d - %(message)s'

# 创建处理器
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter(format1))
logger = logging.getLogger('format_test')
logger.setLevel(logging.INFO)
logger.addHandler(ch)

logger.info("标准格式: INFO")
logger.error("标准格式: ERROR")

ch.setFormatter(logging.Formatter(format2))
logger.info("详细格式: INFO")
logger.error("详细格式: ERROR")

# 自定义格式化器
class CustomFormatter(logging.Formatter):
    """自定义格式化器"""

    def format(self, record):
        """格式化日志记录"""
        return f"🔧 {record.levelname} 🔧 - {record.message} - 行: {record.lineno}"


ch = logging.StreamHandler()
ch.setFormatter(CustomFormatter())
logger = logging.getLogger('custom_format_test')
logger.setLevel(logging.INFO)
logger.addHandler(ch)

logger.info("自定义格式: INFO")
logger.error("自定义格式: ERROR")


# ===== 7. 日志过滤器 =====

"""
日志过滤器可以过滤特定的日志记录
"""

print("\n=== 7. 日志过滤器 ===")

class FilterByLevel(logging.Filter):
    """按级别过滤"""

    def __init__(self, min_level=logging.INFO):
        self.min_level = min_level
        super().__init__()

    def filter(self, record):
        """过滤记录"""
        return record.levelno >= self.min_level


# 创建处理器
ch = logging.StreamHandler()
ch.addFilter(FilterByLevel(logging.WARNING))
logger = logging.getLogger('filter_test')
logger.setLevel(logging.INFO)
logger.addHandler(ch)

logger.info("这不会被过滤 - INFO")
logger.warning("这会被过滤 - WARNING")
logger.error("这会被过滤 - ERROR")


# ===== 8. 日志上下文管理 =====

"""
使用上下文管理器封装日志配置
"""

class LogContext:
    """日志上下文管理器"""

    def __init__(self, name, level=logging.INFO):
        self.name = name
        self.level = level
        self.logger = None
        self.old_level = None

    def __enter__(self):
        """进入上下文"""
        self.logger = logging.getLogger(self.name)
        self.old_level = self.logger.level
        self.logger.setLevel(self.level)
        return self.logger

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文"""
        if self.logger:
            self.logger.setLevel(self.old_level)
        return False


# 使用上下文管理器
with LogContext('context_test', logging.DEBUG) as logger:
    logger.debug("DEBUG 级别日志")
    logger.info("INFO 级别日志")
    logger.warning("WARNING 级别日志")


# ===== 9. 实战应用 - 日志配置 =====

class LoggerConfig:
    """日志配置类"""

    def __init__(self, log_dir="logs", app_name="myapp"):
        self.log_dir = log_dir
        self.app_name = app_name
        self.logger = None
        self._setup_logging()

    def _setup_logging(self):
        """设置日志"""
        # 创建日志目录
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        # 创建文件处理器
        log_file = os.path.join(self.log_dir, f"{self.app_name}.log")
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)

        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # 创建格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # 创建日志记录器
        self.logger = logging.getLogger(self.app_name)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        # 避免重复添加处理器
        self.logger.propagate = False

    def log_info(self, message):
        """记录信息日志"""
        self.logger.info(message)

    def log_warning(self, message):
        """记录警告日志"""
        self.logger.warning(message)

    def log_error(self, message):
        """记录错误日志"""
        self.logger.error(message)

    def log_debug(self, message):
        """记录调试日志"""
        self.logger.debug(message)


# 测试日志配置
logger = LoggerConfig(app_name="应用程序")

logger.log_info("应用启动")
logger.log_warning("系统负载较高")
logger.log_error("数据库连接失败")

logger.log_debug("调试信息")

print(f"\n日志已写入: logs/applications.log")


# ===== 10. 日志最佳实践 =====

"""
最佳实践：
1. 使用 logging 而不是 print
2. 为不同的模块使用不同的 logger
3. 设置合适的日志级别
4. 使用格式化的日志输出
5. 使用文件处理器和 RotatingFileHandler
6. 在生产环境中禁用 DEBUG 日志
7. 定期清理旧日志文件
"""

# 清理测试文件
if os.path.exists("application.log"):
    os.remove("application.log")

if os.path.exists("rotating.log"):
    os.remove("rotating.log")

for i in range(4):
    filename = f"rotating.log.{i}"
    if os.path.exists(filename):
        os.remove(filename)

shutil.rmtree("logs", ignore_errors=True)
