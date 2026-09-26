#一行列表推导式

# 传统写法（4 行）
# squares = []
# for x in range(1, 6):
#     squares.append(x ** 2)

# 列表推导式写法（1 行）
# squares = [x ** 2 for x in range(1, 6)]

# squares = []
# for i in range(1,11):
#     squares.append(i**2)
#
# squares=[x**2 for x in range(1,11)]
#
# for i,j in enumerate(squares):#经典列表遍历
#     print(i,j)
#
# squares=[x*2 for x in squares]
#
# for i,j in enumerate(squares):#经典列表遍历
#     print(i,j)
#

# numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#
# # 1. 筛选偶数
# evens = [n for n in numbers if n % 2 == 0]
# print("偶数列表:", evens)
#
# # 2. 筛选奇数并计算立方
# odd_cubes = [n ** 3 for n in numbers if n % 2 != 0]
# print("奇数立方:", odd_cubes)
#
# # 3. 批量字符串处理
# names = ["alice", "bob", "charlie"]
# capitalized_names = [name.capitalize() for name in names]
# print("首字母大写:", capitalized_names)  # ['Alice', 'Bob', 'Charlie']
#dask1 偶数平方列表
numbers = [x for x in range(1,51)]
new_numbers =[x**2 for x in numbers if x%2==0]
#话可以合并
print(new_numbers)
print(len(new_numbers))
#dask2 字符串批量清洗和过滤
raw_skills = ["PYTHON", "GO", "JAVASCRIPT", "C", "SQL", "DOCKER", "AI"]
new_raw_skills = [i.capitalize() for i in raw_skills if len(i)>2]
#capitalize()是首字母大写、其余字母小写，CG->Cg！
print(new_raw_skills)


