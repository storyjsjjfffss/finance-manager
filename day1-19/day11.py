#字典（Dictionary）基础。
#键（Key）的约束：必须是不可变且唯一的类型（通常是字符串或整数）。如果出现重复的 Key，后面的值会覆盖前面的值。
#值（Value）：可以是任何 Python 数据类型（包括数字、字符串、列表甚至另一个字典）。
# 结构: {键1: 值1, 键2: 值2}
# user = {"name": "Alex", "age": 20, "is_admin": False}
# student = {"name": "Charlie", "math": 88}
#
# # 1. 增与改
# student["english"] = 95  # 新增键 english
# student["math"] = 92     # 修改键 math 的值
#
# # 2. 安全取值 .get()
# print("姓名:", student.get("name"))
# print("物理成绩:", student.get("physics", "缺考"))  # 不会报错，输出“缺考”
#
# # 3. 遍历字典
# print("\n--- 遍历字典的所有项 ---")
# for subject, score in student.items():#.items()字典自带的函数，返回所有键值对
#     print(f"科目: {subject} -> 分数: {score}")


text= "apple banana apple orange banana apple"
words = text.split()
words_count={}
# for word in words:
#     if word in words_count:
#         words_count[word]+=1
#     else:
#         words_count[word]=1

for word in words:
    words_count[word]=words_count.get(word,0)+1
for word, count in words_count.items():
    print(f"{word}: {count}")

