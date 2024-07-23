from player import *


class Warrior(Player):

    def __init__(self, g, x, y, dir_touches, nb, dmg=15, cards=None):
        super().__init__(g, x, y, dir_touches, nb, "warrior", 9, dmg=dmg, cards=cards)
        self.max_damage = 50
        self.max_capacities = 5

    def attack(self):
        for p in self.g.touchables:
            if p is not self:
                if self.obt_rect().colliderect(p.obt_rect()):
                    if (self.x <= p.x and self.direction == 0) or (self.x >= p.x and self.direction == 1):
                        p.deal_damage(self.damage)

    def capacity(self):
        self.g.map[round(self.y / self.g.ss)][round(self.x / self.g.ss)] = [12, 0]
        self.g.clear_world_at_pos(round(self.y / self.g.ss), round(self.x / self.g.ss))

# cree une barricade qui renvoie les projectiles
