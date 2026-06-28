# Lesson 7.4 - 属性和装饰器
# ★★★ 核心概念，Python 高级特性

"""
@property 装饰器允许将方法转换为属性访问
类方法 (classmethod) 和静态方法 (staticmethod)
__slots__ 内存优化
"""

# ===== 1. @property 装饰器 =====

"""
@property 将方法转换为属性访问
通过 getter/setter 方法实现属性的访问和修改
"""

class BankAccount:
    """银行账户类 - 使用 @property"""

    def __init__(self, account_number, owner, initial_balance=0):
        self.account_number = account_number
        self.owner = owner
        self._balance = initial_balance  # 私有属性

    @property
    def balance(self):
        """获取余额 - getter"""
        return self._balance

    @balance.setter
    def balance(self, value):
        """设置余额 - setter"""
        if value >= 0:
            self._balance = value
        else:
            print("余额不能为负数")

    @property
    def is_active(self):
        """获取账户是否激活 - getter"""
        return self._balance > 0

    def deposit(self, amount):
        """存款方法"""
        if amount > 0:
            self._balance += amount
            print(f"存款 {amount}，当前余额: {self._balance}")
        else:
            print("存款金额必须为正数")

    def withdraw(self, amount):
        """取款方法"""
        if amount > 0:
            if amount <= self._balance:
                self._balance -= amount
                print(f"取款 {amount}，当前余额: {self._balance}")
            else:
                print("余额不足")
        else:
            print("取款金额必须为正数")


print("=== 1. @property 装饰器 ===")

account = BankAccount("123456", "张三", 1000)
print(f"账户号: {account.account_number}")
print(f"所有者: {account.owner}")
print(f"初始余额: {account.balance}")

# 通过方法存款
account.deposit(500)
print(f"存款后余额: {account.balance}")

# 通过属性设置余额
account.balance = 2000
print(f"设置后余额: {account.balance}")

# 尝试设置负数余额
account.balance = -100

print(f"当前余额: {account.balance}")
print(f"账户激活: {account.is_active}")


# ===== 2. @classmethod =====

"""
@classmethod 定义类方法
第一个参数是类本身 (cls)
用于操作类，而不是实例
"""

class Student:
    """学生类"""

    # 类属性
    school = "清华大学"
    total_students = 0

    def __init__(self, name, major):
        self.name = name
        self.major = major
        Student.total_students += 1

    @classmethod
    def get_school(cls):
        """获取学校名称 - 类方法"""
        return cls.school

    @classmethod
    def set_school(cls, new_school):
        """设置学校名称 - 类方法"""
        cls.school = new_school

    @classmethod
    def create_student(cls, name, major):
        """创建学生 - 类方法"""
        return cls(name, major)

    @classmethod
    def get_total_students(cls):
        """获取学生总数 - 类方法"""
        return cls.total_students

    @staticmethod
    def is_valid_name(name):
        """验证姓名 - 静态方法"""
        return len(name) > 0 and len(name) < 50

    def __str__(self):
        return f"学生: {self.name}, 专业: {self.major}, 学校: {self.school}"


print("\n=== 2. @classmethod ===")

print(f"学校: {Student.get_school()}")
print(f"学生总数: {Student.get_total_students()}")

s1 = Student("张三", "计算机科学")
s2 = Student("李四", "软件工程")

print(f"学校: {Student.get_school()}")
print(f"学生总数: {Student.get_total_students()}")

# 使用类方法创建实例
s3 = Student.create_student("王五", "数学")
print(f"\n创建的学生: {s3}")

