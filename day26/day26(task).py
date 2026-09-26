class Item:
    def __init__(self,name:str,price:float):
        self.name=name
        self.price=price
    def __str__(self):
        return f"Item('{self.name}',${self.price})"
    def __repr__(self):
        return f"Item('{self.name}',{self.price})"
    def __eq__(self,other):
        if isinstance(other,Item):
            return self.name==other.name and self.price==other.price
        else:
            return False
class Cart:
    def __init__(self):
        self.items=[]
    def add_item(self,item:Item):
        self.items.append(item)
    def __len__(self):
        return len(self.items)
    def __add__(self,other):
        if isinstance(other,Cart):
            new_cart=Cart()

            new_cart.items=self.items+other.items
            return new_cart
        else:
            return NotImplemented
    def __str__(self):
        total_price=0
        #total_price = sum(item.price for item in self.items)
        for item in self.items:
            total_price+=item.price
        return f"购物车包含 {len(self.items)} 件商品，总金额: ¥{total_price:.2f}"

if __name__=="__main__":
    apple=Item("apple",5.0)
    milk=Item("milk",12.0)
    bread=Item("bread",8.0)
    if apple==Item("apple",5.0):
        print(f"等于")
    else:
        print("不等于")
    C1=Cart()
    C0=Cart()
    C0.add_item(apple)
    C0.add_item(bread)
    C1.add_item(milk)
    print(f"已有商品数{len(C1.items)}")
    C_total=C1+C0
    print(C_total)
