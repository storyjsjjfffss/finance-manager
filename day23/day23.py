class User:
    # 类属性（所有实例共享）
    total_users = 0

    def __init__(self, username, password):
        self.username = username
        self.__password = password  # 私有属性，防泄漏
        User.total_users += 1

    # 1. 实例方法：校验密码
    def check_password(self, input_pwd):
        return self.__password == input_pwd

    # 2. 类方法：备用构造器（工厂方法）
    @classmethod
    def from_string(cls, user_str):
        """允许通过 'Tom,123456' 格式直接创建用户实例"""
        name, pwd = user_str.split(",")
        return cls(name, pwd)

    # 3. 静态方法：独立工具
    @staticmethod
    def is_valid_username(name):
        return len(name) >= 3 and name.isalnum()


# 演示三种调用
u1 = User("Alex", "abc_123")
u2 = User.from_string("Bob,pwd666")  # 通过类方法创建

print("用户总数:", User.total_users)
print("Alex 密码是否正确:", u1.check_password("wrong"))
print("用户名验证结果:", User.is_valid_username("admin123"))