# def greet(name, msg="你好"):
#     return f"{msg}，{name}！"
#
# print(greet("小明"))           # 使用默认值 -> "你好，小明！"
# print(greet("小华", "早上好"))   # 覆盖默认值 -> "早上好，小华！"


# 1. 封装一个计算矩形面积和周长的函数
# def calc_rectangle(width, height):
#     """计算矩形面积与周长，返回多个值（本质是返回一个元组）"""
#     area = width * height
#     perimeter = (width + height) * 2
#     return area, perimeter
#
# # 接收多返回值（解构赋值）
# a, p = calc_rectangle(5, 3)
# print(f"面积: {a}, 周长: {p}")
def calculate_discount(price, level="normal"):#默认参数必须放在非默认参数的后面。
    if level == "vip":
        return price * 0.8
    elif level == "svip":
        return price * 0.7
    else:
        return price

def is_prime(n):
    if n<=1:
        return False
    for i in range(2,int(n**0.5)+1):
        if n % i == 0:
            return False

    return True

while True:
    c=int(input("Enter a number: "))
    print(is_prime(c))
    if c==0:
        break

primes = [i for i in range(1, 51) if is_prime(i)]
print(primes)

for i in range(1,51):
    if is_prime(i):
        print(i,end=" ")
