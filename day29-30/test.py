import json
from datetime import datetime
from collections import defaultdict


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

def load_transactions(filepath):
    transactions = []                      # ① 准备空列表装对象
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)            # ② 读出来是列表套字典
        for item in data:                  # ③ 遍历每个字典
            transactions.append(Transaction(          # ④ 把字典"喂"给构造器
                amount=item["amount"],                # 按字段名传参
                category=item["category"],
                t_type=item.get("t_type", "支出"),    # get 兜底，缺了用默认
                date_str=item.get("date_str")         # 缺了会在 __init__ 里自动取当前时间
            ))
    except (FileNotFoundError, json.JSONDecodeError):
        print("加载失败，返回空列表")
        return []
    return transactions                      # ⑤ 返回对象列表

if __name__ == "__main__":
