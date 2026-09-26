# tasks = ["写代码", "吃午饭", "散步"]
#
# # 1. 访问与修改元素
# print("第一项任务:", tasks[0])
# print("最后一项任务:", tasks[-1])
# tasks[1] = "吃健康轻食"  # 直接根据索引修改内容
#
# # 2. 追加与弹出
# tasks.append("读技术书籍")  # 末尾追加
# tasks.append("刷抖音")
# print("追加后:", tasks)
#
# finished = tasks.pop(0)    # 弹出第一个任务
# not_wanted = tasks.pop(-1)
# print(f"已完成并移除了: {finished}")
# print(f"不想干的: {not_wanted}")
# print("剩余任务:", tasks)
# print("当前待办总数:", len(tasks))
#

todos = []

while True:
    print("=== 我的待办清单 ===")
    if len(todos) == 0:
        print("(暂无任务)")
        print("-----------------")
    else:
        for i,item in enumerate(todos,1):
            print(f"{i}.{item}")

        print("-"*20)
    print("请选择：1.新增  2.删除 q.退出:",end=" ")
    cin =input()

    if cin == "1":
        print("请输入新任务:",end=" ")
        todos.append(input())
    elif cin == "2":
        print("请输入要删除的任务编号:",end=" ")
        n=int(input())
        if 1 <= n <= len(todos):
            removed = todos.pop(n - 1)
            print(f"已删除任务：{removed}")
        else:
            print("编号不存在，失败")
    #1 raw_input = input("请输入要删除的任务编号: ")
    #
    # # 1. 检查是否为纯数字字符串
    # if raw_input.isdigit():
    #     n = int(raw_input)
    #     # 2. 检查数字是否在有效范围内
    #     if 1 <= n <= len(todos):
    #         removed = todos.pop(n - 1)
    #         print(f"已删除任务：{removed}")
    #     else:
    #         print("编号超出范围，删除失败！")
    # else:
    #     print("输入无效！请输入有效的数字编号。")

    #2 try:
    #     n = int(input("请输入要删除的任务编号: "))
    #     if 1 <= n <= len(todos):
    #         removed = todos.pop(n - 1)
    #         print(f"已删除任务：{removed}")
    #     else:
    #         print("编号超出范围，删除失败！")
    # except ValueError:
    #     # 只要用户输入的不是整数（比如输了字符串、浮点数或乱码），就会跳转到这里
    #     print("输入错误：必须输入有效的整数编号！")
    elif cin == "q":
        print("您已退出")
        break
    else:
        print("指令无效，请重新输入")
    print()


