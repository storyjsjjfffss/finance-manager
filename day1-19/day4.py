# age=int(input("Enter your age:"))
# if age < 0:
#     print("输入无效，年纪不可以为负！")
# elif age < 18:
#     print("未成年通道，半价")
# elif age < 65:
#     print("全价")
# else:
#     print("免费")


score = float(input("Enter your score: "))
if score<0 or score>100:
    print("Invalid score")
elif score >= 90 and score <= 100:
    print("A")
elif score >= 80 and score < 90:
    print("B")
elif score >= 70 and score < 80:
    print("C")
elif score >= 60 and score < 70:
    print("D")
else:
    print("F")
