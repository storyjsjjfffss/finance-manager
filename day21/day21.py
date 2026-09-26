import json
DEFAULT_FILE = "tasks.json"


def load_tasks(filepath='task.json'):
    try:
        with open(filepath, 'r',encoding="utf-8") as f:
            json_data = json.load(f)
            print(f'[correct] 导出成功！')
            print(json_data)
            return json_data
    except FileNotFoundError as e:
        print(f'[failure] 未找到指定的文件！{filepath}')
        return []
    except json.decoder.JSONDecodeError as e:
        print(f'[failure] json文件解析失败')
        return []

def save_tasks(tasks, filepath='task.json'):
    try:
        with open(filepath, 'w',encoding='utf-8') as f:
            json.dump(tasks, f, indent=4, ensure_ascii=False)
            print(f'[correct] 上传成功！')
            return True
    except FileNotFoundError as e:
        print(f'[failure] 未找到指定的文件！{filepath}')
        return False

def add_tasks(tasks,title,filepath='task.json'):
    if title.strip() == '':
        raise ValueError("任务标日不能为空")
    tasks.append({'id':len(tasks)+1,'title':title,'status':'pending'})
    try:
        with open('task.json', 'w', encoding='utf-8') as f:
            json.dump(tasks, f, indent=4, ensure_ascii=False)
            print(f'[correct] 已添加到文件{filepath}中。')
            return True
    except FileNotFoundError as e:
        print(f'[failure] 未找到指定的文件！{filepath}')
        return False

def complete_tasks(tasks,task_id):
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = 'complete'
            save_tasks(tasks)
            print(f'任务{task_id}已完成')
            return task
    raise LookupError(f"未找到 ID 为 {task_id} 的任务！")

if __name__ == '__main__':
    tasks= load_tasks()
    print("首次登录需要先进行查看1")
    while True:
        print("1. 查看任务  2. 添加任务  3. 完成任务  q. 退出系统。", end=": ")
        s=input()
        if s=='1':
            tasks=load_tasks()
        elif s=='2':
            try:
                title = input("请输入你想要添加的任务").strip()
                add_tasks(tasks,title)
                print(f'{title}已添加')
            except ValueError as e:
                print(e)
        elif s=='3':
            try:
                tasks_id = int(input("请输入你已经完成的任务id").strip())
                complete_tasks(tasks,tasks_id)
                print(f'该序号{tasks_id}已完成！')
            except (ValueError,LookupError) as e:
                print(e)
        elif s=='q':
            print("您已退出任务管理器！")
            break
        else:
            print(f'指令无效')



