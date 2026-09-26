class Hero:
    def __init__(self, name, hp, attack_power):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack_power = attack_power

    def is_alive(self):
        """生命值大于 0 即为存活"""
        return self.hp > 0

    def take_damage(self, damage):
        """单次扣减伤害，最低扣到 0"""
        self.hp = max(0, self.hp - damage)
        print(f"[{self.name}] 受到 {damage} 点伤害，剩余血量: {self.hp}/{self.max_hp}")

    def attack(self, target_hero):
        """攻击目标英雄对象"""
        print(f"\n⚔️ [{self.name}] 发起攻击 -> [{target_hero.name}]")
        target_hero.take_damage(self.attack_power)
        if not target_hero.is_alive():
            print(f"💀 [{target_hero.name}] 已阵亡！")


if __name__ == '__main__':
    hero_a = Hero('曹操', 100, 35)
    hero_b = Hero('盖伦', 200, 15)

    print("=== 对决开始 ===")
    while True:
        hero_a.attack(hero_b)
        if not hero_b.is_alive():
            print(f"\n🏆 胜者诞生: [{hero_a.name}] 赢得了对决！")
            break

        hero_b.attack(hero_a)
        if not hero_a.is_alive():
            print(f"\n🏆 胜者诞生: [{hero_b.name}] 赢得了对决！")
            break