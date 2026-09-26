#今日综合实战任务：简易超市收银与库存管理系统
#本程序需要综合运用字典（管理库存与单价）、列表（管理购物车）、流程控制及异常防御。
# 商品库：以商品名称为键，值为包含 price 和 stock 的字典
inventory = {
    "苹果": {"price": 5.5, "stock": 10},
    "面包": {"price": 8.0, "stock": 5},
    "牛奶": {"price": 12.0, "stock": 3}
}

# 购物车：使用列表存放多条购买记录，如 [{"name": "苹果", "amount": 2, "subtotal": 11.0}]
cart = []
print("欢迎来到直博购物系统")
print("想看商品清单请输入1，想添加商品进购物车请输入2，想结帐请输入3,退出输入q")
while True:
    money=0
    request=input("看商品1，添加2，想结3,退出q，请选择：")
    if request=="1":
        for name, item in inventory.items():
            print(f'名称：{name},价格：{item["price"]},库存：{item["stock"]}')
    elif request == "2":
        goods_name = input('请输入你想要购买的商品：')
        if goods_name in inventory and inventory[goods_name]["stock"] > 0:
            try:
                goods_num = int(input("请输入你想要购买的数量"))
                if goods_num <= inventory[goods_name]["stock"] and inventory[goods_name]["stock"] > 0:
                    inventory[goods_name]["stock"] -= goods_num
                    consume = inventory[goods_name]["price"] * goods_num
                    cart.append({"name": goods_name, "amount": goods_num, "subtotal": consume})
                    print(f"您所购买的{goods_name}已加入购物车")
                elif goods_num > inventory[goods_name]["stock"]:
                    print(f"当前的库存不足，当前仅剩下{inventory[goods_name]['stock']}件")
                elif goods_num <= 0:
                    print("您所购买的商品数必须大于等于1")
                else:
                    print('输入错误')
            except ValueError:
                print('输入的格式不对，请重新输入')
        else:#有更改的点，买完，和没有都需要考虑
            print('很抱歉，没能找到你想购买的商品')
    elif request == "3":
        if len(cart) >0:
            for i, item in enumerate(cart,1):
                print(f'{i},商品名称：{item.get("name")},数量：{item.get("amount")},小计{item.get("subtotal")}')
                money+=item.get("subtotal")
            print(f"总计金额{money:.2f}，请支付")
            cart.clear()
        else:
            print('购物车为空，无需结账！')
    elif request.lower() == "q":
        print("期待下次见面")
        break
    else:
        print("无效操作，请重试!")

