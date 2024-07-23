from pygame import *
from copy import deepcopy


class Board:

    def __init__(self, g):
        self.g = g
        self.s = 2
        self.width, self.height = (len(self.g.map[0]) + 4)*self.s, (len(self.g.map) + 4)*self.s
        self.image = Surface((self.width, self.height))
        self.image.fill("#323232")
        self.pos = self.g.W // 2 - self.width // 2, self.g.H - self.height - 16
        draw.rect(self.image, "#c8c8c8", (self.s, self.s, self.width - 2 * self.s, self.height - 2 * self.s))
        for i, e in enumerate(self.g.map):
            for j, f in enumerate(e):
                if f[0] in self.g.solids or f == [4, 1]:
                    draw.rect(self.image, "#2f2d4a", Rect(self.s * (2 + j), self.s * (2 + i), self.s, self.s))
                else:
                    draw.rect(self.image, self.g.sky_color, Rect(self.s * (2 + j), self.s * (2 + i), self.s, self.s))

    def change_wd_size(self):
        self.pos = self.g.W // 2 - self.width // 2, self.g.H - self.height - 16

    def ud(self):
        ns = self.image.copy()
        for p in self.g.players:
            if p.riding_who is None:
                draw.rect(ns, "#dc7070", Rect(self.s * ((p.x + self.g.ss // 2) // self.g.ss + 2), self.s * ((p.y + self.g.ss // 2) // self.g.ss + 2), self.s, self.s))
        draw.rect(ns, "#907caf", Rect(self.s * ((self.g.ship.x + self.g.s * 10) // self.g.ss + 2), self.s * ((self.g.ship.y + self.g.s * 10) // self.g.ss + 2), self.s, self.s))
        self.g.show(ns, self.pos, dcam=False)
