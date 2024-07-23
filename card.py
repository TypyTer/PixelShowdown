from pygame import *


class Card(sprite.Sprite):

    def __init__(self, owner, perso, pos, nb):
        super().__init__()
        self.owner = owner
        self.s = self.owner.card_s
        self.g = owner.g
        self.wtb = self.owner.zp
        self.pos = pos
        self.nb = nb
        self.role = perso
        self.images = [transform.scale(image.load(f"ress/img/card/{i}.png"), (24*self.s, 32*self.s)) for i in range(23)]
        self.perso = transform.scale(image.load(f"ress/img/{perso}/0.png"), (16*self.s, 16*self.s))
        for e in self.images:
            e.blit(self.perso, (4*self.s, 4*self.s))
        self.owner.cards.add(self)

    def obt_rect(self):
        return Rect(self.pos[0] + self.owner.nb*self.g.W//2, self.pos[1], 24*self.s, 32*self.s)

    def ud(self):
        self.wtb.blit(self.images[self.g.t // 2 % len(self.images)], self.pos)
        if self.owner.DOWN in self.g.just_keyd and self.nb == self.owner.selected:
            self.kill()
            for i in range(len(self.g.players)):
                if self.g.players.sprites()[i] is self.owner:
                    self.g.change_player_role(i, {str(a.__name__).lower(): a for a in self.g.roles}[self.role])
