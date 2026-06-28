# Lesson 7.1 - 类的基础
# ★★★ 核心概念，面向对象编程的基础

"""
类是面向对象编程（OOP）的核心概念。
本文档涵盖：
1. class 定义
2. __init__ 构造函数
3. self 关键字
4. 实例属性 vs 类属性
5. 实例方法
6. 对象创建和使用
"""

# ===== 1. 基本类定义 =====

"""
类是对象的模板，定义了对象的属性和方法
使用 class 关键字定义
"""

class Person:
    """人的类"""

    # 类属性：所有实例共享
    species = "人类"

    def __init__(self, name, age, gender):
        """构造函数：初始化对象"""
        self.name = name  # 实例属性
        self.age = age
        self.gender = gender

    def introduce(self):
        """实例方法：定义对象的行为"""
        return f"我是{self.name}，{self.age}岁，性别{self.gender}"

    def greet(self):
        """打招呼方法"""
        return f"你好，我是{self.name}"


# ===== 2. 创建和使用对象 =====

print("=== 1. 创建和使用对象 ===")

# 创建第一个对象
p1 = Person("张三", 25, "男")
print(f"p1.name = {p1.name}")
print(f"p1.age = {p1.age}")
print(f"p1.gender = {p1.gender}")
print(f"p1.introduce() = {p1.introduce()}")
print(f"p1.greet() = {p1.greet()}")

# 创建第二个对象
p2 = Person("李四", 30, "女")
print(f"\np2.name = {p2.name}")
print(f"p2.age = {p2.age}")
print(f"p2.introduce() = {p2.introduce()}")

# ===== 3. 类属性 vs 实例属性 =====

print("\n=== 2. 类属性 vs 实例属性 ===")

class Student:
    """学生类"""

    # 类属性
    school = "清华大学"
    count = 0

    def __init__(self, name, major):
        # 实例属性
        self.name = name
        self.major = major
        Student.count += 1  # 每次创建实例，计数加1

    def __str__(self):
        return f"学生: {self.name}, 专业: {self.major}"


# 创建实例
s1 = Student("张三", "计算机科学")
s2 = Student("李四", "软件工程")

print(f"s1.school = {s1.school}")
print(f"s2.school = {s2.school}")
print(f"类属性 school = {Student.school}")

print(f"\nschool.count = {s1.count}")
print(f"类属性 count = {Student.count}")

# 类属性是共享的
Student.school = "北京大学"
print(f"\n修改类属性后:")
print(f"s1.school = {s1.school}")
print(f"s2.school = {s2.school}")
print(f"Student.school = {Student.school}")

# 实例属性是独立的
s1.name = "王五"
s2.name = "赵六"
print(f"\n修改实例属性后:")
print(f"s1.name = {s1.name}")
print(f"s2.name = {s2.name}")

# ===== 4. 类方法和实例方法 =====

class BankAccount:
    """银行账户类"""

    # 类属性
    account_count = 0

    def __init__(self, owner, balance=0):
        """构造函数"""
        self.owner = owner
        self.balance = balance
        BankAccount.account_count += 1

    def deposit(self, amount):
        """实例方法：存款"""
        if amount > 0:
            self.balance += amount
            return f"存入 {amount}，当前余额: {self.balance}"
        return "存款金额必须为正数"

    def withdraw(self, amount):
        """实例方法：取款"""
        if amount > 0:
            if amount <= self.balance:
                self.balance -= amount
                return f"取出 {amount}，当前余额: {self.balance}"
            return "余额不足"
        return "取款金额必须为正数"

    def get_balance(self):
        """实例方法：查询余额"""
        return self.balance

    @classmethod
    def get_total_accounts(cls):
        """类方法：获取总账户数"""
        return f"总账户数: {cls.account_count}"

    @classmethod
    def create_account(cls, owner, balance):
        """类方法：创建账户"""
        return cls(owner, balance)

    @staticmethod
    def is_valid_email(email):
        """静态方法：验证邮箱格式"""
        return '@' in email and '.' in email


print("\n=== 3. 类方法和实例方法 ===")

# 使用实例方法
account1 = BankAccount("张三", 1000)
print(f"创建账户: {account1.owner}, 余额: {account1.get_balance()}")

print(account1.deposit(500))
print(account1.withdraw(200))

# 使用类方法
print(BankAccount.get_total_accounts())

# 使用静态方法
print(f"验证邮箱: {BankAccount.is_valid_email('test@example.com')}")
print(f"验证邮箱: {BankAccount.is_valid_email('invalid-email')}")

# 使用类方法创建账户
account2 = BankAccount.create_account("李四", 2000)
print(f"创建账户: {account2.owner}, 余额: {account2.get_balance()}")

# ===== 5. 属性访问和修改 =====

class Car:
    """汽车类"""

    def __init__(self, brand, model):
        self._brand = brand  # 私有属性（约定用下划线）
        self._model = model

    @property
    def brand(self):
        """获取品牌属性"""
        return self._brand

    @brand.setter
    def brand(self, value):
        """设置品牌属性"""
        if len(value) > 0:
            self._brand = value

    @property
    def model(self):
        """获取型号属性"""
        return self._model

    @model.setter
    def model(self, value):
        """设置型号属性"""
        if len(value) > 0:
            self._model = value

    def __str__(self):
        return f"汽车: {self._brand} {self._model}"


