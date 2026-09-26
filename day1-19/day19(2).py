import json
def save_users(filename,users_data):
    with open(filename,'w',encoding="utf-8") as f:
        json.dump(users_data,f,indent=4,ensure_ascii=False)
        #json和write的区别，json可以收很多类型，比如字典之类的，write只接受字符串

def load_users(filename):
    print('正在加载配置文件')
    file_obj=None
    try:
        file_obj=open(filename, 'r', encoding="utf-8")
        data=json.load(file_obj)
    except FileNotFoundError:
        print(f"[error]文件未找到，请检查文件名{filename}")
        return []
    except json.decoder.JSONDecodeError as err:
        print(f"[error]JSON语法错误，详情{err}")
        return []
    except KeyError as err:
        print(f'业务异常{err}')
        return []
    else:
        print(f"成功加载{len(data)}名用户")
        return data
    finally:
        if file_obj is not None and not file_obj.closed:
            file_obj.close()
            print("[清理] 文件流安全释放。")

users = [
    {"id": 1, "name": "Alex",  "age": 20, "email": "alex@example.com",  "role": "admin"},
    {"id": 2, "name": "bob",   "age": 22, "email": "bob@example.com",   "role": "developer"},
    {"id": 3, "name": "Kasai", "age": 19, "email": "kasai@example.com", "role": "guest"}
]

save_users('config.json',users)
user_data=load_users('config.json')
print(user_data)
#精进
def load_users_pythonic(filename):
    print('正在加载配置文件...')
    try:
        # with 会自动处理文件关闭，即便是抛出 JSONDecodeError 也会安全释放
        with open(filename, 'r', encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"[error] 文件未找到，请检查文件名: {filename}")
        return []
    except json.decoder.JSONDecodeError as err:
        print(f"[error] JSON 语法错误，详情: {err}")
        return []
    else:
        print(f"成功加载 {len(data)} 名用户")
        return data