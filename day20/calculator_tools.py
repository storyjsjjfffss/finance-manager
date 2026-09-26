# calculator_tools.py
"""通用算术计算工具模块"""

def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("除数不能为零！")
    return a / b

# 自测隔离防火墙
if __name__ == "__main__":
    print("[calculator_tools 自测运行中...]")
    print("5 + 3 =", add(5, 3))
    print("10 / 2 =", divide(10, 2))
    print(f"当前模块的名字 __name__ 是: '{__name__}'")