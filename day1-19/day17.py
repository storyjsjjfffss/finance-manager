#匿名函数（Lambda）与高阶函数（map / filter / sorted key）
# 核心语法约束：
#
# 只能包含单行表达式，不能写赋值语句、for/while 循环或多行逻辑。
#
# 不需要且不能写 return：冒号右侧表达式的计算结果会自动返回。
# 1. 基础对比：普通函数 vs Lambda
def square(x):
    return x ** 2

square_lambda = lambda x: x ** 2
print("普通函数与 Lambda 计算结果一致:", square(5) == square_lambda(5))

# 2. sorted 配合 key 参数（最常用的业务场景）
students = [
    {"name": "Alex", "score": 82},
    {"name": "Bob", "score": 95},
    {"name": "Charlie", "score": 78}
]

# 按分数从高到低降序排序
by_score_desc = sorted(students, key=lambda s: s["score"], reverse=True)#不好理解啊
print("按成绩降序:", by_score_desc)

# 3. map 与 filter 转换过滤
numbers = [1, 2, 3, 4, 5, 6]
# 筛选出偶数后将每个偶数乘以 10
evens = filter(lambda x: x % 2 == 0, numbers)#返回的不是列表，是迭代器本身，得用list
scaled = map(lambda x: x * 10, evens)
# filter(判断函数, 数据)  →  数据被“过滤”成更小的列表
# map(变换函数, 数据)     →  数据被“映射”成新形态的列表
print("处理结果:", list(scaled))  # [20, 40, 60]
# 第 3 周后半段：数据持久化与工程稳健性
# Day 18：文件读写与上下文管理器（open, with 语法糖，文本与 CSV 读写）。
#
# Day 19：数据交换格式与异常防御体系（JSON 序列化与反序列化，try-except-else-finally，自定义异常）。
#
# Day 20：模块化与代码拆分（import 原理、自定义模块、if __name__ == '__main__' 工程入口规范）。
#
# Day 21：第 3 周综合项目：本地数据持久化的个人记账本 / 任务管理器（带自动保存与崩溃恢复）。
#
# 第 4 周：面向对象编程（OOP）
# Day 22：类与对象基础（class, __init__ 构造方法, 实例属性与 self 的底层本质）。
#
# Day 23：方法与属性封装（实例方法、类方法 @classmethod、静态方法 @staticmethod、私有属性 __var）。
#
# Day 24：面向对象三大特性之一：继承（Inheritance）（父类扩展、super() 调用、方法重写）。
#
# Day 25：面向对象三大特性之二：多态与接口抽象（鸭子类型 Duck Typing、统一接口交互）。
#
# Day 26：魔法方法（Magic Methods）（__str__, __repr__, __len__, __eq__ 自定义对象交互）。
#
# Day 27：面向对象实战建模：RPG 游戏战斗引擎 / 银行账户清算系统。
#
# Day 28：常用内置标准库探索（datetime, pathlib, collections）。
#
# 第 5 周：综合实战与结营（Day 29 - 30）
# Day 29：大作业架构设计与编码（结合 OOP + JSON持久化 + 异常处理 的完整独立 CLI 软件）。
#
# Day 30：工程收尾与进阶指引（虚拟环境 venv、依赖管理 requirements.txt、代码重构与后续进阶学习路线）。
#
# 四、 开启新对话的交接指令