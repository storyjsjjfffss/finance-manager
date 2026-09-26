# day20_main.py
import calculator_tools

print(f"--- 启动主程序，当前入口 __name__ 是: '{__name__}' ---")

# 调用导入的模块中的函数
res1 = calculator_tools.add(100, 200)
print(f"跨模块调用加法结果: {res1}")

try:
    res2 = calculator_tools.divide(10, 0)
except ZeroDivisionError as err:
    print(f"捕获模块抛出的异常: {err}")