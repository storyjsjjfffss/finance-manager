# # 1. *args 接收任意多个数值
# def calculate_sum(*args):
#     # args 在函数内部是一个元组，例如 (10, 20, 30)
#     print("接收到的位置参数元组:", args)
#     return sum(args)
#
# print("求和结果:", calculate_sum(1, 2, 3, 4, 5))
#
# # 2. **kwargs 接收任意多个关键字配置
# def print_user_profile(username, **kwargs):
#     print(f"\n用户: {username}")
#     # kwargs 在函数内部是一个字典
#     for key, value in kwargs.items():
#         print(f"  - {key}: {value}")
#
# print_user_profile("Alex", age=24, city="北京", role="Engineer")

def custom_aggregator(mode,*arg):
    if len(arg)==0:
        return 0
    else:
        if mode == "sum":
            return sum(arg)
        elif mode == "avg":
            return round(sum(arg)/len(arg),2)#round到后两位
        else:
            return "未知状态"

print(custom_aggregator("sum",1,2,3,4))
print(custom_aggregator("avg",10,20,35))
print(custom_aggregator("avg"))

def build_insert_query(table_name,**kwargs):
    columns=",".join(kwargs.keys())
    values =",".join([f"'{v}'"for v in kwargs.values()])
    return f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
print(build_insert_query("users", name="Alex", age=25, status="active"))