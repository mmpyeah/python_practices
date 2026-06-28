# Lesson 7.3 - 魔术方法
# ★★★ 核心概念，Python 魔术方法的威力

"""
魔术方法（Magic Methods / Dunder Methods）是 Python 类中特殊的方法
它们以双下划线开头和结尾，如 __init__、__str__ 等
本文档涵盖：
1. __str__ 和 __repr__
2. __len__ 和 __bool__
3. __eq__ 和 __lt__ 等
4. __add__ 和 __mul__ 等
5. __contains__ 等
6. __dict__ 和 __slots__
"""

# ===== 1. __str__ 和 __repr__ =====

"""
__str__: 用户友好的字符串表示（str() 时调用）
__repr__: 开发者友好的字符串表示（repr() 时调用，调试用）
"""

class Book:
    """书籍类"""

    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    def __str__(self):
        """用户友好的字符串表示"""
        return f"《{self.title}》 by {self.author} ({self.year})"

    def __repr__(self):
        """开发者友好的字符串表示"""
        return f"Book(title='{self.title}', author='{self.author}', year={self.year})"


print("=== 1. __str__ 和 __repr__ ===")

book = Book("Python编程", "张三", 2024)

# 使用 str() - 用户友好
print(f"str(book) = {str(book)}")

# 使用 repr() - 开发者友好
print(f"repr(book) = {repr(book)}")

# 打印对象时默认调用 __str__
print(f"\n打印对象: {book}")

# 在交互式环境中使用 repr
# >>> book
# Book(title='Python编程', author='张三', year=2024)


# ===== 2. __len__ 和 __bool__ =====

class Line:
    """线段类"""

    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def length(self):
        """计算长度"""
        return ((self.x2 - self.x1)**2 + (self.y2 - self.y1)**2)**0.5

    def __len__(self):
        """返回长度"""
        return int(self.length())

    def __bool__(self):
        """返回布尔值"""
        return self.length() > 0


print("\n=== 2. __len__ 和 __bool__ ===")

line = Line(0, 0, 3, 4)
print(f"长度: {len(line)}")

# 在 if 条件中
if line:
    print("线段长度 > 0")
else:
    print("线段长度 <= 0")

# 创建零长度线段
line_zero = Line(1, 1, 1, 1)
print(f"零长度线段长度: {len(line_zero)}")
if line_zero:
    print("线段存在")
else:
    print("线段不存在")


# ===== 3. __eq__ 和比较方法 =====

"""
比较方法：__eq__、__lt__、__le__、__gt__、__ge__、__ne__
用于实现对象的比较操作
"""

class Rectangle:
    """矩形类"""

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def __eq__(self, other):
        """相等比较"""
        if not isinstance(other, Rectangle):
            return NotImplemented
        return (self.width, self.height) == (other.width, other.height)

    def __lt__(self, other):
        """小于比较"""
        if not isinstance(other, Rectangle):
            return NotImplemented
        return self.area() < other.area()

    def __le__(self, other):
        """小于等于比较"""
        if not isinstance(other, Rectangle):
            return NotImplemented
        return self.area() <= other.area()

    def __gt__(self, other):
        """大于比较"""
        if not isinstance(other, Rectangle):
            return NotImplemented
        return self.area() > other.area()

    def __ge__(self, other):
        """大于等于比较"""
        if not isinstance(other, Rectangle):
            return NotImplemented
        return self.area() >= other.area()

    def area(self):
        return self.width * self.height

    def __str__(self):
        return f"矩形({self.width} x {self.height})"


print("\n=== 3. __eq__ 和比较方法 ===")

rect1 = Rectangle(5, 10)
rect2 = Rectangle(5, 10)
rect3 = Rectangle(10, 5)

print(f"rect1 == rect2: {rect1 == rect2}")
print(f"rect1 == rect3: {rect1 == rect3}")

print(f"\n比较面积:")
print(f"rect1 area: {rect1.area()}")
print(f"rect2 area: {rect2.area()}")
print(f"rect3 area: {rect3.area()}")
print(f"rect1 < rect3: {rect1 < rect3}")
print(f"rect3 > rect1: {rect3 > rect1}")

