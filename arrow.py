from pygame import *


class Arrow(sprite.Sprite):

    def __init__(self, owner, data=None):
        super().__init__()
        self.g = owner.g
        self.owner = owner
        if data is None:
            self.x, self.y = owner.x, owner.y+self.g.ss//2
            self.direction = owner.direction
        else:
            self.x, self.y, self.direction = data
        self.image = transform.flip(transform.scale(image.load(f"ress/img/arrow/0.png"), (9*self.g.s, 3*self.g.s)), bool(self.direction), False)
        self.v = 10 * self.g.s
        self.lifetime = 60
        self.g.projectiles.add(self)
        self.damage = owner.damage

    def ud(self):
        if self.in_ground() == 0:
            self.x -= (self.direction*2 - 1) * self.v
            for p in self.g.touchables:
                if p is not self.owner:
                    if Rect(self.x, self.y, 9*self.g.s, 3*self.g.s).colliderect(p.obt_rect()):
                        self.kill()
                        p.deal_damage(self.damage)
        elif self.in_ground() == 2:
            self.direction = int(not bool(self.direction))
            self.image = transform.flip(transform.scale(image.load(f"ress/img/arrow/0.png"), (9 * self.g.s, 3 * self.g.s)), bool(self.direction), False)
            self.x -= (self.direction * 2 - 1) * self.v
            self.owner = None
        self.g.show(self.image, (self.x, self.y))
        self.lifetime -= 1
        if self.lifetime == 0:
            self.kill()

    def get_block(self):
        return int(self.x // self.g.ss), int(self.y // self.g.ss)

    def in_ground(self):
        x, y = self.get_block()[0] * self.g.ss, self.get_block()[1] * self.g.ss
        for dx in range(2):
            for dy in range(2):
                try:
                    assert y//self.g.ss+dy >= 0 and x//self.g.ss+dx >= 0
                    if self.g.map[y//self.g.ss+dy][x//self.g.ss+dx][0] in self.g.solids:
                        if Rect(self.x, self.y, 9*self.g.s, 3*self.g.s).colliderect(Rect(x+self.g.ss*dx, y+self.g.ss*dy + 1, self.g.ss, self.g.ss)):
                            return 1 + int(self.g.map[y//self.g.ss+dy][x//self.g.ss+dx][0] == 12)
                except:
                    pass
        return 0
