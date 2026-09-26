import security_util
import json

def save_users(filename,users_data):
    with open(filename,'w',encoding="utf-8") as f:
        json.dump(users_data,f,indent=4,ensure_ascii=False)

def register_user():
    while True:
        password = input('Enter your password: ')

        try:
            security_util.validate_password(password)
        except ValueError as e:
            print(f'[失败] 密码不合规：{e}')
        else:
            print(f"[成功] 密码为{password}，请记好！")
            save_users("password_save.json",password)
            break

if __name__ == '__main__':
    print("=== 欢迎使用用户安全管理系统 ===")
    register_user()

