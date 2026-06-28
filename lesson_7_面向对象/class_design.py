# Lesson 7.5 - 类设计综合实战
# ★★★ 核心概念，OOP 的综合应用

"""
综合实战：设计一个服务器信息类
包含：继承、属性、魔术方法、序列化
"""

# ===== 1. 基础服务器类 =====

class ServerInfo:
    """服务器信息类"""

    def __init__(self, hostname, ip_address, port, status="online"):
        self.hostname = hostname
        self.ip_address = ip_address
        self.port = port
        self.status = status
        self.boot_time = self._get_boot_time()
        self.cpu_usage = 0
        self.memory_usage = 0

    def _get_boot_time(self):
        """获取系统启动时间"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def update_status(self, status):
        """更新服务器状态"""
        self.status = status
        return f"服务器 {self.hostname} 状态更新为 {status}"

    def get_info(self):
        """获取服务器信息"""
        return (f"服务器: {self.hostname} ({self.ip_address}:{self.port})\n"
                f"  状态: {self.status}\n"
                f"  启动时间: {self.boot_time}\n"
                f"  CPU使用率: {self.cpu_usage}%\n"
                f"  内存使用率: {self.memory_usage}%")

    def __str__(self):
        return self.get_info()

    def __repr__(self):
        return f"ServerInfo(hostname='{self.hostname}', ip_address='{self.ip_address}', port={self.port})"

    def __eq__(self, other):
        if not isinstance(other, ServerInfo):
            return NotImplemented
        return (self.hostname == other.hostname and
                self.ip_address == other.ip_address and
                self.port == other.port)

    def __hash__(self):
        return hash((self.hostname, self.ip_address, self.port))


# ===== 2. Web服务器类 =====

class WebServer(ServerInfo):
    """Web服务器类 - 继承自 ServerInfo"""

    def __init__(self, hostname, ip_address, port=80, status="online", workers=4):
        super().__init__(hostname, ip_address, port, status)
        self.workers = workers
        self.uptime = "0h 0m 0s"
        self.requests = 0
        self.errors = 0

    def update_stats(self, cpu, memory, uptime, requests, errors):
        """更新统计数据"""
        self.cpu_usage = cpu
        self.memory_usage = memory
        self.uptime = uptime
        self.requests = requests
        self.errors = errors

    def get_info(self):
        """重写获取信息"""
        return (f"Web服务器: {self.hostname} ({self.ip_address}:{self.port})\n"
                f"  状态: {self.status}\n"
                f"  工作进程: {self.workers}\n"
                f"  运行时间: {self.uptime}\n"
                f"  请求总数: {self.requests}\n"
                f"  错误数: {self.errors}\n"
                f"  CPU使用率: {self.cpu_usage}%\n"
                f"  内存使用率: {self.memory_usage}%")

    def handle_request(self):
        """处理请求"""
        self.requests += 1
        return f"处理请求: {self.hostname}"

    def start(self):
        """启动服务器"""
        if self.status != "online":
            self.status = "online"
            return f"服务器 {self.hostname} 已启动"
        return f"服务器 {self.hostname} 已经在运行"

    def stop(self):
        """停止服务器"""
        if self.status == "online":
            self.status = "stopped"
            return f"服务器 {self.hostname} 已停止"
        return f"服务器 {self.hostname} 已经停止"

    def __str__(self):
        return f"WebServer({self.hostname})"

    def __repr__(self):
        return (f"WebServer(hostname='{self.hostname}', ip_address='{self.ip_address}', "
                f"port={self.port}, workers={self.workers}, status='{self.status}')")


# ===== 3. 数据库服务器类 =====

class DatabaseServer(ServerInfo):
    """数据库服务器类 - 继承自 ServerInfo"""

    def __init__(self, hostname, ip_address, port=3306, status="online", database="mysql"):
        super().__init__(hostname, ip_address, port, status)
        self.database = database
        self.connections = 0
        self.max_connections = 100
        self.version = "8.0.0"

    def update_stats(self, cpu, memory, connections, version):
        """更新统计数据"""
        self.cpu_usage = cpu
        self.memory_usage = memory
        self.connections = connections
        self.version = version

    def get_info(self):
        """重写获取信息"""
        return (f"数据库服务器: {self.hostname} ({self.ip_address}:{self.port})\n"
                f"  状态: {self.status}\n"
                f"  数据库: {self.database}\n"
                f"  版本: {self.version}\n"
                f"  当前连接: {self.connections}/{self.max_connections}\n"
                f"  CPU使用率: {self.cpu_usage}%\n"
                f"  内存使用率: {self.memory_usage}%")

    def connect(self, db_name):
        """连接数据库"""
        if self.status == "online":
            self.connections += 1
            return f"连接到 {self.hostname} 的数据库 {db_name}"
        return f"服务器 {self.hostname} 未运行"

    def disconnect(self):
        """断开数据库连接"""
        if self.connections > 0:
            self.connections -= 1
            return f"断开 {self.hostname} 的连接"
        return f"{self.hostname} 没有活动连接"

    def __str__(self):
        return f"DatabaseServer({self.hostname})"

    def __repr__(self):
        return f"DatabaseServer(hostname='{self.hostname}', database='{self.database}', status='{self.status}')"


# ===== 4. 服务器监控系统 =====

class ServerMonitor:
    """服务器监控系统"""

    def __init__(self):
        self.servers = set()
        self.monitored_servers = []

    def add_server(self, server):
        """添加服务器"""
        if server in self.servers:
            print(f"服务器 {server} 已经在监控中")
            return

        self.servers.add(server)
        self.monitored_servers.append(server)
        print(f"添加服务器 {server} 到监控列表")

    def remove_server(self, server):
        """移除服务器"""
        if server in self.servers:
            self.servers.remove(server)
            self.monitored_servers.remove(server)
            print(f"移除服务器 {server}")
        else:
            print(f"服务器 {server} 不在监控中")

    def get_all_servers(self):
        """获取所有监控的服务器"""
        return sorted(self.monitored_servers, key=lambda s: s.hostname)

    def get_server_info(self, hostname):
        """获取服务器信息"""
        for server in self.servers:
            if server.hostname == hostname:
                return server.get_info()
        return f"未找到服务器 {hostname}"

    def generate_report(self):
        """生成监控报告"""
        report = []
        report.append("=== 服务器监控报告 ===\n")

        for server in self.monitored_servers:
            report.append(server.get_info())
            report.append("-" * 50)

        return "\n".join(report)

    def __str__(self):
        return f"ServerMonitor(监控 {len(self.monitored_servers)} 个服务器)"


# ===== 5. 序列化支持 =====

class ServerSerializer:
    """服务器序列化器"""

    @staticmethod
    def to_dict(server):
        """将服务器对象转换为字典"""
        return {
            'hostname': server.hostname,
            'ip_address': server.ip_address,
            'port': server.port,
            'status': server.status,
            'cpu_usage': server.cpu_usage,
            'memory_usage': server.memory_usage
        }

    @staticmethod
    def to_json(servers):
        """将多个服务器转换为 JSON 字符串"""
        import json
        return json.dumps([ServerSerializer.to_dict(s) for s in servers], indent=2, ensure_ascii=False)

    @staticmethod
    def from_dict(data):
        """从字典创建服务器对象"""
        # 这里简化处理，实际应根据类型创建不同的对象
        return ServerInfo(data['hostname'], data['ip_address'], data['port'], data['status'])

    @staticmethod
    def from_json(json_str):
        """从 JSON 字符串创建服务器对象"""
        import json
        data = json.loads(json_str)
        return [ServerSerializer.from_dict(d) for d in data]


# ===== 6. 实战应用 =====

print("=== 1. 创建服务器 ===")

# 创建 Web 服务器
web1 = WebServer("web1", "192.168.1.10", port=80, workers=4)
web2 = WebServer("web2", "192.168.1.11", port=443, workers=8)

# 创建数据库服务器
db1 = DatabaseServer("db1", "192.168.1.20", port=3306, database="mysql")
db2 = DatabaseServer("db2", "192.168.1.21", port=3306, database="postgres")

# 更新服务器统计
web1.update_stats(45, 60, "5h 30m 0s", 1000000, 50)
web2.update_stats(70, 85, "10h 15m 0s", 2000000, 120)

db1.update_stats(30, 40, 15, "8.0.0")
db2.update_stats(25, 35, 12, "8.0.0")


# ===== 7. 使用服务器 =====

print("\n=== 2. 使用服务器 ===")

# Web 服务器操作
print(web1.start())
print(f"请求: {web1.handle_request()}")
print(web1.stop())

# 数据库服务器操作
print(db1.connect("mydb"))
print(db1.get_info())

# 监控系统
monitor = ServerMonitor()
monitor.add_server(web1)
monitor.add_server(web2)
monitor.add_server(db1)
monitor.add_server(db2)

print(f"\n监控服务器: {monitor}")
print(f"所有服务器: {monitor.get_all_servers()}")

# 生成报告
report = monitor.generate_report()
print(f"\n监控报告:")
print(report)


# ===== 8. 序列化和反序列化 =====

print("\n=== 3. 序列化 ===")

servers = [web1, web2, db1, db2]
json_data = ServerSerializer.to_json(servers)
print(f"JSON数据:\n{json_data}")

# 从 JSON 恢复
restored_servers = ServerSerializer.from_json(json_data)
print(f"\n恢复的服务器数量: {len(restored_servers)}")


# ===== 9. 使用魔术方法 =====

print("\n=== 4. 使用魔术方法 ===")

# 相等比较
print(f"web1 == web1: {web1 == web1}")
print(f"web1 == web2: {web1 == web2}")

# 哈希（用于集合）
server_set = {web1, web2}
print(f"\nWeb服务器集合: {[str(s) for s in server_set]}")

# 字符串表示
print(f"\nweb1: {web1}")
print(f"repr(web1): {repr(web1)}")

# 对象转换为字典
server_dict = ServerSerializer.to_dict(web1)
print(f"\nweb1 字典: {server_dict}")


# ===== 10. 多态处理 =====

class ServerProcessor:
    """服务器处理器"""

    def process(self, server):
        """处理服务器"""
        method_name = f"process_{server.__class__.__name__.lower()}"
        method = getattr(self, method_name, self.process_generic)
        return method(server)

    def process_webservers(self, server):
        return f"处理 Web 服务器: {server.hostname}, 请求数: {server.requests}"

    def process_databaseservers(self, server):
        return f"处理数据库服务器: {server.hostname}, 连接数: {server.connections}"

    def process_generic(self, server):
        return f"处理服务器: {server}"


print("\n=== 5. 多态处理 ===")

processor = ServerProcessor()

for server in [web1, db1]:
    result = processor.process(server)
    print(result)


# ===== 11. 总结 =====

print("\n=== 6. 总结 ===")

print("服务器系统包含:")
print("  1. 基础服务器类 (ServerInfo) - 提供基本属性和方法")
print("  2. Web服务器类 (WebServer) - 继承自 ServerInfo，添加 Web 特有功能")
print("  3. 数据库服务器类 (DatabaseServer) - 继承自 ServerInfo，添加数据库功能")
print("  4. 监控系统 (ServerMonitor) - 管理和监控多个服务器")
print("  5. 序列化器 (ServerSerializer) - 序列化和反序列化")

print(f"\n监控 {len(monitor.monitored_servers)} 个服务器:")
for server in monitor.monitored_servers:
    print(f"  - {server}")
