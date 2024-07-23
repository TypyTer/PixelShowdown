from player import *
from ghost import Ghost


class Monk(Player):

    def __init__(self, g, x, y, dir_touches, nb, dmg=5, cards=None):
        super().__init__(g, x, y, dir_touches, nb, "monk", 9, dmg=dmg, cards=cards)
        self.max_damage = 45

    def attack(self):
        for p in self.g.touchables:
            if p is not self:
                if self.obt_rect().colliderect(p.obt_rect()):
                    if (self.x <= p.x and self.direction == 0) or (self.x >= p.x and self.direction == 1):
                        p.deal_damage(self.damage)

    def wide_capacity(self):
        if self.g.touch(13, self.x, self.y):
            self.g.map[round(self.y / self.g.ss)][round(self.x / self.g.ss)] = [-1, 0]
            self.g.clear_world_at_pos(round(self.y / self.g.ss), round(self.x / self.g.ss))
            Ghost(self.g, self.x, self.y, [i for i, p in enumerate(self.g.players) if p is not self][0], 0)
            Ghost(self.g, self.x, self.y, [i for i, p in enumerate(self.g.players) if p is not self][0], 1)

