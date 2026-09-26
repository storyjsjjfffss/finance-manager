# # 1. 覆盖写入文件 (w 模式)
# with open("notes.txt", "w", encoding="utf-8") as f:
#     f.write("Python 文件持久化学习\n")
#     f.write("第二行：掌握 with 语句\n")
#
# # 2. 追加写入文件 (a 模式)
# with open("notes.txt", "a", encoding="utf-8") as f:
#     f.write("第三行：使用 a 模式追加一条新日志\n")
#
# # 3. 逐行流式读取与清洗换行符
# print("--- 读取并打印文件内容 ---")
# with open("notes.txt", "r", encoding="utf-8") as f:
#     for line_num, line in enumerate(f, 1):
#         # line 末尾自带 \n，使用 .strip() 去除首尾空白与换行
#         print(f"第 {line_num} 行: {line.strip()}")

# def record_log(username,action):
#     with open("notes.txt","a",encoding="utf-8") as f:
#         f.write(f"用户{username}执行了操作{action}\n")
#
# record_log("Alex","登录系统")
# record_log("liubei","查看订单")

count=[]


def analyze_file(filename):
    total = 0
    with open(filename,"r",encoding="utf-8") as f:
        for line_number,line in enumerate(f,1):
            print(line_number,line.strip())#line自带换行，去掉换行和空格
            count.extend(line.strip().split())#`count.append(列表)`加一个元素，结果是 "列表套列表"
            #`words.extend(列表)`把列表里的每个单词拆开加进去，结果还是单词列表
        print(line_number)
        print(len(count))
        for i in count:
            if i.lower()=="python":
                total+=1
        print(total)

analyze_file("sample.txt")

#优化，主要是列表推导式
def analyze_file(filename):
    total_lines = 0
    words = []  # 在函数内部初始化容器，保证函数独立与纯粹

    with open(filename, "r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, 1):
            total_lines = line_number
            # 去除换行并分词，用 extend 扁平化加入列表
            words.extend(line.strip().split())

    # 统计出现次数（统一转小写匹配）
    target_count = sum(1 for w in words if w.lower() == "python")

    print("=" * 10, "文本分析报告", "=" * 10)
    print(f"总行数: {total_lines}")
    print(f"总词数: {len(words)}")
    print(f"单词 'python' 出现频次: {target_count}")
    print("=" * 30)

analyze_file("sample.txt")

