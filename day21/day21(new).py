import json

DEFAULT_FILE = "tasks.json"

def load_tasks(filepath=DEFAULT_FILE):
    """安全读取本地任务文件"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print(f"[提示] 未找到本地存档文件 '{filepath}'，已自动创建新任务池。")
        return []
    except json.decoder.JSONDecodeError:
        print(f"[警告] 存档文件 '{filepath}' 格式损坏，已重置为空任务池。")
        return []

def save_tasks(tasks, filepath=DEFAULT_FILE):
    """序列化持久化到本地"""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=4, ensure_ascii=False)
            return True
    except Exception as e:
        print(f"[错误] 保存文件失败: {e}")
        return False

def add_task(tasks, title, filepath=DEFAULT_FILE):
    """新增任务并触发保存"""
    clean_title = title.strip()
    if not clean_title:
        raise ValueError("任务标题不能为空！")

    # 动态获取当前最大 ID 并 +1，避免重复
    new_id = max([t["id"] for t in tasks], default=0) + 1
    new_item = {"id": new_id, "title": clean_title, "status": "pending"}
    tasks.append(new_item)

    # 复用通用保存函数
    save_tasks(tasks, filepath)
    return new_item

def complete_task(tasks, task_id, filepath=DEFAULT_FILE):
    """完成任务并同步保存"""
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "completed"
            save_tasks(tasks, filepath)
            return task
    raise LookupError(f"未找到 ID 为 {task_id} 的任务！")

def display_tasks(tasks):
    """格式化展示任务清单"""
    if not tasks:
        print("\n--- 暂无任何待办任务 ---")
        return

    print("\n" + "=" * 12 + " 待办任务清单 " + "=" * 12)
    for t in tasks:
        # pending 显示待办，completed 显示已完成
        status_tag = "✅ [已完成]" if t["status"] == "completed" else "⏳ [待办中]"
        print(f"ID: {t['id']:<3} | 状态: {status_tag} | 任务: {t['title']}")
    print("=" * 38)

if __name__ == "__main__":
    # 启动时自动加载历史数据，彻底杜绝数据覆盖清空
    tasks = load_tasks()

    while True:
        print("\n1. 查看任务  2. 添加任务  3. 完成任务  q. 退出系统")
        action = input("请选择操作: ").strip()

        if action == "1":
            display_tasks(tasks)

        elif action == "2":
            title_input = input("请输入任务内容: ")
            try:
                item = add_task(tasks, title_input)
                print(f"[成功] 任务已添加 (ID: {item['id']})")
            except ValueError as e:
                print(f"[错误] {e}")

        elif action == "3":
            try:
                task_id_input = int(input("请输入已完成的任务 ID: ").strip())
                complete_task(tasks, task_id_input)
                print(f"[成功] ID 为 {task_id_input} 的任务状态已更新为已完成！")
            except ValueError:
                print("[错误] 任务 ID 必须是纯整数！")
            except LookupError as e:
                print(f"[错误] {e}")

        elif action.lower() == "q":
            print("数据已持久化，已安全退出系统。")
            break
        else:
            print("[提示] 指令无效，请输入 1/2/3 或 q。")