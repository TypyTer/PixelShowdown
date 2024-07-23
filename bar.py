from pygame import *


class Bar:

    def __init__(self, g, where_to_draw, number, max_qte, fg_color, over_color):
        self.blitting_surface = where_to_draw
        self.width, self.height = 102 * g.s, 13 * g.s
        self.x_img = 5 * g.s
        self.y_img = 5 * g.s + (2 + 15) * number * g.s
        self.x = self.x_img + (15 + 5) * g.s
        self.y = self.y_img + g.s
        self.inner_d = 2 * g.s
        self.max_qte = max_qte
        self.bg_color = "#222222"
        self.over_color = over_color
        self.fg_color = fg_color
        self.image = transform.scale(image.load(f"ress/img/icons/{number}.png"), (15*g.s, 15*g.s))

    def obt_big_rect(self):
        return Rect(self.x, self.y, self.width, self.height)

    def obt_little_rect(self, qte):
        return Rect(self.x + self.inner_d, self.y + self.inner_d, qte / self.max_qte * (self.width - 2 * self.inner_d), self.height - 2 * self.inner_d)

    def ud(self, qte):
        self.blitting_surface.blit(self.image, (self.x_img, self.y_img))
        draw.rect(self.blitting_surface, self.bg_color, self.obt_big_rect())
        draw.rect(self.blitting_surface, self.fg_color, self.obt_little_rect(min(self.max_qte, qte)))
        draw.rect(self.blitting_surface, self.over_color, self.obt_little_rect(max(0, qte-self.max_qte)))
