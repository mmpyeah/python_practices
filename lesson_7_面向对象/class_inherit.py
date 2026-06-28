# Lesson 7.2 - 类的继承
# ★★★ 核心概念，OOP 复用代码的核心

"""
继承是 OOP 中最重要的特性之一。
它允许创建一个新类，继承现有类的属性和方法。
本文档涵盖：
1. 基本继承
2. super() 函数
3. 方法重写
4. 多继承
5. MRO（方法解析顺序）
6. Mixin 模式
"""

# ===== 1. 基本继承 =====

"""
继承允许子类继承父类的属性和方法
使用 class 子类名(父类名) 定义
"""

class Animal:
    """动物基类"""

    def __init__(self, name):
        self.name = name

    def speak(self):
        """动物的叫声"""
        return "动物会发出声音"

    def move(self):
        """动物会移动"""
        return f"{self.name} 在移动"

    def eat(self):
        """动物会吃"""
        return f"{self.name} 在吃食物"


class Dog(Animal):
    """狗类 - 继承自 Animal"""

    def __init__(self, name, breed):
        # 调用父类的构造函数
        super().__init__(name)
        self.breed = breed

    # 方法重写
    def speak(self):
        return "汪汪汪！"

    def fetch(self):
        """狗的特有方法"""
        return f"{self.name} 正在捡球"


class Cat(Animal):
    """猫类 - 继承自 Animal"""

    def __init__(self, name, color):
        super().__init__(name)
        self.color = color

    # 方法重写
    def speak(self):
        return "喵喵喵！"

    def climb(self):
        """猫的特有方法"""
        return f"{self.name} 正在爬树"


print("=== 1. 基本继承 ===")

# 创建狗对象
dog = Dog("旺财", "哈士奇")
print(f"名字: {dog.name}")
print(f"品种: {dog.breed}")
print(f"叫: {dog.speak()}")
print(f"移动: {dog.move()}")
print(f"捡球: {dog.fetch()}")

# 创建猫对象
cat = Cat("咪咪", "白色")
print(f"\n名字: {cat.name}")
print(f"颜色: {cat.color}")
print(f"叫: {cat.speak()}")
print(f"移动: {cat.move()}")
print(f"爬树: {cat.climb()}")


# ===== 2. 调用父类方法 =====

class Bird(Animal):
    """鸟类 - 继承自 Animal"""

    def __init__(self, name, can_fly):
        super().__init__(name)
        self.can_fly = can_fly

    # 重写方法，并调用父类方法
    def speak(self):
        # 调用父类方法
        parent_speak = super().speak()
        return f"{self.name} 会飞: {self.can_fly}, {parent_speak}"

    def fly(self):
        """鸟的特有方法"""
        if self.can_fly:
            return f"{self.name} 正在飞向天空"
        return f"{self.name} 不会飞，在地面走路"


print("\n=== 2. 调用父类方法 ===")

parrot = Bird("鹦鹉", True)
print(parrot.speak())
print(parrot.fly())

# 无法飞行的鸟
ostrich = Bird("鸵鸟", False)
print(ostrich.speak())
print(ostrich.fly())


# ===== 3. 多继承 =====

"""
Python 支持多继承，子类可以继承多个父类
"""

class CanFly:
    """能飞的特性（Mixin）"""
    def fly(self):
        return "我会飞"


class CanSwim:
    """能游的特性（Mixin）"""
    def swim(self):
        return "我会游泳"


class Duck(CanFly, CanSwim, Animal):
    """鸭子类 - 继承自多个类"""

    def __init__(self, name):
        super().__init__(name)

    def quack(self):
        """鸭子的叫声"""
        return "嘎嘎嘎！"


print("\n=== 3. 多继承 ===")

duck = Duck("小白")
print(f"鸭子: {duck.name}")
print(f"叫: {duck.speak()}")  # 调用 Animal 的方法
print(f"飞: {duck.fly()}")
print(f"游: {duck.swim()}")
print(f"嘎嘎叫: {duck.quack()}")


# ===== 4. 方法解析顺序 (MRO) =====

"""
多继承时，Python 使用 C3 线性化算法确定方法解析顺序
可以使用 super() 或类的 mro() 方法查看
"""

class A:
    def method(self):
        return "A.method"

class B(A):
    def method(self):
        return "B.method"

class C(A):
    def method(self):
        return "C.method"

class D(B, C):
    """D 继承 B 和 C，B 继承 A，C 也继承 A"""
    pass


print("\n=== 4. 方法解析顺序 (MRO) ===")

d = D()
print(f"D.method: {d.method()}")

# 查看类的 MRO
print(f"D 的方法解析顺序 (MRO):")
for i, cls in enumerate(D.__mro__, 1):
    print(f"  {i}. {cls.__name__}")


# ===== 5. Mixin 模式 =====

"""
Mixin 是一种特殊的类，只提供方法，不负责初始化状态
常用于多继承，实现功能组合
"""

class MixinLogger:
    """日志 Mixin"""
    def log(self, message):
        print(f"[LOG] {message}")


