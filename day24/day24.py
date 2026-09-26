# 父类：通用动物
class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def make_sound(self):
        print(f"{self.name} 发出了某种通用的叫声。")

    def show_info(self):
        print(f"名字: {self.name}, 年龄: {self.age} 岁")


# 子类 1：狗（继承 Animal）
class Dog(Animal):
    def __init__(self, name, age, breed):
        # 1. 调用父类构造方法初始化通用属性
        super().__init__(name, age)
        # 2. 绑定狗专属的属性
        self.breed = breed

    # 3. 方法重写：覆盖父类的通用叫声
    def make_sound(self):
        print(f"🐶 {self.name}（{self.breed}）兴奋地汪汪叫！")


# 子类 2：猫（继承 Animal）
class Cat(Animal):
    # 没有重写 __init__，自动直接继承父类的构造方式
    def make_sound(self):
        print(f"🐱 {self.name} 温柔地喵喵叫～")

    # 定义猫专属的独有方法
    def catch_mouse(self):
        print(f"{self.name} 抓到了一只老鼠！")


# --- 实例化验证 ---
d = Dog("旺财", 3, "金毛")
c = Cat("花花", 2)

d.show_info()    # 继承自父类
d.make_sound()   # 执行子类重写版本

c.show_info()    # 继承自父类
c.make_sound()   # 执行子类重写版本
c.catch_mouse()  # 猫专属方法

# 类型层级判定
print("d 是否属于 Animal 类:", isinstance(d, Animal))  # True
print("Dog 是否是 Animal 的子类:", issubclass(Dog, Animal))  # True