# 使用静态方法验证姓名
print(f"\n姓名验证:")
print(f"  张三: {Student.is_valid_name('张三')}")
print(f"  abc: {Student.is_valid_name('abc')}")
print(f"  a"*51: {Student.is_valid_name('a' * 51)}")

# 修改学校
Student.set_school("北京大学")
print(f"\n修改学校后:")
print(f"  s1 学校: {s1}")
print(f"  s2 学校: {s2}")
print(f"  全局学校: {Student.get_school()}")


# ===== 3. @staticmethod =====

"""
@staticmethod 定义静态方法
不需要实例或类，像普通函数一样使用
"""

class Calculator:
    """计算器类"""

    @staticmethod
    def add(a, b):
        """加法"""
        return a + b

    @staticmethod
    def subtract(a, b):
        """减法"""
        return a - b

    @staticmethod
    def multiply(a, b):
        """乘法"""
        return a * b

    @staticmethod
    def divide(a, b):
        """除法"""
        if b == 0:
            raise ValueError("除数不能为零")
        return a / b

    @staticmethod
    def is_even(n):
        """判断是否为偶数"""
        return n % 2 == 0

    @classmethod
    def calculate_power(cls, base, exponent):
        """计算幂 - 使用类方法"""
        result = 1
        for _ in range(exponent):
            result *= base
        return result


print("\n=== 3. @staticmethod ===")

print(f"2 + 3 = {Calculator.add(2, 3)}")
print(f"2 - 3 = {Calculator.subtract(2, 3)}")
print(f"2 * 3 = {Calculator.multiply(2, 3)}")
print(f"2 / 3 = {Calculator.divide(2, 3):.2f}")

print(f"\n偶数判断:")
print(f"  2: {Calculator.is_even(2)}")
print(f"  3: {Calculator.is_even(3)}")

print(f"\n幂运算:")
print(f"  2^10 = {Calculator.calculate_power(2, 10)}")


# ===== 4. __slots__ 内存优化 =====

"""
__slots__ 定义类的属性
可以节省内存和限制实例属性
"""

class Point:
    """点类 - 使用 __slots__"""

    __slots__ = ['x', 'y']

    def __init__(self, x, y):
        self.x = x
        self.y = y


print("\n=== 4. __slots__ 内存优化 ===")

# 创建多个点对象
points = [Point(i, i*2) for i in range(1000)]

print(f"创建了 {len(points)} 个点")

# 查看内存占用
import sys
point = Point(10, 20)
print(f"单个 Point 对象大小: {sys.getsizeof(point)} 字节")

# 没有使用 __slots__
class PointWithoutSlots:
    def __init__(self, x, y):
        self.x = x
        self.y = y

point_no_slots = PointWithoutSlots(10, 20)
print(f"PointWithoutSlots 对象大小: {sys.getsizeof(point_no_slots)} 字节")


# ===== 5. 类方法、静态方法和实例方法的区别 =====

class Service:
    """服务类"""

    def __init__(self, name):
        self.name = name

    # 实例方法
    def instance_method(self):
        return f"实例方法: {self.name}"

    # 类方法
    @classmethod
    def class_method(cls, name):
        return f"类方法: {cls.name} - {name}"

    # 静态方法
    @staticmethod
    def static_method(name):
        return f"静态方法: {name}"

    # 属性方法
    @property
    def name_upper(self):
        return self.name.upper()


print("\n=== 5. 三种方法的区别 ===")

service = Service("示例服务")

# 调用实例方法
print(service.instance_method())

# 调用类方法
print(Service.class_method("调用"))

# 调用静态方法
print(Service.static_method("调用"))

# 调用属性方法
print(f"大写名称: {service.name_upper}")


# ===== 6. 属性访问的层级 =====

"""
@property, @classmethod, @staticmethod 可以嵌套使用
"""

class Base:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


class Derived(Base):
    def __init__(self, value, multiplier):
        super().__init__(value)
        self.multiplier = multiplier

    @property
    def value(self):
        """重写父类的属性"""
        return super().value * self.multiplier

    @value.setter
    def value(self, new_value):
        super().value = new_value / self.multiplier


print("\n=== 6. 属性访问的层级 ===")

derived = Derived(100, 2)
print(f"derived.value = {derived.value}")

derived.value = 200
print(f"设置后: {derived.value}")

# 通过 super() 访问父类
print(f"原始值: {derived._value}")


# ===== 7. 使用 @property 实现复杂逻辑 =====

class Temperature:
    """温度类"""

    def __init__(self, celsius):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        self._celsius = value

    @property
    def fahrenheit(self):
        """摄氏度转华氏度"""
        return self._celsius * 9/5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value):
        """华氏度转摄氏度"""
        self._celsius = (value - 32) * 5/9

    @property
    def kelvin(self):
        """摄氏度转开尔文"""
        return self._celsius + 273.15

    def __str__(self):
        return f"{self.celsius:.2f}°C = {self.fahrenheit:.2f}°F = {self.kelvin:.2f}K"


print("\n=== 7. 使用 @property 实现复杂逻辑 ===")

temp = Temperature(25)
print(f"初始温度: {temp}")

temp.celsius = 30
print(f"设置摄氏度: {temp}")

temp.fahrenheit = 100
print(f"设置华氏度: {temp}")

print(f"\n温度转换:")
print(f"25°C = {temp.celsius}°C")
print(f"25°C = {temp.fahrenheit:.2f}°F")
print(f"25°C = {temp.kelvin:.2f}K")


# ===== 8. 实战应用 - 用户验证 =====

class User:
    """用户类 - 使用 @property 验证"""

    def __init__(self, username, email, password):
        self._username = None
        self._email = None
        self._password = None

        self.username = username
        self.email = email
        self.password = password

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        if len(value) >= 3 and len(value) <= 20:
            self._username = value
        else:
            raise ValueError("用户名长度必须在 3-20 个字符之间")

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if '@' in value and '.' in value:
            self._email = value
        else:
            raise ValueError("无效的邮箱格式")

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        if len(value) >= 8:
            self._password = value
        else:
            raise ValueError("密码长度至少为 8 个字符")

    def __str__(self):
        return f"用户: {self.username}, 邮箱: {self.email}"


print("\n=== 8. 实战应用 - 用户验证 ===")

try:
    user = User("张三", "zhangsan@example.com", "password123")
    print(f"创建用户: {user}")
except ValueError as e:
    print(f"错误: {e}")

try:
    user2 = User("ab", "invalid-email", "123")
    print(f"创建用户: {user2}")
except ValueError as e:
    print(f"错误: {e}")

try:
    user3 = User("张三", "zhangsan@example.com", "1234567")
    print(f"创建用户: {user3}")
except ValueError as e:
    print(f"错误: {e}")

# 成功创建
user4 = User("张三", "zhangsan@example.com", "password123")
print(f"\n创建用户: {user4}")
