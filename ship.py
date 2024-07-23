from pygame import *


class Ship(sprite.Sprite):

    def __init__(self, g, x, y):
        super().__init__()
        self.g = g
        self.x, self.y = x, y
        self.v = 4 * self.g.s
        self.image = transform.scale(image.load(f"ress/img/ship/0.png"), (20*self.g.s, 20*self.g.s))
        self.go_back_home = False

    def obt_rect(self):
        return Rect(self.x, self.y, self.g.s * 20, self.g.s * 20)

    def get_block(self):
        return int(self.x // self.g.ss), int(self.y // self.g.ss)

    def ud(self):
        if not self.go_back_home:
            if len([p for p in self.g.players if p.riding_who is not None]) == 0:
                self.y += self.g.ss
                self.y += self.g.s
                if self.in_ground():
                    self.y -= self.g.s
                self.y -= self.g.ss
            if self.y > (len(self.g.map) + 4) * self.g.ss or (self.y < 12 * self.g.ss and not self.g.map_length * self.g.ss // 2 - self.g.ss < self.x < self.g.map_length * self.g.ss // 2 + self.g.ss):
                if len([e for e in self.g.players if e.riding_who is not None]) == 0:
                    self.go_back_home = True
        else:
            if self.y > 8 * self.g.ss:
                if - 4 * self.g.ss < self.x < (self.g.map_length + 4) * self.g.ss:
                    if self.x < self.g.map_length * self.g.ss // 2:
                        self.x -= self.v
                    else:
                        self.x += self.v
                else:
                    self.y -= self.v
            elif not self.g.map_length * self.g.ss // 2 - self.g.ss < self.x < self.g.map_length * self.g.ss // 2 + self.g.ss:
                if self.x < self.g.map_length * self.g.ss // 2:
                    self.x += self.v
                else:
                    self.x -= self.v
            else:
                self.go_back_home = False
        self.g.show(self.image, (self.x, self.y))

    def in_ground(self):
        x, y = self.get_block()[0] * self.g.ss, self.get_block()[1] * self.g.ss
        for dx in range(3):
            for dy in range(3):
                try:
                    assert y // self.g.ss + dy >= 0 and x // self.g.ss + dx >= 0
                    if self.g.map[y // self.g.ss + dy][x // self.g.ss + dx][0] in self.g.solids:
                        if self.obt_rect().colliderect(Rect(x + self.g.ss * dx, y + self.g.ss * dy + 1, self.g.ss, self.g.ss)):
                            return True
                except:
                    pass
        return False





