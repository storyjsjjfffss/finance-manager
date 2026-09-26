class Item:
    def __init__(self, name:str,value:int):
        self.name = name
        self.value = value
    def __str__(self):
        return f"{self.name}价值{self.value}金币"
class Weapon(Item):
    def __init__(self,name:str,value:int,extra_atk:int):
        super().__init__(name,value)
        self.extra_atk = extra_atk
    def __str__(self):
        return f"{self.name}价值{self.value}金币,附加{self.extra_atk}额外伤害"
class Potion(Item):
    def __init__(self,name:str,value:int,heal_hp:int):
        super().__init__(name,value)
        self.heal_hp = heal_hp
    def __str__(self):
        return f"{self.name}价值{self.value}金币,使用恢复{self.heal_hp}点血量"

class Inventory:
    capacity: int = 5
    def __init__(self):
        self.items = []


    def add_item(self,item:Item):

        if len(self.items) >= self.capacity:
            raise ValueError(f"库存已满，容量达到上限{self.capacity}")
        self.items.append(item)
    def remove_item(self,item:Item)->Item:
        self.items.remove(item)
        return item
    def __len__(self):
        return len(self.items)
    def __str__(self):
        if len(self.items) == 0:
            return "你的背包空空如也"
        else:
            for ID, item in enumerate(self.items,1):
                return f"{ID},{item}"
class Character:
    def __init__(self,name:str, hp:int,max_hp:int,base_atk:int):
        self.name = name
        self.Hp = hp
        self._max_hp = max_hp
        self.__base_atk = base_atk
        self.bag=Inventory()
        self.equipped_weapon=None
    @property
    def hp(self):
        return self._max_hp
    @property
    def base_atk(self):
        return self.__base_atk
    def equip(self,weapon:Weapon):
        self.equipped_weapon=weapon
    @property
    def total_atk(self):

        self.__base_atk=self.__base_atk + (self.equipped_weapon.extra_atk if self.equipped_weapon else 0)
        return self.__base_atk

    def take_damage(self,damage:int):
        self.Hp = max(self.Hp-damage, 0)
        print(f'受到了{damage}点伤害！')
    def attack(self,target):
        target.Hp-=self.base_atk
        print(f'对{target.name}造成了{self.base_atk}点伤害')
    def use_potion(self,potion:Potion):
        self.Hp=min(potion.heal_hp+self.Hp,self._max_hp)
        self.bag.remove_item(potion)
        print(f"已恢复到{self.Hp}生命值。")
        print(f"{potion.name}已经移除。")
class Warrior(Character):
    def __init__(self,name:str,hp:int,max_hp:int,base_atk:int):
        super().__init__(name,hp,max_hp,base_atk)
    def attack(self,target):
        # 比如：血量低于上限的 30% 时，攻击 ×1.5（狂暴）
        if self.Hp < self._max_hp * 0.3:
            target.Hp -= self.base_atk * 1.5
            print(f'对{target.name}造成了{self.base_atk*1.5}点伤害')
        else:
            target.Hp -= self.base_atk
            print(f'对{target.name}造成了{self.base_atk}点伤害')


if __name__ == '__main__':
    iron_sword=Weapon("铁剑",value=50,extra_atk=15)
    red_potion = Potion("小型生命药水", value=20, heal_hp=50)
    player = Warrior("亚瑟",hp=100, max_hp=100, base_atk=20)
    player.bag.add_item(iron_sword)
    player.bag.add_item(red_potion)
    print(player.bag)
    player.equip(player.bag.remove_item(iron_sword))
    print(f"玩家的攻击力是{player.total_atk}")
    monster_g = Character("哥布林",150,150,20)
    while True:
        player.attack(monster_g)
        if monster_g.Hp <= 0:
            print(f"您已击败{monster_g.name}!")
            break
        if player.Hp<=player.hp*0.3:
            player.use_potion(red_potion)

        monster_g.attack(player)

        if player.Hp <= 0:
            print(f"您已经阵亡{player.name}!")
            break









