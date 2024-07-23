from pygame import *
from copy import deepcopy
from bar import Bar
from particle import Particle
from random import randint
from card import Card


class Player(sprite.Sprite):

    def __init__(self, g, x, y, dir_touches, nb, perso_type, delay, dmg=15, cards=None):
        super().__init__()
        self.g = g
        self.nb = nb
        self.perso_type = perso_type
        self.zp = Surface((self.g.W//2, self.g.H))
        self.image = transform.scale(image.load(f"ress/img/{self.perso_type}/0.png"), (self.g.ss, self.g.ss))
        self.opos = self.x, self.y = x, y
        self.cam_dx = x - self.g.W // 2
        self.cam_dy = y - self.g.H // 2
        self.KEY_SET = self.LEFT, self.RIGHT, self.UP, self.DOWN, self.ATTACK, self.CAPACITY = dir_touches
        self.v = 3 * self.g.s
        self.vy = 0
        self.jump_height = 7 * self.g.s
        self.nb_jumps = 2
        self.hidden = False
        self.direction = nb
        temp = {"standing": 0, "walking0": 0, "walking1": 1, "walking2": 2, "walking3": 3, "jumping": 3, "sneaking": 4, "attacking0": 5, "attacking1": 6, "attacking2": 7, "attacking3": 7, "attacking4": 8, "attacking5": 8, "attacking6": 7, "attacking7": 7, "attacking8": 6, "attacking9": 5}
        self.postures = [deepcopy(temp), deepcopy(temp)]
        for i, e in enumerate(self.postures):
            for k, val in e.items():
                self.postures[i][k] = transform.flip(transform.scale(image.load(f"ress/img/{self.perso_type}/{val}.png"), (self.g.ss, self.g.ss)), bool(i), False)
        self.g.players.add(self)
        self.g.touchables.add(self)
        self.attacking = False
        self.hit_time = 0
        self.max_life = self.life = 100
        self.damage = dmg
        self.delay_attack = self.time_since_last_attack = delay
        self.max_damage = 100
        self.capacity_coordinate = []
        self.max_capacities = 1
        self.riding_who = None
        self.lifebar = Bar(self.g, self.zp, 0, self.max_life, "#1ea28c", "#5acf8f")
        self.damagebar = Bar(self.g, self.zp, 1, self.max_life, "#dc3510", "#000000")
        self.delaybar = Bar(self.g, self.zp, 2, self.delay_attack, "#808080", "#000000")

        self.choosing = False
        self.card_s = 3
        if cards is None:
            self.cards = sprite.Group()
            for i, e in enumerate(['warrior', 'archer', 'mage', 'monk']):
                Card(self, e, (self.g.W // 4 + (i-1.5) * 32 * self.card_s - 12 * self.card_s, (self.g.H-32 * self.card_s)//2), i)
        else:
            self.cards = sprite.Group()
            for c in cards:
                Card(self, c[1], c[0], c[2])

        self.selected = 0
        if len(self.cards) > 0:
            while len([c for c in self.cards if self.selected == c.nb]) == 0:
                self.selected = (self.selected + 1) % 4

    def change_wd_size(self):
        self.zp = Surface((self.g.W // 2, self.g.H))
        self.lifebar.blitting_surface = self.zp
        self.damagebar.blitting_surface = self.zp
        self.delaybar.blitting_surface = self.zp
        for i, c in enumerate(self.cards):
            c.wtb = self.zp
            c.pos = (self.g.W // 4 + (i-1.5) * 32 * self.card_s - 12 * self.card_s, (self.g.H-32 * self.card_s)//2)

    def wide_capacity(self):
        try:
            if self.g.map[round(self.y / self.g.ss)][round(self.x / self.g.ss)][0] in [-1, 6, 7, 9] and self.g.map[round(self.y / self.g.ss) + 1][round(self.x / self.g.ss)][0] in self.g.solids:
                self.y -= self.g.ss
                if not self.in_ground():
                    self.y += self.g.ss
                    if len(self.capacity_coordinate) == self.max_capacities:
                        pop = self.capacity_coordinate.pop(0)
                        self.g.map[pop[1]][pop[0]] = [-1, 0]
                        self.g.clear_world_at_pos(pop[1], pop[0])
                    self.capacity()
                    self.capacity_coordinate.append([round(self.x / self.g.ss), round(self.y / self.g.ss)])
                    self.y -= self.g.ss
                    for p in self.g.players:
                        if p.in_ground():
                            p.y -= self.g.ss
                else:
                    self.y += self.g.ss
        except IndexError:
            pass

    def deal_damage(self, amount):
        self.riding_who = None
        self.life -= amount
        if self.life <= 0:
            self.life = 0
            dy = 0
            try:
                while self.g.map[round(self.y / self.g.ss) + dy + 1][round(self.x / self.g.ss)][0] not in self.g.solids and dy < 20:
                    dy += 1
                if self.g.map[round(self.y / self.g.ss) + dy][round(self.x / self.g.ss)][0] in [-1, 6, 7, 8, 9]:
                    self.g.map[round(self.y / self.g.ss) + dy][round(self.x / self.g.ss)] = [13, 0]
                    self.g.clear_world_at_pos(round(self.y / self.g.ss) + dy, round(self.x / self.g.ss))
            except IndexError:
                pass
            self.die()

    def set_posture(self, posture_name):
        self.image = self.postures[self.direction].get(posture_name)

    def obt_rect(self):
        return Rect(self.x, self.y, self.g.ss, self.g.ss)

    def ud(self):
        if not self.choosing:
            if self.riding_who is None:
                if not self.hidden:
                    dy = 0
                    dx = 0
                    if not self.g.touch(4, self.x, self.y):
                        if (not self.attacking) or (self.perso_type != "mage"):
                            self.vy += 0.7 * self.g.s
                            if self.UP in self.g.just_keyd and self.nb_jumps > 0 and not self.attacking:
                                self.vy = - self.jump_height
                                self.nb_jumps -= 1
                            if self.g.touch(2, self.x, self.y):
                                self.vy = - self.jump_height*2
                            dy += self.vy
                    else:
                        self.nb_jumps = 2
                        self.vy = 0
                        if self.g.keys.get(self.UP):
                            self.y -= self.v
                            if not self.g.touch(4, self.x, self.y):
                                self.y += self.v
                        if self.g.keys.get(self.DOWN):
                            self.y += self.v
                            if not self.g.touch(4, self.x, self.y):
                                self.y -= self.v
                    if not self.attacking:
                        if self.g.keys.get(self.LEFT):
                            dx -= self.v
                            self.direction = 1
                        if self.g.keys.get(self.RIGHT):
                            dx += self.v
                            self.direction = 0
                        if self.DOWN in self.g.just_keyd:
                            if self.obt_rect().colliderect(self.g.ship.obt_rect()) and not self.g.ship.go_back_home:
                                for p in self.g.players:
                                    p.riding_who = None
                                self.riding_who = self.g.ship
                            elif self.g.touch(3, self.x, self.y):
                                self.hidden = True
                                self.x = round(self.x / self.g.ss) * self.g.ss
                                self.y = round(self.y / self.g.ss) * self.g.ss
                            elif self.g.touch(5, self.x, self.y):
                                self.teleport_stump()
                            elif self.g.touch(10, self.x, self.y) and self.damage < self.max_damage:
                                self.damage = min(self.max_damage, self.damage + 5 + 5 * self.g.map[round(self.y / self.g.ss)][round(self.x / self.g.ss)][1])
                                self.g.map[round(self.y/self.g.ss)][round(self.x/self.g.ss)] = [-1, 0]
                                self.g.clear_world_at_pos(round(self.y/self.g.ss), round(self.x/self.g.ss))

                    if self.g.keys.get(self.ATTACK) and self.time_since_last_attack >= self.delay_attack:
                        self.time_since_last_attack = 0
                        self.attacking = True

                    if self.CAPACITY in self.g.just_keyd:
                        self.wide_capacity()

                    if not self.hidden:
                        was_on_ladder = self.g.touch(4, self.x, self.y)
                        if round(dx//self.g.s) != 0:
                            signe = int(round(dx//self.g.s)//abs(round(dx//self.g.s)))
                            for i in range(abs(round(dx//self.g.s))):
                                self.x += self.g.s * signe
                                if self.in_ground() and ((not was_on_ladder) or (was_on_ladder and not self.g.touch(4, self.x, self.y))):
                                    self.x -= self.g.s * signe
                                    break

                        if round(dy // self.g.s) != 0:
                            signe = int(round(dy // self.g.s) // abs(round(dy // self.g.s)))
                            for i in range(abs(round(dy // self.g.s))):
                                self.y += self.g.s * signe
                                if self.in_ground():
                                    self.y -= self.g.s * signe
                                    if self.vy > 0:
                                        self.nb_jumps = 2
                                    self.vy = 0
                                    break
                        self.get_posture()
                        self.g.show(self.image, (self.x, self.y))

                    if self.y >= 800 * self.g.s:
                        self.die()
                else:
                    if self.DOWN in self.g.just_keyd:
                        self.hidden = False
                    if self.g.map[self.get_block()[1]][self.get_block()[0]][1] in [0, 1, 2, 3]:
                        self.life = min(self.max_life, self.life + 0.1 * self.g.map[self.get_block()[1]][self.get_block()[0]][1])
                    elif self.g.map[self.get_block()[1]][self.get_block()[0]][1] == 4:
                        self.life = min(self.max_life * 1.5, self.life + 0.1)
                    else:
                        self.deal_damage(0.1 * self.g.map[self.get_block()[1]][self.get_block()[0]][1])
                        for p in self.g.players:
                            if p is not self:
                                p.life = min(p.max_life, p.life + 0.1 * self.g.map[self.get_block()[1]][self.get_block()[0]][1])

                if self.attacking:
                    self.hit_time += 1
                    if self.hit_time == 6 * 1:
                        self.attack()
                    if self.hit_time == 1 * 10 - 1:
                        self.hit_time = 0
                        self.attacking = False

            else:
                if self.g.keys.get(self.RIGHT) and self.g.keys.get(self.DOWN) and self.g.keys.get(self.LEFT):
                    self.riding_who = None
                lx, ly = self.g.ship.x, self.g.ship.y
                if not self.g.ship.go_back_home:
                    if self.g.keys.get(self.RIGHT):
                        self.g.ship.x += self.g.ship.v * (1 + int(self.g.keys.get(self.ATTACK, False) and self.damage >= 0.05))
                        self.direction = 0
                        if self.g.ship.in_ground():
                            self.g.ship.x -= self.g.ship.v * (1 + int(self.g.keys.get(self.ATTACK, False) and self.damage >= 0.05))
                    if self.g.keys.get(self.LEFT):
                        self.g.ship.x -= self.g.ship.v * (1 + int(self.g.keys.get(self.ATTACK, False) and self.damage >= 0.05))
                        self.direction = 1
                        if self.g.ship.in_ground():
                            self.g.ship.x += self.g.ship.v * (1 + int(self.g.keys.get(self.ATTACK, False) and self.damage >= 0.05))
                    if self.g.keys.get(self.UP):
                        self.g.ship.y -= self.g.ship.v * (1 + int(self.g.keys.get(self.ATTACK, False) and self.damage >= 0.05))
                        if self.g.ship.in_ground():
                            while self.g.ship.in_ground():
                                self.g.ship.y += self.g.s
                    if self.g.keys.get(self.DOWN):
                        self.g.ship.y += self.g.ship.v * (1 + int(self.g.keys.get(self.ATTACK, False) and self.damage >= 0.05))
                        if self.g.ship.in_ground():
                            if self.g.ship.in_ground():
                                while self.g.ship.in_ground():
                                    self.g.ship.y -= self.g.s
                self.vy = 0
                self.x = self.g.ship.x + 2 * self.g.s
                self.y = self.g.ship.y + 2 * self.g.s
                self.get_posture()
                self.g.show(self.image, (self.x, self.y))
                if self.g.keys.get(self.ATTACK, False) and self.damage >= 0.05 and (ly != self.g.ship.y or lx != self.g.ship.x):
                    self.damage -= 0.05

            self.time_since_last_attack += 1
            self.ud_add()

        else:
            if self.RIGHT in self.g.just_keyd:
                self.selected = (self.selected + 1) % 4
                while len([c for c in self.cards if self.selected == c.nb]) == 0:
                    self.selected = (self.selected + 1) % 4
            if self.LEFT in self.g.just_keyd:
                self.selected = (self.selected - 1) % 4
                while len([c for c in self.cards if self.selected == c.nb]) == 0:
                    self.selected = (self.selected - 1) % 4
            draw.rect(self.zp, "#1c3055", Rect(self.g.W // 4 + (self.selected-1.5) * 32 * self.card_s - 12 * self.card_s - 2 * self.g.s, (self.g.H-32 * self.card_s)//2 - 2 * self.g.s, 24 * self.card_s + 4 * self.g.s, 32 * self.card_s + 4 * self.g.s))
            for c in self.cards:
                c.ud()

    def ud_cam_d(self):
        self.cam_dx += (self.x - self.cam_dx - self.g.W / 2) / 10
        self.cam_dy += (self.y - self.cam_dy - self.g.H / 2) / 10

    def ud_add(self):
        pass

    def die(self):
        if len(self.cards) == 0:
            self.g.menu = True
        y = len(self.g.map) - 1
        while self.g.map[y][0][0] not in self.g.solids:
            y -= 1
        while self.g.map[y][0][0] in self.g.solids:
            y -= 1
        for e in self.capacity_coordinate:
            self.g.map[e[1]][e[0]] = [-1, 0]
            self.g.clear_world_at_pos(e[1], e[0])
        self.choosing = True
        self.g.touchables.remove(self)

    def get_block(self):
        return int(self.x // self.g.ss), int(self.y // self.g.ss)

    def get_posture(self):
        if self.riding_who is not None:
            self.set_posture(f"standing")
        elif self.attacking:
            self.set_posture(f"attacking{self.hit_time//1}")
        else:
            self.y += self.g.s
            if not (self.in_ground() or self.g.touch(4, self.x, self.y)):
                self.set_posture("jumping")
            elif (not self.g.touch(4, self.x, self.y)) and (self.g.keys.get(self.RIGHT) or self.g.keys.get(self.LEFT)):
                self.set_posture(f"walking{self.g.t//3%4}")
            elif self.g.keys.get(self.DOWN):
                self.set_posture("sneaking")
            else:
                self.set_posture("standing")
            self.y -= self.g.s

    def in_ground(self):
        x, y = self.get_block()[0] * self.g.ss, self.get_block()[1] * self.g.ss
        for dx in range(2):
            for dy in range(2):
                try:
                    assert y//self.g.ss+dy >= 0 and x//self.g.ss+dx >= 0
                    if self.g.map[y//self.g.ss+dy][x//self.g.ss+dx][0] in self.g.solids:
                        if Rect(self.x, self.y, self.g.ss, self.g.ss).colliderect(Rect(x+self.g.ss*dx, y+self.g.ss*dy+1, self.g.ss, self.g.ss)):
                            return True
                except:
                    pass
        return False

    def teleport_stump(self):
        x, y = int((self.x + self.g.ss / 2) / self.g.ss) * self.g.ss, int((self.y + self.g.ss / 2) / self.g.ss) * self.g.ss
        for e in self.g.stump_coordinates:
            for i, f in enumerate(e):
                if f == [x, y]:
                    self.x, self.y = e[i-1][0], e[i-1][1]

    def attack(self):
        for p in self.g.players:
            if p is not self:
                if self.obt_rect().colliderect(p.obt_rect()):
                    if (self.x <= p.x and self.direction == 0) or (self.x >= p.x and self.direction == 1):
                        p.deal_damage(self.damage)

    def capacity(self):
        pass

    def ud_bars(self):
        if not self.choosing:
            self.lifebar.ud(self.life)
            self.damagebar.ud(self.damage)
            self.delaybar.ud(max(self.delay_attack - self.time_since_last_attack, 0))
