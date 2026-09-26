# # 1. 演示 range 的步长与区间特性
# print("步长为 2 的遍历:")
# for i in range(1, 8, 2):
#     print(i, end=" -> ")#print() 内部默认设置了 end="\n",如果不用end结尾的话，结果就是还是会换行
# print("结束")
#
# # 2. 累加求和思想（累加器模式）
# total = 0
# for n in range(1, 11):
#     total += n  # 等价于 total = total + n
# print(f"1 到 10 的累加和为: {total}")
#
# # 3. 双重循环初体验（打印 3行 4列 的星号矩阵）
# print("\n3x4 矩阵:")
# for row in range(3):
#     for col in range(4):
#         print("*", end=" ")
#     print()  # 内层循环每跑完一行，换一行

# print("步长为二的遍历")
# for i in range(1,10,2):
#     print(i,end="->")
# print("end")
# total = 0
# for i in range(1,10,2):
#     total += i
# print(f"1,3,5,,7,9的和{total}")
#
# print("\n3*4矩阵")
# for row in range(3):
#     for col in range(4):
#         print("*",end=" ")
#     print()

total =0
for i in range(1,101):
    total += i
print(total)
for row in range(1,10):
    for col in range(1,row+1):
        print(f"{col}*{row}={col*row}",end=" ")
    print()
