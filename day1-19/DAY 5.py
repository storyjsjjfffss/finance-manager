# # 演示逻辑运算符组合与括号
# is_weekend = True
# has_homework = False
#
# # 只有在周末且没有作业时才可以打游戏
# can_play_game = is_weekend and not has_homework
# print(f"可以打游戏吗？ {can_play_game}")
#
# # 演示取模判断整除：能够被 2 整除且能被 3 整除（即能被 6 整除）
# num = 12
# is_divisible_by_6 = (num % 2 == 0) and (num % 3 == 0)
# print(f"{num} 能被 6 整除吗？ {is_divisible_by_6}")
from operator import truediv

# is_weekend = True
# has_homework = True
# play_game = is_weekend and has_homework
# print(f"can i play games? {play_game}")

years=int(input("Enter the number of years: "))
leap_years=(years%4 == 0 and years%100 != 0) and (years%400 == 0)
print(leap_years)

a = int(input("Enter the first length: "))
b = int(input("Enter the second length: "))
c = int(input("Enter the third length: "))

tri=a>0 and b>0 and c>0 and a+b>c and b+c>a and c+b>a
if tri:
    print("可以构成三角形")
if not tri:
    print("无法构成有效三角形")