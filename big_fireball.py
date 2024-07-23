from pygame import *


class BigFireball(sprite.Sprite):

    def __init__(self, owner):
        super().__init__()
        self.g = owner.g
        self.image = transform.flip(transform.scale(image.load(f"ress/img/big_fireball/0.png"), (7*self.g.s, 7*self.g.s)), bool(owner.direction), False)
        self.x, self.y = owner.x, owner.y+self.g.ss//4
        self.owner = owner
        self.direction = owner.direction
        self.v = 10 * self.g.s
        self.lifetime = 120
        self.g.projectiles.add(self)
        self.damage = 35

    def ud(self):
        self.x -= (self.direction*2 - 1) * self.v
        for p in self.g.touchables:
            if p is not self.owner:
                if Rect(self.x, self.y, 9*self.g.s, 3*self.g.s).colliderect(p.obt_rect()):
                    self.kill()
                    p.deal_damage(self.damage)
                    if self.owner is not None:
                        self.owner.life = min(self.owner.max_life * 1.5, self.owner.life + self.damage)
        if self.in_ground() == 1:
            self.x += (self.direction * 2 - 1) * self.v * 0.5
        if self.in_ground() == 2:
            self.direction = int(not bool(self.direction))
            self.image = transform.flip(transform.scale(image.load(f"ress/img/big_fireball/0.png"), (7 * self.g.s, 7 * self.g.s)), bool(self.direction), False)
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
                        if Rect(self.x, self.y, 7*self.g.s, 7*self.g.s).colliderect(Rect(x+self.g.ss*dx, y+self.g.ss*dy+1, self.g.ss, self.g.ss)):
                            return 1 + int(self.g.map[y//self.g.ss+dy][x//self.g.ss+dx][0] == 12)
                except:
                    pass
        return 0
