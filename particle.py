from pygame import *
from random import randint


class Particle(sprite.Sprite):

    def __init__(self, g, x, y, c):
        super().__init__()
        self.g = g
        self.size = 2
        self.x, self.y = x + randint(-2*self.g.s, 2*self.g.s), y + randint(-2*self.g.s, 2*self.g.s)
        self.image = Surface((self.size*self.g.s, self.size*self.g.s), SRCALPHA)
        help = "0123456789abcdef"
        for dx in range(self.size):
            for dy in range(self.size):
                if randint(0, 1) == 0:
                    nc = ""
                    for carac in c:
                        if carac in help:
                            nc += help[(help.index(carac)+randint(-1, 1)) % 16]
                        else:
                            nc += carac
                    draw.rect(self.image, nc, Rect(dx * self.g.s, dy * self.g.s, self.g.s, self.g.s))
        self.lifetime = randint(15, 30)
        self.g.particles.add(self)
        self.randd = randint(0, 4)

    def ud(self):
        # if self.g.t % 5 == self.randd:
        #     self.x += (randint(0, 1) * 2 - 1) * self.g.s
        #     self.y += (randint(0, 1) * 2 - 1) * self.g.s
        self.lifetime -= 1
        self.g.show(self.image, (self.x, self.y))
        if self.lifetime == 0:
            self.kill()
