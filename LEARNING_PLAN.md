# Python 学习计划 · 文件生成总览

> 课程来源：马士兵教育 Python 运维自动化
> 项目路径：D:\PythonProjects\Project1
> 更新时间：2024-06-28
>
> 进度图例：✅ 已完成   🔄 进行中   ⬜ 待生成

---

## 总进度

| Lesson | 主题 | 文件数 | 状态 |
|--------|------|--------|------|
| Lesson 1 | Python 基础入门 | 1 | ✅ |
| Lesson 2 | 字符串 | 6 | ✅ |
| Lesson 3 | 数据结构 | 6 | ✅ |
| Lesson 4 | 控制流 | 4 | ✅ |
| Lesson 5 | 函数进阶 | 5 | ⬜ |
| Lesson 6 | 文件操作 & 异常处理 | 5 | ⬜ |
| Lesson 7 | 面向对象 OOP | 6 | ⬜ |
| Lesson 8 | 模块 & 标准库 | 6 | ⬜ |
| Lesson 9 | 高级特性（选修） | 4 | ⬜ |
| 毕业项目 | 运维自动化综合项目 | 1 | ⬜ |

**总计：44 个文件 | 已完成：17 个 | 进度：39%**

---

## Lesson 1 · Python 基础入门 ✅

路径：`lesson1/`

| 文件 | 说明 | 状态 |
|------|------|------|
| `main.py` | 变量、类型转换、input/print、函数定义、bytes 基础、体脂率计算器综合练习 | ✅ |

---

## Lesson 2 · 字符串 ✅

路径：`lesson_2_字符串/`

| 文件 | 说明 | 重点 | 状态 |
|------|------|------|------|
| `str_concat.py` | 5种拼接方式：+、%、format、f-string、join；各自优缺点对比 | ★★ | ✅ |
| `str_slice.py` | 切片语法 str[start:stop:step]、负索引、反转、日志字段提取、回文判断 | ★ | ✅ |
| `str_methods.py` | 大小写转换、find/index/count、replace、split/join、strip、startswith/endswith | ★★ | ✅ |
| `str_regex.py` | re 模块：search/findall/match、分组捕获、compile、sub替换、常用正则模板 | ★★ | ✅ |
| `str_encoding.py` | encode/decode、UTF-8/GBK差异、乱码处理、bytes/bytearray、chardet检测 | ★ | ✅ |
| `str_advanced.py` | f-string格式化进阶、多行字符串、+拼接vs join性能对比、translate批量替换 | ★ | ✅ |

---

## Lesson 3 · 数据结构 ✅

路径：`lesson_3_数据结构/`

> ★★ 运维脚本最核心的一课，列表和字典几乎在每个脚本里都用到

| 文件 | 说明 | 重点 | 状态 |
|------|------|------|------|
| `list_basic.py` | 列表创建、增删改查、append/extend/insert/remove/pop、index/count、sort/reverse | ★★ | ✅ |
| `list_advanced.py` | 列表推导式、嵌套列表、zip/enumerate/sorted/map/filter、二维表操作 | ★★ | ✅ |
| `tuple_basic.py` | 元组创建、不可变性、解包赋值、*args收集、具名元组 namedtuple | ★ | ✅ |
| `dict_basic.py` | 字典创建、增删改查、get/setdefault、keys/values/items、dict推导式、合并 | ★★ | ✅ |
| `set_basic.py` | 集合创建、去重、交集/并集/差集/对称差、frozenset、集合推导式 | ★ | ✅ |
| `collections_module.py` | Counter词频统计、defaultdict、OrderedDict、deque双端队列、ChainMap | ★★ | ✅ |

---

## Lesson 4 · 控制流 ✅

路径：`lesson_4_控制流/`

| 文件 | 说明 | 重点 | 状态 |
|------|------|------|------|
| `if_else.py` | if/elif/else、三元表达式、match-case（Python 3.10+）、真值判断陷阱 | ★ | ✅ |
| `for_loop.py` | for 遍历、enumerate、zip、range、循环 else、break/continue、日志扫描实战 | ★★ | ✅ |
| `while_loop.py` | while 循环、while else、无限循环 + break、重试机制、轮询场景 | ★ | ✅ |
| `comprehension.py` | 列表/字典/集合/生成器推导式、条件过滤、嵌套推导式、性能对比 | ★★ | ✅ |

---

## Lesson 5 · 函数进阶 ⬜

路径：`lesson_5_函数进阶/`

| 文件 | 说明 | 重点 | 状态 |
|------|------|------|------|
| `func_args.py` | 位置参数、默认参数、*args、**kwargs、关键字限定参数、参数解包 | ★★ | ⬜ |
| `func_lambda.py` | lambda 匿名函数、map/filter/reduce 配合 lambda、sorted key 用法 | ★ | ⬜ |
| `func_decorator.py` | 装饰器原理、@wraps、带参数的装饰器、计时器/日志/权限校验装饰器实战 | ★★ | ⬜ |
| `func_generator.py` | yield 生成器、生成器表达式、send/throw/close、itertools 模块 | ★★ | ⬜ |
| `func_closure.py` | 闭包原理、nonlocal、工厂函数、闭包 vs 全局变量、实战计数器 | ★ | ⬜ |

