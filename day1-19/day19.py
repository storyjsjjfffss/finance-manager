# 操作场景	函数名	功能说明	核心参数提示
# 内存字符串互转
# json.dumps(obj)	将 Python 字典/列表序列化为 JSON 字符串	 ensure_ascii=False（保留中文）
# indent=4（格式化缩进排版）
# json.loads(s)	将 JSON 格式字符串反序列化为 Python 原生对象	传入合法 JSON 字符串

# 文件流直接读写
# json.dump(obj, f)	将 Python 对象直接序列化并写入文件对象	配合 with open(..., "w")
# json.load(f)	从文件对象中直接读取并还原为 Python 对象	配合 with open(..., "r")

import json

# 1. 结构化数据准备
system_config = {
    "app_name": "TaskMaster",
    "version": 1.2,
    "debug_mode": False,
    "allowed_roles": ["admin", "developer", "guest"],
    "database": {
        "host": "localhost",
        "port": 3306
    }
}

# 2. 序列化写入本地 config.json
with open("config.json", "w", encoding="utf-8") as f:
    # indent=4 让生成的 JSON 缩进换行，可读性极高
    # ensure_ascii=False 确保中文和特殊字符原样显示，不被转义成 \uXXXX
    json.dump(system_config, f, indent=4, ensure_ascii=False)

print("[成功] 配置文件写入完成。")

# 3. 完整异常防御读取流程
def load_app_config(filepath):
    print(f"\n正在尝试加载配置文件: {filepath}")
    file_obj = None
    try:
        file_obj = open(filepath, "r", encoding="utf-8")
        data = json.load(file_obj)
        # 业务逻辑校验：如果配置中缺少必要字段，主动报错
        if "version" not in data:
            raise KeyError("配置文件格式损坏：缺失 'version' 字段！")
    except FileNotFoundError:
        print(f"[错误] 文件未找到，请确认路径: {filepath}")
        return None
    except json.JSONDecodeError as err:
        print(f"[错误] JSON 语法损坏，无法解析！详情: {err}")
        return None
    except KeyError as err:
        print(f"[业务异常] {err}")
        return None
    else:
        # 只有读取且解析完全成功时才执行
        print(f"[正常] 配置加载成功！当前应用: {data['app_name']} v{data['version']}")
        return data
    finally:
        # 无论成功或捕获异常，清理文件句柄
        if file_obj and not file_obj.closed:
            file_obj.close()
            print("[清理] 文件流安全释放。")

# 测试正常加载
load_app_config("config.json")

# 测试不存在的文件
load_app_config("non_existent.json")