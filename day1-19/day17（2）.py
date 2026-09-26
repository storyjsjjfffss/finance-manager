products = [
    {"name": "机械键盘", "price": 299.0, "sales": 850},
    {"name": "无线鼠标", "price": 89.0, "sales": 2300},
    {"name": "4K显示器", "price": 1499.0, "sales": 320},
    {"name": "降噪耳机", "price": 599.0, "sales": 1100}
]
price_product=sorted(products, key=lambda x: x["price"], reverse=True)
sale_product=sorted(products, key=lambda x: x["sales"], reverse=True)

#task2 脏文本流水线清理

raw_tags = ["  python ", "", "  AI ", "   ", "backend  ", "DATA "]
filter_tags = filter(lambda x:x.strip()!="", raw_tags)
map_tags=map(lambda x:x.strip().lower(),filter_tags)
print(list(map_tags))