class MixinTime:
    """时间 Mixin"""
    def get_creation_time(self):
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class User(MixinLogger, MixinTime):
    """用户类，组合多个 Mixin"""

    def __init__(self, username):
        self.username = username

    def login(self):
        """用户登录"""
        self.log(f"用户 {self.username} 登录成功")
        return f"登录时间: {self.get_creation_time()}"


print("\n=== 5. Mixin 模式 ===")

user = User("张三")
print(user.login())
print(user.get_creation_time())


# ===== 6. 抽象基类 =====

"""
抽象基类（Abstract Base Class）定义了子类必须实现的方法
使用 abc 模块实现
"""

from abc import ABC, abstractmethod

class Shape(ABC):
    """形状抽象基类"""

    @abstractmethod
    def area(self):
        """计算面积"""
        pass

    @abstractmethod
    def perimeter(self):
        """计算周长"""
        pass

    def print_info(self):
        """通用方法"""
        print(f"面积: {self.area()}, 周长: {self.perimeter()}")


class Rectangle(Shape):
    """矩形类"""

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


class Circle(Shape):
    """圆形类"""

    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2

    def perimeter(self):
        return 2 * 3.14159 * self.radius


print("\n=== 6. 抽象基类 ===")

rect = Rectangle(5, 10)
print(f"矩形: {rect.area()}, {rect.perimeter()}")

circle = Circle(5)
print(f"圆形: {circle.area():.2f}, {circle.perimeter():.2f}")

# 创建形状列表
shapes = [Rectangle(3, 4), Circle(5)]
for shape in shapes:
    shape.print_info()


# ===== 7. 方法重写中的参数扩展 =====

"""
子类重写父类方法时，可以添加额外参数
"""

class Parent:
    def greet(self, name):
        return f"你好，{name}"


class Child(Parent):
    def greet(self, name, age=None):
        """重写方法，添加年龄参数"""
        if age:
            return f"你好，{name}！你{age}岁了"
        return f"你好，{name}"


print("\n=== 7. 方法重写中的参数扩展 ===")

parent = Parent()
child = Child()

print(parent.greet("张三"))  # "你好，张三"
print(child.greet("张三"))  # "你好，张三！你25岁了"
print(child.greet("李四", 30))  # "你好，李四！你30岁了"


# ===== 8. 继承层次结构 =====

class Vehicle:
    """车辆基类"""
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

    def move(self):
        return f"{self.brand} {self.model} 在行驶"


class Car(Vehicle):
    """汽车类"""
    def __init__(self, brand, model, doors):
        super().__init__(brand, model)
        self.doors = doors

    def move(self):
        return f"{self.brand} {self.model} 在公路上行驶"


class ElectricCar(Car):
    """电动汽车类"""
    def __init__(self, brand, model, doors, battery):
        super().__init__(brand, model, doors)
        self.battery = battery

    def move(self):
        return f"{self.brand} {self.model} 在公路上安静地行驶"

    def charge(self):
        return f"{self.brand} {self.model} 正在充电，电量: {self.battery}%"


class Tesla(ElectricCar):
    """特斯拉类"""
    def __init__(self, model, doors=4, battery=100):
        super().__init__("Tesla", model, doors, battery)

    def self_driving(self):
        return f"{self.model} 开启了自动驾驶"


print("\n=== 8. 继承层次结构 ===")

tesla = Tesla("Model 3", 4, 100)
print(f"品牌: {tesla.brand}")
print(f"型号: {tesla.model}")
print(f"车门: {tesla.doors}")
print(f"电量: {tesla.battery}%")
print(f"移动: {tesla.move()}")
print(f"充电: {tesla.charge()}")
print(f"自动驾驶: {tesla.self_driving()}")


# ===== 9. 实战应用 - 多态 =====

"""
多态：相同的接口，不同的实现
"""

class AnimalSound:
    """动物叫声处理"""

    def make_sound(self, animal):
        if isinstance(animal, Dog):
            return animal.speak()
        elif isinstance(animal, Cat):
            return animal.speak()
        elif isinstance(animal, Duck):
            return animal.quack()
        else:
            return "未知动物的叫声"


print("\n=== 9. 实战应用 - 多态 ===")

sounds = AnimalSound()

animals = [Dog("旺财"), Cat("咪咪"), Duck("小白", "mallard")]

for animal in animals:
    # 统一接口，不同行为
    print(f"{animal.__class__.__name__}: {sounds.make_sound(animal)}")


# ===== 测试代码 =====

print("\n=== 测试用户系统 ===")

class DatabaseUser(MixinLogger, MixinTime):
    """数据库用户类"""

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def login(self):
        self.log(f"用户 {self.username} 从 {self.email} 登录")
        return f"登录时间: {self.get_creation_time()}"

    def change_password(self, old_password, new_password):
        # 模拟密码验证
        self.log(f"用户 {self.username} 更新密码")
        return f"密码已更新: {self.username}"


db_user = DatabaseUser("admin", "admin@example.com")
print(db_user.login())
print(db_user.change_password("123456", "newpassword"))

# 创建不同类型的形状
print("\n形状统计:")
shapes = [Rectangle(5, 10), Circle(5)]
total_area = sum(shape.area() for shape in shapes)
print(f"总面积: {total_area:.2f}")
