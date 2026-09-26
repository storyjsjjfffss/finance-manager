class Student:
    """定义学生类"""
    def __init__(self, name, grade):
        # 绑定实例属性
        self.name = name
        self.grade = grade
        self.scores = []  # 每个学生自带一个独立的成绩单

    def add_score(self, score):
        """向当前学生成绩单添加分数"""
        if 0 <= score <= 100:
            self.scores.append(score)
        else:
            print("分数必须在 0 到 100 之间！")

    def get_average(self):
        """计算当前学生的平均分"""
        if not self.scores:
            return 0.0
        return sum(self.scores) / len(self.scores)

    def print_report(self):
        """打印学生专属学情报告"""
        avg = self.get_average()
        print(f"学生 [{self.name}] | 年级: {self.grade} | 平均分: {avg:.1f} | 录入总科数: {len(self.scores)}")


# --- 实例化并测试 ---
# 实例化两个完全独立的学生对象
s1 = Student("Alex", "高二")
s2 = Student("Bob", "高三")

# 分别操作各自的方法
s1.add_score(90)
s1.add_score(80)

s2.add_score(95)
s2.add_score(100)
s2.add_score(90)

# 输出各自的报告（数据互不干扰）
s1.print_report()
s2.print_report()