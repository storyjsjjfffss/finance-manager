user_alex_tags = ["编程", "羽毛球", "电影", "摄影", "编程", "电影"]
user_bob_tags = ["音乐", "摄影", "羽毛球", "骑行", "音乐"]
alex_set=set(user_alex_tags)
bob_set=set(user_bob_tags)
print(alex_set)
print(bob_set)
intersection=alex_set & bob_set
union=alex_set | bob_set
repeat=float(len(intersection))/float(len(union))
print(intersection)
print(union)
print(repeat)