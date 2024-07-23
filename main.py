from pygame import *
from sys import exit
from random import randint, shuffle
from os import listdir
from warrior import Warrior
from archer import Archer
from mage import Mage
from monk import Monk
from particle import Particle
from ship import Ship
from board import Board


class Game:

    def __init__(self):
        self.W, self.H = 1000, 600
        self.root = display.set_mode((self.W, self.H), RESIZABLE)
        display.set_caption("Pixel Showdown")
        self.s = 2
        self.ss = 16 * self.s
        self.map_length = 100
        self.keys = {}
        self.just_keyd = []
        self.clock = time.Clock()
        self.t = 0
        self.projectiles = sprite.Group()
        self.particles = sprite.Group()

        self.stump_coordinates = []

        self.sky_color = "#000008"
        self.stuff = ['grass', 'dirt', 'mushroom', 'bush', 'ladder', 'stump', 'lawn', 'flower', 'root', 'rock', 'upgrading_rock', 'arrow_launcher', 'box', 'grave', 'stone']
        self.nb_to_img = {i: [transform.scale(image.load("ress/img/" + self.stuff[i] + f"/{j}.png"), (self.ss, self.ss)) for j in range(len(listdir("ress/img/" + self.stuff[i])))] for i in range(len(self.stuff))}
        self.solids = [0, 1, 12, 14]
        self.stars = Surface((self.map_length*self.ss, 50 * self.ss))
        self.stars.fill(self.sky_color)
        for i in range(400):
            draw.rect(self.stars, (255, randint(128, 255), 128), (randint(0, self.map_length*self.ss-1), randint(0, 50 * self.ss-1), self.s, self.s))
        self.map = []
        self.set_map()
        self.world = Surface((len(self.map[0])*self.ss, len(self.map)*self.ss))
        self.set_world()

        self.players = sprite.Group()
        self.ghosts = sprite.Group()
        self.touchables = sprite.Group()
        self.roles = [Warrior, Archer, Mage, Monk]

        y1 = len(self.map) - 1
        while self.map[y1][0][0] not in self.solids:
            y1 -= 1
        while self.map[y1][0][0] in self.solids:
            y1 -= 1

        y2 = len(self.map) - 1
        while self.map[y2][self.map_length-1][0] not in self.solids:
            y2 -= 1
        while self.map[y2][self.map_length-1][0] in self.solids:
            y2 -= 1

        self.player_poss = [[0, y1*self.ss], [self.ss * (self.map_length-1), y2*self.ss]]

        Warrior(self, self.player_poss[0][0], self.player_poss[0][1], [K_q, K_d, K_z, K_s, K_a, K_e], 0)
        Warrior(self, self.player_poss[1][0], self.player_poss[1][1], [K_KP4, K_KP6, K_KP8, K_KP5, K_KP7, K_KP9], 1)

        for p in self.players:
            p.choosing = True

        self.ship = Ship(self, self.map_length * self.ss / 2, -self.ss)
        self.board = Board(self)

        self.menu = True
        self.menu_image = transform.scale(image.load("ress/img/background_menu/0.png"), (self.W, self.W*0.6))
        self.menu_image_pos = (0, (self.H-self.menu_image.get_height())//2)
        self.play_button_size = 128
        self.play_button_pos = ((self.W - self.play_button_size)//2, (self.H - self.play_button_size)//2)
        self.play_button_images = [transform.scale(image.load(f"ress/img/play_button/{i}.png"), (self.play_button_size, self.play_button_size)) for i in range(2)]

    def change_player_role(self, nb, role):
        who = self.players.sprites()[nb]
        data = []
        for c in who.cards:
            data.append([c.pos, c.role, c.nb])
        self.players.sprites()[nb] = role(self, who.opos[0], who.opos[1], who.KEY_SET, who.nb, dmg=who.damage, cards=data)
        self.players.sprites()[nb].zp = who.zp
        who.kill()

    def ud(self):
        self.just_keyd = []
        for e in event.get():
            if e.type == QUIT:
                quit()
                exit()
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    quit()
                    exit()
                self.keys[e.key] = True
                self.just_keyd.append(e.key)
            if e.type == KEYUP:
                self.keys[e.key] = False
            if e.type == WINDOWRESIZED:
                self.W, self.H = display.get_window_size()
                self.menu_image = transform.scale(image.load("ress/img/background_menu/0.png"), (self.W, self.W * 0.6))
                self.play_button_pos = ((self.W - self.play_button_size)//2, (self.H - self.play_button_size)//2)
                self.root = display.set_mode((self.W, self.H), RESIZABLE)
                Surface((self.map_length*self.ss, 50 * self.ss))
                self.stars.fill(self.sky_color)
                for i in range(400):
                    draw.rect(self.stars, (255, randint(128, 255), 128), (randint(0, self.map_length*self.ss - 1), randint(0, 50 * self.ss - 1), self.s, self.s))
                for p in self.players:
                    p.change_wd_size()
                self.board.change_wd_size()

        if self.menu:
            self.root.fill(self.sky_color)
            self.root.blit(self.menu_image, self.menu_image_pos)
            if Rect(self.play_button_pos[0], self.play_button_pos[1], self.play_button_size, self.play_button_size).collidepoint(mouse.get_pos()[0], mouse.get_pos()[1]):
                self.root.blit(self.play_button_images[1], self.play_button_pos)
                if mouse.get_pressed(3)[0]:
                    self.menu = False
                    self.reinit()
            else:
                self.root.blit(self.play_button_images[0], self.play_button_pos)

        else:
            for p in self.players:
                p.zp.fill(self.sky_color)

            self.show(self.world, (0, 0))

            for g in self.ghosts:
                g.ud()

            for p in self.players:
                p.ud()

            self.ship.ud()

            for p in self.projectiles:
                p.ud()

            for p in self.particles:
                p.ud()

            for p in self.players:
                p.ud_bars()

            self.board.ud()

            for p in self.players:
                self.root.blit(p.zp, (self.W//2*p.nb, 0))
            draw.line(self.root, "#aaaaaa", (self.W//2, 0), (self.W//2, self.H), self.s)

            for p in self.players:
                p.ud_cam_d()

            self.t += 1

        display.flip()
        self.clock.tick(30)

    def reinit(self):
        self.t = 0
        self.projectiles = sprite.Group()
        self.particles = sprite.Group()

        self.stump_coordinates = []
        self.stars = Surface((self.map_length*self.ss, 50 * self.ss))
        self.stars.fill(self.sky_color)
        for i in range(400):
            draw.rect(self.stars, (255, randint(128, 255), 128), (randint(0, self.map_length*self.ss-1), randint(0, 50 * self.ss-1), self.s, self.s))
        self.map = []
        self.set_map()
        self.world = Surface((len(self.map[0])*self.ss, len(self.map)*self.ss))
        self.set_world()

        self.players = sprite.Group()
        self.ghosts = sprite.Group()
        self.touchables = sprite.Group()

        y1 = len(self.map) - 1
        while self.map[y1][0][0] not in self.solids:
            y1 -= 1
        while self.map[y1][0][0] in self.solids:
            y1 -= 1

        y2 = len(self.map) - 1
        while self.map[y2][self.map_length-1][0] not in self.solids:
            y2 -= 1
        while self.map[y2][self.map_length-1][0] in self.solids:
            y2 -= 1

        self.player_poss = [[0, y1*self.ss], [self.ss * (self.map_length-1), y2*self.ss]]

        Warrior(self, self.player_poss[0][0], self.player_poss[0][1], [K_q, K_d, K_z, K_s, K_a, K_e], 0)
        Warrior(self, self.player_poss[1][0], self.player_poss[1][1], [K_KP4, K_KP6, K_KP8, K_KP5, K_KP7, K_KP9], 1)

        for p in self.players:
            p.choosing = True

        self.ship = Ship(self, self.map_length * self.ss / 2, -self.ss)
        self.board = Board(self)


    def run(self):
        while True:
            self.ud()

    def show(self, what, where, dcam=True):
        if dcam:
            for p in self.players:
                if not p.choosing:
                    p.zp.blit(what, (where[0]-p.cam_dx - self.W // 4, where[1]-p.cam_dy))
        else:
            for p in self.players:
                if not p.choosing:
                    p.zp.blit(what, (where[0] - self.W // 4, where[1]))

    def clear_world_at_pos(self, i, j):
        self.world.blit(self.stars, (j*self.ss, i*self.ss), area=Rect(j*self.ss, i*self.ss, self.ss, self.ss))
        if self.nb_to_img.get(self.map[i][j][0]):
            self.world.blit(self.nb_to_img[self.map[i][j][0]][self.map[i][j][1]], (j * self.ss, i * self.ss))

    def set_world(self):
        self.world.blit(self.stars, (0, 0))
        for y, e in enumerate(self.map):
            for x, f in enumerate(e):
                if self.nb_to_img.get(f[0]):
                    self.world.blit(self.nb_to_img[f[0]][f[1]], (x*self.ss, y*self.ss))
                if f[0] == 5:
                    self.stump_coordinates.append([x*self.ss, y*self.ss])
        if len(self.stump_coordinates) % 2 == 1:
            self.stump_coordinates.append(self.stump_coordinates[-1])
        transition = []
        shuffle(self.stump_coordinates)
        for i in range(len(self.stump_coordinates)//2):
            transition.append([self.stump_coordinates[2*i], self.stump_coordinates[2*i+1]])
        self.stump_coordinates = transition

    def touch(self, nb, x, y):
        y = y + self.ss // 2
        x = x + self.ss // 2
        if not (0 <= int(y // self.ss) < len(self.map)) or not (0 <= int(x // self.ss) < len(self.map[0])):
            return False
        return self.map[int(y // self.ss)][int(x // self.ss)][0] == nb

    def create_particle(self, amount, x, y, c):
        for i in range(amount):
            Particle(self, x, y, c)

    def set_map(self):
        h = 50
        self.map = [[[-1, 0] for _ in range(self.map_length)] for _ in range(h)]
        y = 40
        for i in range(self.map_length):
            self.map[y][i] = [0, 0]
            for j in range(1, h-y):
                self.map[y+j][i] = [1, randint(0, 3)]
            if randint(1, 2) == 1:
                self.map[y-1][i] = [6, randint(0, 2)]
            if randint(1, 4) == 1:
                self.map[y-1][i] = [7, randint(0, 3)]
            if randint(1, 8) == 1:
                self.map[y - 1][i] = [9, randint(0, 3)]
            if randint(1, 10) == 1:
                self.map[y-1][i] = [2, randint(0, 2)]
            if randint(1, 15) == 1:
                self.map[y-1][i] = [5, 0]
            if randint(1, 15) == 1:
                self.map[y - 1][i] = [10, 0]
            if randint(1, 20) == 1:
                self.map[y-1][i] = [3, max(0, randint(-3, 3))]
            if randint(1, 5) == 1:
                y = min(max(5, y+randint(0, 1)*2 - 1), h-5)
        for i in range(self.map_length):
            if randint(1, 3) == 1:
                tl = randint(3, 7)
                th = randint(3, 4)
                if i + tl < self.map_length:
                    select = [[self.map[k][j][0] for k in range(len(self.map))] for j in range(i, i+tl+1)]
                    max_h = min([t.index(0) for t in select])
                    if max_h - 1 - th >= 20:
                        for j in range(tl):
                            self.map[max_h - th][i + j] = [0, 0]
                            if randint(1, 2) == 1:
                                self.map[max_h - th - 1][i + j] = [6, randint(0, 2)]
                                if randint(1, 4) == 1:
                                    self.map[max_h - th + 1][i + j] = [8, 0]
                            if randint(1, 4) == 1:
                                self.map[max_h - th - 1][i + j] = [7, randint(0, 3)]
                                if randint(1, 2) == 1:
                                    self.map[max_h - th + 1][i + j] = [8, 0]
                            if randint(1, 8) == 1:
                                self.map[max_h - th - 1][i + j] = [9, randint(0, 3)]
                            if randint(1, 10) == 1:
                                self.map[max_h - th - 1][i + j] = [2, randint(0, 2)]
                            if randint(1, 15) == 1:
                                self.map[max_h - th - 1][i + j] = [5, 0]
                                if randint(1, 2) == 1:
                                    self.map[max_h - th + 1][i + j] = [8, 1]
                            if randint(1, 15) == 1:
                                self.map[max_h - th - 1][i + j] = [10, 0]
                            if randint(1, 20) == 1:
                                self.map[max_h - th - 1][i + j] = [3, max(0, randint(-3, 3))]
                        for _ in range(max(1, randint(-1, 2))):
                            pos_ladder = randint(i+1, i + tl - 2)
                            self.map[max_h - th][pos_ladder] = [4, 1]
                            self.map[max_h - th - 1][pos_ladder] = [4, 0]
                            c = 1
                            while self.map[max_h - th + c][pos_ladder][0] != 0 and self.map[max_h - th + c][pos_ladder] != [4, 1]:
                                self.map[max_h - th + c][pos_ladder] = [4, 0]
                                c += 1

        y = 10
        for i in range(self.map_length):
            if i in [0, self.map_length - 1] + [int(self.map_length//2) + k for k in [-3, 3]]:
                for j in range(0, 6):
                    self.map[y + j][i] = [14, 0]
            if i not in [0, self.map_length - 1] + [int(self.map_length//2) + k for k in [-3, -2, -1, 0, 1, 2, 3]]:
                self.map[y][i] = [0, 0]
                for j in range(1, 5):
                    self.map[y + j][i] = [1, randint(0, 3)]
                self.map[y+5][i] = [14, 0]
                if randint(1, 2) == 1:
                    self.map[y - 1][i] = [6, randint(0, 2)]
                if randint(1, 4) == 1:
                    self.map[y - 1][i] = [7, randint(0, 3)]
                if randint(1, 8) == 1:
                    self.map[y - 1][i] = [9, randint(0, 3)]
                if randint(1, 10) == 1:
                    self.map[y - 1][i] = [2, randint(0, 2)]
                if randint(1, 15) == 1:
                    self.map[y - 1][i] = [10, 1]
                if randint(1, 20) == 1:
                    self.map[y - 1][i] = [3, randint(2, 4)]


Game().run()
