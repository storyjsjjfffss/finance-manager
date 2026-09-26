from datetime import datetime, timedelta
from collections import Counter, defaultdict

now = datetime.now()
expire_str = "2026-11-15"
expire=datetime.strptime(expire_str, "%Y-%m-%d")
time_left = expire - now
Day_left = time_left.days
print(Day_left ,"天")


search_keywords = ["手机", "耳机", "手机", "电脑", "手机", "键盘", "耳机"]
user_purchases = [("Alex", "鼠标"), ("Bob", "键盘"), ("Alex", "显示器"), ("Alex", "耳机")]

list1 = Counter(search_keywords)
print(list1.most_common(2))

list2 = defaultdict(list)
for name, purchase in user_purchases:
    list2[name].append(purchase)
print(list2)