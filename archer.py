from player import *
from arrow import Arrow


class Archer(Player):

    def __init__(self, g, x, y, dir_touches, nb, dmg=5, cards=None):
        super().__init__(g, x, y, dir_touches, nb, "archer", 60, dmg=dmg, cards=cards)
        self.max_damage = 30
        self.max_capacities = 1

    def attack(self):
        Arrow(self)
        for a in self.capacity_coordinate:
            Arrow(self, data=(a[0]*self.g.ss + self.g.ss//2, a[1]*self.g.ss+self.g.ss//2, 0))
            Arrow(self, data=(a[0]*self.g.ss - self.g.ss//2, a[1]*self.g.ss+self.g.ss//2, 1))

    def capacity(self):
        self.g.map[round(self.y / self.g.ss)][round(self.x / self.g.ss)] = [11, 0]
        self.g.clear_world_at_pos(round(self.y / self.g.ss), round(self.x / self.g.ss))

# crée un bloc depuis lequel il peut tirer ses fleches