# 排序
rectangles = [rect1, rect3, rect2]
rectangles.sort()
print(f"\n按面积排序: {[str(r) for r in rectangles]}")


# ===== 4. __add__、__sub__ 等算术运算 =====

"""
算术运算方法：__add__、__sub__、__mul__、__div__、__floordiv__、__mod__ 等
"""

class Vector:
    """向量类"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        """加法运算"""
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        return NotImplemented

    def __sub__(self, other):
        """减法运算"""
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        return NotImplemented

    def __mul__(self, scalar):
        """乘法运算（标量乘向量）"""
        if isinstance(scalar, (int, float)):
            return Vector(self.x * scalar, self.y * scalar)
        return NotImplemented

    def __rmul__(self, scalar):
        """乘法运算（标量乘向量，顺序无关）"""
        if isinstance(scalar, (int, float)):
            return Vector(self.x * scalar, self.y * scalar)
        return NotImplemented

    def __truediv__(self, scalar):
        """除法运算（标量除向量）"""
        if isinstance(scalar, (int, float)):
            if scalar == 0:
                raise ValueError("不能除以零")
            return Vector(self.x / scalar, self.y / scalar)
        return NotImplemented

    def __neg__(self):
        """取负"""
        return Vector(-self.x, -self.y)

    def __abs__(self):
        """绝对值"""
        return (self.x**2 + self.y**2)**0.5

    def __str__(self):
        return f"Vector({self.x}, {self.y})"

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"


print("\n=== 4. __add__ 等算术运算 ===")

v1 = Vector(3, 4)
v2 = Vector(1, 2)

print(f"v1 = {v1}")
print(f"v2 = {v2}")

# 加法
v3 = v1 + v2
print(f"v1 + v2 = {v3}")

# 减法
v4 = v1 - v2
print(f"v1 - v2 = {v4}")

# 标量乘法
v5 = v1 * 2
print(f"v1 * 2 = {v5}")

# 标量除法
v6 = v1 / 2
print(f"v1 / 2 = {v6}")

# 加法/乘法的交换顺序
v7 = 2 * v1
print(f"2 * v1 = {v7}")

# 取负
v8 = -v1
print(f"-v1 = {v8}")

# 绝对值
print(f"|v1| = {abs(v1):.2f}")

# ===== 5. __contains__ 等 =====

"""
__contains__: 检查元素是否在容器中 (in 操作符)
"""

class Container:
    """容器类"""

    def __init__(self, *items):
        self.items = list(items)

    def __contains__(self, item):
        """检查元素是否在容器中"""
        return item in self.items

    def __iter__(self):
        """迭代器"""
        return iter(self.items)

    def __len__(self):
        """返回长度"""
        return len(self.items)

    def __str__(self):
        return f"Container({self.items})"


print("\n=== 5. __contains__ 等 ===")

container = Container(1, 2, 3, 4, 5)
print(f"container = {container}")
print(f"3 in container: {3 in container}")
print(f"6 in container: {6 in container}")

# 遍历
print(f"\n遍历容器:")
for item in container:
    print(f"  {item}")

# 在其他容器中使用
print(f"\n嵌套容器测试:")
print(f"3 in Container(1, 2, 3, 4, 5)[1]: {3 in Container(1, 2, 3, 4, 5)[1]}")
print(f"3 in Container(1, 2, 3, 4, 5): {3 in Container(1, 2, 3, 4, 5)}")

# ===== 6. __getitem__、__setitem__、__delitem__ =====

"""
索引操作：__getitem__、__setitem__、__delitem__
实现容器的索引和切片功能
"""

class IndexedContainer:
    """可索引容器"""

    def __init__(self, *items):
        self.items = list(items)

    def __getitem__(self, index):
        """获取元素"""
        return self.items[index]

    def __setitem__(self, index, value):
        """设置元素"""
        self.items[index] = value

    def __delitem__(self, index):
        """删除元素"""
        del self.items[index]

    def __len__(self):
        return len(self.items)

    def __str__(self):
        return f"IndexedContainer({self.items})"


print("\n=== 6. __getitem__ 等 ===")

container = IndexedContainer('a', 'b', 'c', 'd', 'e')
print(f"container = {container}")
print(f"container[0] = {container[0]}")
print(f"container[-1] = {container[-1]}")

# 设置元素
container[1] = 'B'
print(f"设置后: {container}")

# 删除元素
del container[3]
print(f"删除后: {container}")


# ===== 7. __dict__ 和 __slots__ =====

"""
__dict__: 获取对象的属性字典
__slots__: 限制对象的属性，节省内存
"""

class NormalClass:
    """普通类"""

    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email


print("\n=== 7. __dict__ 和 __slots__ ===")

obj = NormalClass("张三", 25, "zhangsan@example.com")
print(f"obj.__dict__ = {obj.__dict__}")

# 查看内存占用
import sys
print(f"NormalClass 对象大小: {sys.getsizeof(obj)} 字节")


class SlotsClass:
    """使用 __slots__ 的类"""

    __slots__ = ['name', 'age', 'email']

    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email


obj_slots = SlotsClass("李四", 30, "lisi@example.com")
print(f"obj_slots.__dict__ = {obj_slots.__dict__}")  # __slots__ 类没有 __dict__

print(f"SlotsClass 对象大小: {sys.getsizeof(obj_slots)} 字节")


# ===== 8. 实战应用 - 自定义数据类型 =====

class Point:
    """自定义点类"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        """向量加法"""
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        return NotImplemented

    def __sub__(self, other):
        """向量减法"""
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y)
        return NotImplemented

    def __mul__(self, scalar):
        """标量乘法"""
        if isinstance(scalar, (int, float)):
            return Point(self.x * scalar, self.y * scalar)
        return NotImplemented

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


class Rectangle:
    """自定义矩形类"""

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __str__(self):
        return f"Rectangle({self.x}, {self.y}, {self.width}, {self.height})"

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


print("\n=== 8. 实战应用 - 自定义数据类型 ===")

# 点的运算
p1 = Point(1, 2)
p2 = Point(3, 4)
p3 = p1 + p2  # (1,2) + (3,4) = (4,6)
print(f"p1 = {p1}, p2 = {p2}")
print(f"p1 + p2 = {p3}")

# 矩形信息
rect = Rectangle(0, 0, 5, 10)
print(f"\n矩形信息: {rect}")
print(f"面积: {rect.area()}")
print(f"周长: {rect.perimeter()}")

# 在集合中使用
points = {p1, p2, p3}
print(f"\n点集合: {points}")

# 排序
points_list = [p1, p2, p3]
points_list.sort(key=lambda p: p.x)  # 按x坐标排序
print(f"按x排序: {points_list}")


# ===== 9. 常用魔术方法总结 =====

"""
常用魔术方法：
- __str__, __repr__: 字符串表示
- __len__, __bool__: 长度和布尔值
- __eq__, __lt__, __gt__, __le__, __ge__, __ne__: 比较运算
- __add__, __sub__, __mul__, __div__, __neg__: 算术运算
- __contains__, __iter__, __len__: 容器操作
- __getitem__, __setitem__, __delitem__: 索引操作
- __dict__, __slots__: 属性管理
"""

class CustomList:
    """自定义列表类"""

    def __init__(self, *items):
        self.items = list(items)

    def __getitem__(self, index):
        return self.items[index]

    def __setitem__(self, index, value):
        self.items[index] = value

    def __delitem__(self, index):
        del self.items[index]

    def __len__(self):
        return len(self.items)

    def __str__(self):
        return f"CustomList({self.items})"

    def __repr__(self):
        return f"CustomList({self.items})"

    def __contains__(self, item):
        return item in self.items

    def __iter__(self):
        return iter(self.items)


print("\n=== 9. 常用魔术方法总结 ===")

c = CustomList(1, 2, 3, 4, 5)
print(f"c = {c}")
print(f"c[0] = {c[0]}")
print(f"2 in c: {2 in c}")

for item in c:
    print(f"  {item}")

print(f"\n长度: {len(c)}")
