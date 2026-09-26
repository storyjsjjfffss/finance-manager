class Currency:
    """金额货币类，重载加法与相等比较"""
    def __init__(self, amount: float, unit: str = "CNY"):
        self.amount = round(amount, 2)
        self.unit = unit

    # 1. 普通字符串展示 (print)
    def __str__(self):
        return f"{self.amount:.2f} {self.unit}"

    # 2. 调试器与列表显示
    def __repr__(self):
        return f"Currency(amount={self.amount}, unit='{self.unit}')"

    # 3. 运算符重载: +
    def __add__(self, other):
        if not isinstance(other, Currency):
            raise TypeError("只能对两个 Currency 对象执行加法！")
        if self.unit != other.unit:
            raise ValueError(f"币种不匹配，无法直接相加: {self.unit} vs {other.unit}")
        # 返回一个全新的 Currency 实例
        return Currency(self.amount + other.amount, self.unit)

    # 4. 相等比较: ==
    def __eq__(self, other):
        if isinstance(other, Currency):
            return self.amount == other.amount and self.unit == other.unit
        return False


# --- 测试魔法方法效果 ---
c1 = Currency(100.5, "CNY")
c2 = Currency(50.2, "CNY")

# 触发 __str__
print("打印 c1:", c1)  # 输出: 100.50 CNY

# 触发 __add__
c3 = c1 + c2
print("加法计算结果 c3:", c3)  # 输出: 150.70 CNY

# 触发 __eq__
print("c1 是否等于 Currency(100.5):", c1 == Currency(100.5, "CNY"))  # True

# 放在列表里触发 __repr__
wallet = [c1, c2, c3]
print("钱包列表:", wallet)