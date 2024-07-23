from player import *
from fireball import Fireball
from big_fireball import BigFireball


class Mage(Player):

    def __init__(self, g, x, y, dir_touches, nb, dmg=5, cards=None):
        super().__init__(g, x, y, dir_touches, nb, "mage", 40, dmg=dmg, cards=cards)
        self.delay_attack = 40
        self.max_damage = 40
        self.time_since_last_capa = 0
        self.capabar = Bar(g, self.zp, 3, 150, "#7b1800", "#000000")

    def ud_add(self):
        self.time_since_last_capa += 1

    def attack(self):
        Fireball(self)
        self.nb_jumps = 2
        self.vy = 0

    def wide_capacity(self):
        if self.time_since_last_capa >= 150:
            BigFireball(self)
            self.nb_jumps = 4
            self.vy = 0
            self.time_since_last_capa = 0

    def ud_bars(self):
        self.lifebar.ud(self.life)
        self.damagebar.ud(self.damage)
        self.delaybar.ud(max(self.delay_attack - self.time_since_last_attack, 0))
        self.capabar.ud(max(150 - self.time_since_last_capa, 0))

    def change_wd_size(self):
        self.zp = Surface((self.g.W // 2, self.g.H))
        self.lifebar.blitting_surface = self.zp
        self.damagebar.blitting_surface = self.zp
        self.delaybar.blitting_surface = self.zp
        self.capabar.blitting_surface = self.zp
        for i, c in enumerate(self.cards):
            c.wtb = self.zp
            c.pos = (self.g.W // 4 + (i-1.5) * 32 * self.card_s - 12 * self.card_s, (self.g.H - 32 * self.card_s)//2)

# cree une tombe qui invoque un zombie
