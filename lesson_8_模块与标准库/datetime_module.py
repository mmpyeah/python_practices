# Lesson 8.5 - datetime 模块
# ★★ 核心概念，Python 时间处理

"""
datetime 模块提供了丰富的时间处理功能。
本文档涵盖：
1. datetime.date - 日期处理
2. datetime.datetime - 日期和时间
3. datetime.timedelta - 时间差
4. 时间戳互转
5. 时区处理（pytz 简介）
6. 格式化
"""

from datetime import date, datetime, timedelta
import time

# ===== 1. datetime.date - 日期处理 =====

"""
date 类用于处理日期
只包含年、月、日
"""

print("=== 1. datetime.date - 日期处理 ===")

# 创建日期
today = date.today()
print(f"今天: {today}")
print(f"类型: {type(today)}")

# 指定日期
birthday = date(1990, 5, 15)
print(f"\n生日: {birthday}")

# 从字符串创建日期
birthday_str = date.fromisoformat("1990-05-15")
print(f"从字符串创建: {birthday_str}")

# 日期操作
tomorrow = today + timedelta(days=1)
yesterday = today - timedelta(days=1)
print(f"\n今天: {today}")
print(f"明天: {tomorrow}")
print(f"昨天: {yesterday}")

# 日期属性
print(f"\n今天的属性:")
print(f"  年份: {today.year}")
print(f"  月份: {today.month}")
print(f"  日期: {today.day}")
print(f"  星期: {today.weekday()} ({['周一', '周二', '周三', '周四', '周五', '周六', '周日'][today.weekday()]})")
print(f"  ISO 日期: {today.isoformat()}")

# 日期计算
print(f"\n日期计算:")
print(f"  明天的年份: {today.year + 1}")
print(f"  100 天后: {today + timedelta(days=100)}")
print(f"  1 个月后: {today + timedelta(days=30)}")
print(f"  1 年后: {today + timedelta(days=365)}")

# 日期比较
print(f"\n日期比较:")
d1 = date(2024, 1, 1)
d2 = date(2024, 12, 31)
print(f"  2024-01-01 < 2024-12-31: {d1 < d2}")
print(f"  2024-01-01 == 2024-01-01: {d1 == date(2024, 1, 1)}")

# ===== 2. datetime.datetime - 日期和时间 =====

"""
datetime 类用于处理日期和时间
包含年、月、日、时、分、秒、微秒
"""

print("\n=== 2. datetime.datetime - 日期和时间 ===")

# 创建 datetime
now = datetime.now()
print(f"现在: {now}")
print(f"类型: {type(now)}")

# 指定 datetime
dt = datetime(2024, 1, 1, 12, 30, 45)
print(f"\n指定时间: {dt}")

# 从字符串创建
dt_from_str = datetime.fromisoformat("2024-01-01 12:30:45")
print(f"从字符串创建: {dt_from_str}")

# 当前时间戳
timestamp = time.time()
print(f"\n当前时间戳: {timestamp}")
print(f"时间戳对应的日期: {datetime.fromtimestamp(timestamp)}")

# 从时间戳创建 datetime
dt_from_ts = datetime.fromtimestamp(timestamp)
print(f"从时间戳创建: {dt_from_ts}")

# 时间操作
tomorrow_dt = now + timedelta(days=1)
yesterday_dt = now - timedelta(days=1)
print(f"\n今天: {now}")
print(f"明天: {tomorrow_dt}")
print(f"昨天: {yesterday_dt}")

# 时间属性
print(f"\n当前时间的属性:")
print(f"  年: {now.year}")
print(f"  月: {now.month}")
print(f"  日: {now.day}")
print(f"  时: {now.hour}")
print(f"  分: {now.minute}")
print(f"  秒: {now.second}")
print(f"  微秒: {now.microsecond}")

# ===== 3. datetime.timedelta - 时间差 =====

"""
timedelta 表示时间差
可以用于日期、时间的加减操作
"""

print("\n=== 3. datetime.timedelta - 时间差 ===")

# 创建时间差
td = timedelta(days=1, hours=2, minutes=30, seconds=45)
print(f"时间差: {td}")
print(f"总秒数: {td.total_seconds()}")

# 计算日期差异
start_date = date(2024, 1, 1)
end_date = date(2024, 1, 10)
diff = end_date - start_date
print(f"\n日期差异: {diff}")
print(f"总天数: {diff.days}")

# 时间差运算
td1 = timedelta(days=5)
td2 = timedelta(hours=10)
result = td1 + td2
print(f"\n5天 + 10小时: {result}")

# 常用时间差
print(f"\n常用时间差:")
print(f"  1 天: {timedelta(days=1)}")
print(f"  1 小时: {timedelta(hours=1)}")
print(f"  1 分钟: {timedelta(minutes=1)}")
print(f"  1 秒: {timedelta(seconds=1)}")
print(f"  1 周时间: {timedelta(weeks=1)}")
print(f"  1 个月: {timedelta(days=30)}")

# ===== 4. 时间戳互转 =====

"""
time.time() 返回当前时间戳（秒）
datetime.fromtimestamp() 从时间戳创建 datetime
"""

print("\n=== 4. 时间戳互转 ===")

# 获取当前时间戳
current_timestamp = time.time()
print(f"当前时间戳: {current_timestamp}")
print(f"当前时间: {datetime.fromtimestamp(current_timestamp)}")

# 指定时间戳
specific_timestamp = 1704067200  # 2024-01-01 00:00:00
print(f"\n时间戳 {specific_timestamp} 对应的时间:")
print(f"  日期时间: {datetime.fromtimestamp(specific_timestamp)}")
print(f"  日期: {date.fromtimestamp(specific_timestamp)}")

