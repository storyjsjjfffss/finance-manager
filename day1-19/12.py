#嵌套数据结构与简易通讯录
#形式 A：列表套字典（List of Dicts）
students=[
    {"name":"Alex","age":20,"score":90},
    {"name":"Bov","age":23,"score":78}
]
#形式 B：字典套字典（Dict of Dicts）
# contacts = {
#     "Alex":{"phone":"12800000000","email":"alex@example.com"},
#     "bob":{"phone":"12344444444","email":"bob@example.com"}
# }
# print(contacts["Alex"]["phone"])
# #嵌套取值与逐层安全访问
# info = contacts.get("Kasai",{})
# phone=info.get("phone","未登记")
# print(phone)
#
# products = [
#     {"id":101,'name':'键盘','tags':['数码','外设']},
#     {"id":102,'name':'显示器','tags':['数码','办公']}
# ]
# for product in products:
#     print(f'商品：{product["name"]}，标签：{product["tags"]}')

address_book={

}
print("===","通讯录管理系统","===")
print('1. 新增/更新  2. 查询  3. 查看全部  q. 退出')
while True:

    action=input("请选择操作：")
    try:
        if action=="1":
            new_human=input("请输入姓名:")
            if new_human in address_book:

                while True:
                    yon = input("是否修改已有联系人的手机号(继续按y,放弃按n):")
                    if yon.lower() == "y":
                        address_book[new_human] = {"phone": input("请输入电话:"), "email": input("请输入邮箱:")}
                        print(f"[成功] 联系人{new_human}已保存。")
                        break
                    elif yon.lower() == "n":
                        print("已放弃选择")
                        break
                    else:
                        print('输入无效')
                        continue
            elif new_human not in address_book:
                address_book[new_human]={"phone":input("请输入电话:"),"email":input("请输入邮箱:")}
                print(f"[成功] 联系人{new_human}已保存。")
            else:
                print('输入无效')
        elif action=="2":
            inqu =input('请输入要查询的对象：')
            if inqu in address_book:
                print(f"姓名：{inqu}|邮箱：{address_book[inqu]['email']}|电话：{address_book[inqu]['phone']}")
            else:
                print("没有该联系人")
        elif action=="3":
            for human in address_book:
                print(f"姓名：{human}|邮箱：{address_book[human]['email']}|电话：{address_book[human]['phone']}")
        elif action=="q":
            break
        else:
            print('请输入正确的指令')

    except ValueError:
        print("请输入正确的选择")
