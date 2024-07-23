from pygame import *


class Ghost(sprite.Sprite):

    def __init__(self, g, x, y, target, tpe):
        super().__init__()
        self.g = g
        self.x, self.y = x, y
        self.nb_target = target
        self.target = self.g.players.sprites()[self.nb_target]
        self.type = tpe
        self.v = self.g.s + self.g.s * tpe
        self.g.ghosts.add(self)
        self.g.touchables.add(self)
        self.images = [transform.scale(image.load(f"ress/img/ghost/0.png"), (self.g.ss, self.g.ss)).convert_alpha(), transform.flip(transform.scale(image.load(f"ress/img/ghost/0.png"), (self.g.ss, self.g.ss)), True, False).convert_alpha()]
        for e in self.images:
            e.set_alpha(128)
        self.direction = 0
        self.life = 10
        self.damage = 0.5 + 0.5 * (-(tpe-1))
    def obt_rect(self):
        return Rect(self.x, self.y, self.g.ss, self.g.ss)

    def ud(self):
        self.target = self.g.players.sprites()[self.nb_target]
        if self.target.x // self.g.ss < self.x // self.g.ss:
            self.x -= self.v
            self.direction = 1
        elif self.target.x // self.g.ss > self.x // self.g.ss:
            self.x += self.v
            self.direction = 0
        else:
            if self.target.y // self.g.ss < self.y // self.g.ss:
                self.y -= self.v
            elif self.target.y // self.g.ss > self.y // self.g.ss:
                self.y += self.v

        if self.target.obt_rect().colliderect(self.obt_rect()):
            self.target.deal_damage(self.damage)

        self.g.show(self.images[self.direction], (self.x, self.y))

    def deal_damage(self, amount):
        self.life -= amount
        if self.life <= 0:
            self.life = 0
            self.kill()






