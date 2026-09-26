# name = "Alex"
# age=18
# print(f"姓名：{name},年龄{age}")

# user_name= input("Enter your name: ")
# age_text=input("Enter your age: ")
# usr_age=int(age_text)
# pi_val=3.14151836
# print(f"你好，{user_name},明年你的年纪是{usr_age}.")
# print(f"原始的圆周率：{pi_val},保n留两位的结果是：{pi_val:.2f}")

#这里的：是必须要的目的是说明后面是对pi_val的格式化处理，如果直接.2f代表是要在pi找叫做2f的属性
goods=input("输入你想买的商品名字：")
price=input("输入商品价格：")
amount=input("想要购买的个数：")
num_price=int(price)
num_amount=int(amount)
print("====================================")
print("             消费小票                ")
print("====================================")
print(f"商品名称：{goods}")
print(f"购买价格：{num_price:.2f}")
print(f"购买数量{num_amount}")
print("------------------------------------")
print("商品总计价格：", num_amount * num_price)
print("商品九折扣价格：", (num_amount * num_price*0.9 ))