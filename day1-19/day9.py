# data = [78.5, 95.0, 62.0, 88.5, 91.0]
#
# # 聚合统计
# count = len(data)
# total = sum(data)
# average = total / count
# highest = max(data)
# lowest = min(data)
#
# print(f"数据总数: {count}")
# print(f"总和: {total:.2f}")
# print(f"平均值: {average:.2f}")
# print(f"极值: 最高 {highest}, 最低 {lowest}")
#
# # 降序排列展示
# sorted_desc = sorted(data, reverse=True)
# print("降序结果:", sorted_desc)
grades = []
count=0
while True:
    try:
        grade = input("请输入一个成绩（输入q结束录入）: ")

        if grade.lower() == 'q':#无论大小写
            if len(grades) == 0:
                print("未录入任何成绩，无法统计")
                break
            else:
                print("="*10,"成绩分析报告","="*10)
                print(f"录入人数：{count}人")
                print(f"总分：{sum(grades)}")
                print(f"平均分：{sum(grades)/len(grades)}")
                print(f"最高分：{max(grades)}",end="|")
                print(f"最低分：{min(grades)}")
                print("_"*30)
                #print(f"成绩降序排名{grades.sort(reverse=True)}")
                #因为他的返回值是none
                #grades.sort(reverse=True)
                #print(f"成绩降序排名：{grades}")
                print(f"成绩降序排名{sorted(grades)}")
                print("="*30)
                break
        elif 0<=float(grade) <= 100:
            grades.append(float(grade))
            #count多余了，因为可以直接len（），第二个float也多余
            count+=1
        else:
            print("输入错误，请输入有效的数字或者结束字母q")
    except ValueError:
        print("输入错误格式错误")
