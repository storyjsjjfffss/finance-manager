import json
from datetime import datetime
from collections import defaultdict


# ==========================================
# 第一层：数据模型层
# ==========================================
class Transaction:
    """单笔账单数据模型"""

    def __init__(self, amount: float, category: str, t_type: str = "支出", date_str: str = None):
        self.amount = amount
        self.category = category
        self.t_type = t_type
        # 若未提供时间，自动获取当前时间并格式化
        self.date_str = date_str if date_str else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        """序列化辅助：将对象转为字典，方便存入 JSON"""
        return {
            "amount": self.amount,
            "category": self.category,
            "t_type": self.t_type,
            "date_str": self.date_str
        }

    def __str__(self):
        # 任务 1：重写魔法方法 (Day 26)

        # 要求：返回格式如 "[支出] 餐饮: ¥50.00 (时间: 2026-09-25 12:00:00)"
        return f"[{self.t_type}] {self.category}: ${self.amount:.2f} (时间：{self.date_str}）"


# ==========================================
# 第二层：业务控制层
# ==========================================
class FinanceManager:
    """财务业务逻辑控制器"""

    def __init__(self, filepath="finance_data.json"):
        self.filepath = filepath
        # 启动时自动加载历史数据
        self.transactions = self.load_data()

    def load_data(self) -> list:
        # 任务 2：JSON 异常防御读取 (Day 19 & 21)
        # 要求：
        # 1. 尝试使用 with open 和 json.load 读取 self.filepath。
        # 2. 如果 FileNotFoundError 或 JSONDecodeError，捕获并返回 []。
        # 3. 如果成功读取到了字典列表，需要将其遍历，把每个字典转换回 Transaction 实例对象，最后返回包含对象的列表。
        try:
            transaction_list=[]
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    transaction_list.append(Transaction(**item))
            return transaction_list

        except FileNotFoundError:
            return []
        except json.decoder.JSONDecodeError:
            return []

    def save_data(self):
        # 任务 3：JSON 序列化写入 (Day 19 & 21)
        # 要求：
        # 1. 遍历 self.transactions，调用每个对象的 to_dict() 方法，生成一个字典列表。
        # 2. 将字典列表 json.dump 写入 self.filepath (缩进4格，支持中文)。
        dict_list =[]
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                for transaction in self.transactions:
                    dict_list.append(transaction.to_dict())
                #dict_list = [t.to_dict() for t in self.transactions]
                json.dump(dict_list, f, ensure_ascii=False, indent=4)
            print("save")
        except FileNotFoundError as e:
            print(e)



    def add_record(self, amount: float, category: str, t_type: str):
        """新增一条账单"""
        if amount <= 0:
            raise ValueError("记账金额必须大于 0！")

        new_t = Transaction(amount, category, t_type)
        self.transactions.append(new_t)
        self.save_data()
        return new_t

    def generate_report(self):
        # 任务 4：生成财务报表 (Day 28)
        # 要求：
        # 1. 实例化一个 defaultdict(float) 命名为 expense_summary。
        # 2. 遍历 self.transactions，如果账单类型 (t_type) 是 "支出"，则将金额累加到对应的 category 键中。
        # 3. 打印出各个分类的总支出。

        expense_summary=defaultdict(float)
        for transaction in self.transactions:
            if transaction.t_type== "支出":
                expense_summary[transaction.category] += transaction.amount
        for category in expense_summary:
            print(category, expense_summary[category])



# ==========================================
# 第三层：视图交互层 (已为你写好)
# ==========================================
def main():
    print("=" * 40)
    print("欢迎使用 个人财务管家 (Finance Master)")
    print("=" * 40)

    manager = FinanceManager()

    while True:
        print("\n1. 记一笔支出  2. 记一笔收入  3. 查看流水  4. 财务报表  q. 退出")
        choice = input("请选择操作: ").strip().lower()

        if choice == '1':
            cat = input("请输入支出分类 (如 餐饮/交通/购物): ")
            try:
                amt = float(input("请输入金额: "))
                item = manager.add_record(amt, cat, "支出")
                print(f"✅ 记录成功: {item}")
            except ValueError as e:
                print(f"❌ 输入有误: {e}")

        elif choice == '2':
            cat = input("请输入收入来源 (如 工资/理财/外包): ")
            try:
                amt = float(input("请输入金额: "))
                item = manager.add_record(amt, cat, "收入")
                print(f"✅ 记录成功: {item}")
            except ValueError as e:
                print(f"❌ 输入有误: {e}")

        elif choice == '3':
            print("\n--- 历史账单流水 ---")
            if not manager.transactions:
                print("暂无任何账单记录。")
            else:
                for t in manager.transactions:
                    print(t)

        elif choice == '4':
            manager.generate_report()

        elif choice == 'q':
            print("数据已安全同步，感谢使用！再见！")
            break

        else:
            print("⚠️ 无效指令，请重新输入。")


if __name__ == "__main__":
    main()