print("\n=== 4. 属性访问和修改 ===")

car = Car("特斯拉", "Model 3")
print(f"初始品牌: {car.brand}")
print(f"初始型号: {car.model}")

car.brand = "比亚迪"
car.model = "汉"
print(f"修改后: {car}")

# 尝试直接访问私有属性（不推荐）
# print(f"直接访问: {car._brand}")  # 这是合法的，但不是推荐的做法

# ===== 6. __slots__ - 内存优化 =====

class Point:
    """使用 __slots__ 优化内存的类"""

    __slots__ = ['x', 'y', 'z']  # 限制可定义的属性

    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z


print("\n=== 5. __slots__ 内存优化 ===")

# 创建对象
p = Point(10, 20, 30)
print(f"Point: ({p.x}, {p.y}, {p.z})")

# 尝试添加新属性（__slots__ 中不允许）
# p.color = "red"  # 会抛出 AttributeError

# 查看内存占用
import sys
print(f"Point 对象大小: {sys.getsizeof(p)} 字节")

# 没有使用 __slots__ 的情况
class PointWithoutSlots:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p2 = PointWithoutSlots(10, 20)
print(f"PointWithoutSlots 对象大小: {sys.getsizeof(p2)} 字节")

# ===== 7. 构造函数和析构函数 =====

class Resource:
    """带资源管理的类"""

    def __init__(self, name):
        print(f"[构造] 创建资源: {name}")
        self.name = name
        self.initialized = True

    def __del__(self):
        """析构函数：对象被销毁时调用"""
        print(f"[析构] 销毁资源: {self.name}")

    def use(self):
        """使用资源"""
        print(f"[使用] 正在使用资源: {self.name}")


print("\n=== 6. 构造函数和析构函数 ===")

print("创建资源:")
r1 = Resource("数据库连接1")
r1.use()

print("\n删除资源:")
del r1

# Python 会自动调用 __del__
print("\n自动删除:")
r2 = Resource("数据库连接2")


# ===== 8. 实战应用 - 用户系统 =====

class User:
    """用户类"""

    # 类属性
    all_users = []

    def __init__(self, username, email, age):
        """构造函数"""
        self.username = username
        self.email = email
        self.age = age
        User.all_users.append(self)

    def get_info(self):
        """获取用户信息"""
        return f"用户名: {self.username}, 邮箱: {self.email}, 年龄: {self.age}"

    def update_age(self, new_age):
        """更新年龄"""
        if new_age > 0:
            self.age = new_age
            return f"{self.username} 的年龄更新为 {self.age}"
        return "年龄必须为正数"

    def __str__(self):
        return self.get_info()

    @classmethod
    def get_all_users(cls):
        """获取所有用户"""
        return cls.all_users

    @staticmethod
    def is_valid_username(username):
        """验证用户名"""
        return len(username) > 3 and len(username) < 20


print("\n=== 7. 实战应用 - 用户系统 ===")

# 创建用户
u1 = User("张三", "zhangsan@example.com", 25)
u2 = User("李四", "lisi@example.com", 30)
u3 = User("王五", "wangwu@example.com", 35)

# 查看用户信息
print(u1.get_info())
print(u2.get_info())

# 更新年龄
print(u2.update_age(31))

# 获取所有用户
print(f"\n所有用户:")
for user in User.get_all_users():
    print(f"  - {user.get_info()}")

# 验证用户名
print(f"\n用户名验证:")
print(f"  张三: {User.is_valid_username('张三')}")  # True
print(f"  ab: {User.is_valid_username('ab')}")      # False
print(f"  太长: {User.is_valid_username('a' * 50)}")  # False (太长)

# ===== 9. 类的各种方法 =====

class Utility:
    """工具类"""

    @classmethod
    def create_instance(cls):
        """创建实例"""
        return cls()

    @staticmethod
    def calculate_sum(a, b):
        """计算和"""
        return a + b

    @staticmethod
    def calculate_product(a, b):
        """计算积"""
        return a * b


print("\n=== 8. 类的各种方法 ===")

# 使用类方法创建实例
util = Utility.create_instance()
print(f"使用类方法创建实例: {util}")

# 使用静态方法
print(f"计算和: {Utility.calculate_sum(10, 20)}")
print(f"计算积: {Utility.calculate_product(10, 20)}")

# ===== 测试代码 =====

print("\n=== 9. 测试用户系统 ===")

# 创建更多用户
users = [
    User("Alice", "alice@example.com", 28),
    User("Bob", "bob@example.com", 32),
    User("Charlie", "charlie@example.com", 24)
]

# 查询特定用户
for user in users:
    print(f"  {user}")

# 统计用户
print(f"\n总用户数: {len(User.get_all_users())}")

# 创建账户
account1 = BankAccount("Alice", 5000)
account2 = BankAccount("Bob", 10000)

print(f"\n账户统计: {BankAccount.get_total_accounts()}")
print(f"账户余额: {account1.get_balance()} + {account2.get_balance()} = {account1.get_balance() + account2.get_balance()}")
