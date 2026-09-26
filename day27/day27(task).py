from typing import TypeVar


class Item:
    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value

    def __str__(self):
        return f"{self.name}(价值{self.value}金币)"

T = TypeVar('T', bound=Item)

class Weapon(Item):
    def __init__(self, name: str, value: int, extra_atk: int):
        super().__init__(name, value)
        self.extra_atk = extra_atk

    def __str__(self):
        return f"{self.name}(价值{self.value}金币, 附加{self.extra_atk}攻击)"


class Potion(Item):
    def __init__(self, name: str, value: int, heal_hp: int):
        super().__init__(name, value)
        self.heal_hp = heal_hp

    def __str__(self):
        return f"{self.name}(价值{self.value}金币, 恢复{self.heal_hp}生命)"


class Inventory:
    capacity: int = 5

    def __init__(self):
        self.items = []

    def add_item(self, item: Item):
        if len(self.items) >= self.capacity:
            raise OverflowError(f"背包已满，无法装入新物品！")
        self.items.append(item)

    def remove_item(self, item: T) -> T:
        """#进阶用法了属于，定义一个范类，因为如果你不定义，你从背包拿出来就是item了，但要是加了就是进入背包是啥就是啥"""
        if item in self.items:
            self.items.remove(item)
            return item
        raise ValueError("背包中没有该物品！")

    def __len__(self):
        return len(self.items)

    def __str__(self):
        if not self.items:
            return "【背包】空空如也"
        # 正确做法：拼接所有物品信息
        lines = ["【背包物品清单】"]
        #很好，以前循环里加上return太搞了
        for idx, item in enumerate(self.items, 1):
            lines.append(f"{idx}. {item}")
        return "\n".join(lines)


class Character:
    def __init__(self, name: str, max_hp: int, base_atk: int):
        self.name = name
        self.max_hp = max_hp
        self._hp = max_hp  # 使用单下划线：受保护属性，允许子类直接访问
        self._base_atk = base_atk  # 使用单下划线：受保护属性

        self.bag = Inventory()
        self.equipped_weapon = None

    @property
    def hp(self):
        return self._hp

    @property
    def is_alive(self):
        return self._hp > 0

    def equip(self, weapon: Weapon):
        self.equipped_weapon = weapon
        print(f"[{self.name}] 装备了 {weapon.name}！")

    @property
    def total_atk(self):
        # 修复：动态计算并返回，绝不覆盖基础属性
        bonus = self.equipped_weapon.extra_atk if self.equipped_weapon else 0
        return self._base_atk + bonus

    def take_damage(self, damage: int):
        self._hp = max(0, self._hp - damage)
        print(f"[{self.name}] 受到了 {damage} 点伤害，剩余生命: {self._hp}/{self.max_hp}")

    def attack(self, target):
        print(f"[{self.name}] 对 [{target.name}] 发起攻击！")
        target.take_damage(self.total_atk)

    def use_potion(self, potion: Potion):
        if potion in self.bag.items:
            self._hp = min(self.max_hp, self._hp + potion.heal_hp)
            self.bag.remove_item(potion)
            print(f"[{self.name}] 饮用 {potion.name}，恢复至 {self._hp} 生命值。")


class Warrior(Character):
    def __init__(self, name: str, max_hp: int, base_atk: int):
        super().__init__(name, max_hp, base_atk)

    def attack(self, target):
        # 使用单下划线受保护属性，或公共属性 self.total_atk
        damage = self.total_atk

        # 狂怒判定：血量低于 30% 触发 1.5 倍暴击
        if self.hp < self.max_hp * 0.3:
            damage = int(damage * 1.5)
            print(f"🔥 [{self.name}] 触发狂怒！对 [{target.name}] 发起暴击！")
        else:
            print(f"[{self.name}] 对 [{target.name}] 发起攻击！")

        # 必须调用目标的 take_damage 方法
        target.take_damage(damage)


if __name__ == '__main__':
    # 1. 实例化
    iron_sword = Weapon("铁剑", value=50, extra_atk=15)
    red_potion = Potion("小型生命药水", value=20, heal_hp=50)

    player = Warrior("亚瑟", max_hp=100, base_atk=20)
    monster_g = Character("哥布林", max_hp=150, base_atk=25)

    # 2. 拾取与装备
    player.bag.add_item(iron_sword)
    player.bag.add_item(red_potion)
    print(player.bag)

    player.equip(player.bag.remove_item(iron_sword))
    print(f"\n玩家当前总攻击力: {player.total_atk}")

    # 3. 战斗主循环
    print("\n--- 战斗开始 ---")
    while player.is_alive and monster_g.is_alive:
        player.attack(monster_g)

        if not monster_g.is_alive:
            print(f"🏆 您已击败 {monster_g.name}!")
            break

        # 玩家自动喝药逻辑（加了个安全校验，确保药水还在背包里）
        if player.hp <= player.max_hp * 0.3 and red_potion in player.bag.items:#这个以前没加
            player.use_potion(red_potion)

        monster_g.attack(player)

        if not player.is_alive:
            print(f"💀 您已经阵亡，{player.name}!")
            break
        print("-" * 20)