---

## Lesson 6 · 文件操作 & 异常处理 ⬜

路径：`lesson_6_文件与异常/`

| 文件 | 说明 | 重点 | 状态 |
|------|------|------|------|
| `file_read_write.py` | open 模式、read/readline/readlines、write/writelines、with 上下文管理器 | ★★ | ⬜ |
| `file_path.py` | pathlib.Path 路径操作、os.path、文件遍历、glob 通配符、目录树 | ★★ | ⬜ |
| `file_format.py` | JSON 读写、CSV 读写（csv 模块 + DictReader）、ini 配置文件（configparser） | ★★ | ⬜ |
| `exception_basic.py` | try/except/else/finally、捕获多个异常、异常链 raise from、自定义异常类 | ★★ | ⬜ |
| `exception_advanced.py` | 上下文管理器 contextlib、with 自定义协议、资源安全释放实战 | ★ | ⬜ |

---

## Lesson 7 · 面向对象 OOP ⬜

路径：`lesson_7_面向对象/`

> ★★ 封装运维工具类的核心，理解这一课才能写出可维护的脚本

| 文件 | 说明 | 重点 | 状态 |
|------|------|------|------|
| `class_basic.py` | class 定义、__init__、self、实例属性 vs 类属性、实例方法 | ★★ | ⬜ |
| `class_inherit.py` | 继承、super()、方法重写、多继承、MRO 顺序、mixin 模式 | ★★ | ⬜ |
| `class_magic.py` | 魔术方法：__str__/__repr__/__len__/__eq__/__lt__/__add__/__contains__ | ★★ | ⬜ |
| `class_property.py` | @property 属性装饰器、@classmethod、@staticmethod、__slots__ 内存优化 | ★ | ⬜ |
| `class_dataclass.py` | dataclass 简化类定义、field、__post_init__、frozen 不可变类 | ★ | ⬜ |
| `class_design.py` | 综合实战：设计一个服务器信息类（含继承、属性、魔术方法、序列化） | ★★ | ⬜ |

---

## Lesson 8 · 模块 & 标准库 ⬜

路径：`lesson_8_模块与标准库/`

> ★★ 运维自动化的武器库，os/subprocess/logging 是工作中最常用的三个

| 文件 | 说明 | 重点 | 状态 |
|------|------|------|------|
| `module_system.py` | import 机制、__name__、包结构、__all__、相对导入、模块搜索路径 sys.path | ★ | ⬜ |
| `os_module.py` | os.path、os.listdir/walk、os.makedirs、os.environ、os.getcwd、shutil | ★★ | ⬜ |
| `subprocess_module.py` | subprocess.run/Popen、捕获输出、管道、超时控制、shell=True 的安全陷阱 | ★★ | ⬜ |
| `logging_module.py` | logging 基础配置、日志级别、FileHandler、RotatingFileHandler、格式化 | ★★ | ⬜ |
| `datetime_module.py` | datetime/date/timedelta、时间戳互转、时区 pytz、格式化 strftime/strptime | ★ | ⬜ |
| `third_party.py` | pip 与虚拟环境、requirements.txt、requests 库 HTTP 请求简介 | ★ | ⬜ |

---

## Lesson 9 · 高级特性（选修）⬜

路径：`lesson_9_高级特性/`

| 文件 | 说明 | 重点 | 状态 |
|------|------|------|------|
| `type_hints.py` | 类型注解 typing、Optional/Union/List/Dict、泛型、mypy 静态检查简介 | ★ | ⬜ |
| `concurrency.py` | threading 多线程、multiprocessing 多进程、GIL 说明、适用场景对比 | ★★ | ⬜ |
| `asyncio_basic.py` | async/await 基础、事件循环、asyncio.gather、异步 HTTP（aiohttp 简介） | ★ | ⬜ |
| `functools_itertools.py` | functools：lru_cache/partial/reduce；itertools：chain/product/groupby | ★ | ⬜ |

---

## 毕业项目 · 运维自动化综合脚本 ⬜

路径：`graduation_project/`

| 文件 | 说明 | 状态 |
|------|------|------|
| `server_inspector.py` | **服务器巡检工具**：综合运用所有 Lesson 知识点。功能包括：读取配置文件（Lesson 6）、SSH 连接执行命令（subprocess/paramiko，Lesson 8）、解析输出（正则+字符串，Lesson 2）、数据汇总到字典/列表（Lesson 3）、面向对象封装 ServerInfo 类（Lesson 7）、写入日志（logging，Lesson 8）、生成巡检报告（JSON/CSV，Lesson 6） | ⬜ |

---

## 学习建议

1. **每个文件直接运行**（`Shift+F10`），对照注释里的预期输出，确认理解
2. **★★ 标注的文件**是重中之重，理解后尝试自己默写一遍
3. **每个 Lesson 审核完**再推进下一个，不要跳课
4. **毕业项目**会把所有知识点串联，完成它标志着入门结束

---

*此文档由 Claude 自动生成并维护，每完成一个 Lesson 后更新进度*