# 时间戳转字符串
timestamp_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(specific_timestamp))
print(f"\n时间戳转字符串: {timestamp_str}")

# 字符串转时间戳
timestamp_from_str = time.mktime(time.strptime("2024-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"))
print(f"字符串转时间戳: {timestamp_from_str}")

# ===== 5. 时区处理 =====

"""
Python 3.9+ 内置了 ZoneInfo
pytz 是旧版本常用的时区库
"""

print("\n=== 5. 时区处理 ===")

# Python 3.9+ 使用 ZoneInfo
from zoneinfo import ZoneInfo

try:
    # 创建带时区的日期时间
    utc_time = datetime.now(ZoneInfo("UTC"))
    beijing_time = datetime.now(ZoneInfo("Asia/Shanghai"))

    print(f"UTC 时间: {utc_time}")
    print(f"北京时间: {beijing_time}")
    print(f"时区差异: {(beijing_time - utc_time).total_seconds() / 3600} 小时")

except ImportError:
    print("ZoneInfo 不可用（需要 Python 3.9+）")
    print("使用 pytz 替代:")
    try:
        import pytz

        beijing_tz = pytz.timezone("Asia/Shanghai")
        beijing_time = datetime.now(beijing_tz)

        print(f"北京时间: {beijing_time}")
        print(f"时区: {beijing_tz}")

    except ImportError:
        print("pytz 也不可用")


# ===== 6. 格式化 =====

"""
strftime - 将 datetime 格式化为字符串
strptime - 将字符串解析为 datetime
"""

print("\n=== 6. 格式化 ===")

# 当前时间
now = datetime.now()

# 常用格式化字符串
formats = {
    "年份": "%Y",  # 2024
    "月份": "%m",  # 01
    "日期": "%d",  # 01
    "星期": "%A",  # Monday
    "星期缩写": "%a",  # Mon
    "小时": "%H",  # 00-23
    "小时 (12小时制)": "%I",  # 00-12
    "分钟": "%M",  # 00-59
    "秒": "%S",  # 00-59
    "时间戳": "%s",  # 时间戳
}

print("常用格式化字符串:")
for name, fmt in formats.items():
    formatted = now.strftime(fmt)
    print(f"  {name} ({fmt}): {formatted}")

# 自定义格式
custom_format = "%Y-%m-%d %H:%M:%S"
formatted = now.strftime(custom_format)
print(f"\n自定义格式 {custom_format}: {formatted}")

# 解析时间字符串
date_string = "2024-01-01 12:30:45"
parsed = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
print(f"解析时间字符串: {parsed}")

# ===== 7. 实战应用 - 日期计算 =====

class DateCalculator:
    """日期计算类"""

    def __init__(self, start_date=None):
        """初始化日期计算器"""
        self.start_date = start_date if start_date else date.today()

    def days_until(self, target_date):
        """计算到目标日期的天数"""
        if isinstance(target_date, str):
            target_date = date.fromisoformat(target_date)
        return (target_date - self.start_date).days

    def days_since(self, target_date):
        """计算从目标日期过去的天数"""
        if isinstance(target_date, str):
            target_date = date.fromisoformat(target_date)
        return (self.start_date - target_date).days

    def add_months(self, months):
        """增加月份"""
        year = self.start_date.year + (self.start_date.month - 1 + months) // 12
        month = (self.start_date.month - 1 + months) % 12 + 1
        day = self.start_date.day
        return date(year, month, day)

    def add_years(self, years):
        """增加年数"""
        return self.start_date.replace(year=self.start_date.year + years)

    def get_weekday_name(self):
        """获取星期名称"""
        weekdays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        return weekdays[self.start_date.weekday()]


# 测试日期计算器
calc = DateCalculator(date(2024, 6, 1))

print(f"\n=== 7. 实战应用 - 日期计算 ===")
print(f"起始日期: {calc.start_date}")
print(f"星期: {calc.get_weekday_name()}")
print(f"到 2024-12-31 的天数: {calc.days_until('2024-12-31')} 天")
print(f"从 2024-01-01 的天数: {calc.days_since('2024-01-01')} 天")
print(f"增加 6 个月后: {calc.add_months(6)}")
print(f"增加 1 年后: {calc.add_years(1)}")

# ===== 8. 日期日志记录 =====

class LogGenerator:
    """日志生成器"""

    @staticmethod
    def generate_timestamp():
        """生成时间戳"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def generate_date_filename():
        """生成日期文件名"""
        return datetime.now().strftime("%Y%m%d") + ".log"

    @staticmethod
    def generate_log_entry(message, level="INFO"):
        """生成日志条目"""
        return f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [{level}] {message}"

    @staticmethod
    def calculate_age(birthdate_str):
        """计算年龄"""
        birthdate = date.fromisoformat(birthdate_str)
        today = date.today()
        return today.year - birthdate.year - (
            (today.month, today.day) < (birthdate.month, birthdate.day)
        )


# 测试日志生成器
logger = LogGenerator()

print(f"\n=== 8. 实战应用 - 日期日志记录 ===")
print(f"当前时间戳: {logger.generate_timestamp()}")
print(f"日期文件名: {logger.generate_date_filename()}")
print(f"日志条目: {logger.generate_log_entry('应用启动', 'INFO')}")
print(f"年龄计算 (1990-05-15): {logger.calculate_age('1990-05-15')} 岁")


# ===== 9. 日期最佳实践 =====

"""
最佳实践：
1. 使用 datetime.now() 获取当前时间
2. 使用 strftime 格式化时间输出
3. 使用 timedelta 进行日期计算
4. 在日志中使用时间戳
5. 在文件名中使用日期
6. 使用 date.toordinal() 转换为序数
"""

# 清理测试
import shutil
if os.path.exists("logs"):
    shutil.rmtree("logs")
