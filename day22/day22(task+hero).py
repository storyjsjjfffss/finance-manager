class Hero:
    def __init__(self, name,hp,attack_power):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack_power=attack_power

    def is_alive(self):
        if self.hp > 0 and self.max_hp > 0:
            return True
        else:
            return False
    def take_damage(self, damage):
        self.hp = max(self.hp-damage, 0)
        print(f'{self.name} takes {damage} damage，剩余血量：{self.hp}')
    def attack(self,target_hero):
        print(f'{self.name} attacks {target_hero.name}')
        target_hero.take_damage(self.attack_power)
        if not target_hero.is_alive():
            print(f"{target_hero.name} is dead")


if __name__ == '__main__':
    hero_a = Hero('曹操',100,35)
    hero_b = Hero('盖伦',200,15)
    while True:
        hero_a.attack(hero_b)
        if not hero_b.is_alive():
            print(f"{hero_a.name} is win")
            break
        hero_b.attack(hero_a)
        if not hero_a.is_alive():
            print(f"{hero_b.name} is win")
            break