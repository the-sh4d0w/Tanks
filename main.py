import json
import os
import random

import pygame


class Game:

    def __init__(self):
        pygame.init()
        self.WIDTH = 800
        self.HEIGHT = 400
        self.window = pygame.display.set_mode(
            size=(self.WIDTH, self.HEIGHT), flags=pygame.SCALED | pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.player = None
        self.enemies = []
        self.bullets = []
        self.walls = []
        self.entities = []
        self.level_number = 1
        self.debug = False
        self.invulnerable = False
        with open("config.json", "r") as f:
            self.config = json.load(f)
        pygame.display.set_caption("Tanks")
        pygame.display.set_icon(pygame.image.load(
            f"images{os.sep}player{os.sep}player_up.png").convert_alpha())

    def load_level(self):
        if not os.path.isfile(f"levels{os.sep}level_{self.level_number}.json"):
            self.level_number = 1
            self.menu_screen()
        with open(f"levels{os.sep}level_{self.level_number}.json", "r") as f:
            level = json.load(f)
        self.player = Player(level["spawn"][0], level["spawn"]
                             [1], self.config["speed"], self.config["firerate"])
        self.entities = []
        self.enemies = []
        self.walls = []
        self.bullets = []
        self.entities.append(self.player)
        for enemy in level["enemies"]:
            enemy_ = Enemy(enemy["spawn"][0], enemy["spawn"][1], self.config["speeds"][enemy["color"]], self.config["firerates"]
                           [enemy["color"]], enemy["color"], self.config["detection_range"], self.config["attack_range"])
            self.enemies.append(enemy_)
        for wall in level["walls"]:
            wall_ = Wall(wall["position"][0],
                         wall["position"][1], wall["type"])
            self.walls.append(wall_)

    def game_loop(self):
        self.load_level()
        game = True
        dead = False
        pygame.mixer.music.load(f"sound{os.sep}background_song.wav")
        pygame.mixer.music.play(-1)
        while game:
            self.window.fill((190, 190, 190))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        self.enemies = []
                    elif event.key == pygame.K_F2:
                        self.invulnerable = not self.invulnerable
                    elif event.key == pygame.K_F3:
                        self.debug = not self.debug
                    elif event.key == pygame.K_F4:
                        game = False
            self.entities = self.enemies + [self.player] + self.walls
            self.player.move(self.entities, self.HEIGHT, self.WIDTH)
            self.player.attack(self.bullets)
            self.player.update(self.window)
            for enemy in self.enemies:
                enemy.move(self.entities, self.player, self.HEIGHT, self.WIDTH)
                enemy.attack(self.player, self.bullets)
                enemy.update(self.window)
            for bullet in self.bullets:
                dead = bullet.move(self.bullets, self.enemies, self.walls,
                                   self.player, self.HEIGHT, self.WIDTH, self.window)
                bullet.update(self.window)
                if dead:
                    game = False
            for wall in self.walls:
                wall.update(self.window)
            if self.invulnerable:
                game = True
            if self.debug:
                self.window.blit(pygame.font.SysFont("Consolas, 'Courier New', monospace", 10).render(
                    "player: " + str(self.player), False, (255, 255, 255)), (5, 5))
                self.window.blit(pygame.font.SysFont("Consolas, 'Courier New', monospace", 10).render(
                    "enemies: " + str(self.enemies), False, (255, 255, 255)), (5, 15))
                self.window.blit(pygame.font.SysFont("Consolas, 'Courier New', monospace", 10).render(
                    "bullets: " + str(self.bullets), False, (255, 255, 255)), (5, 25))
                self.window.blit(pygame.font.SysFont("Consolas, 'Courier New', monospace", 10).render(
                    "walls: " + str(self.walls), False, (255, 255, 255)), (5, 35))
                self.window.blit(pygame.font.SysFont("Consolas, 'Courier New', monospace", 10).render(
                    "position: " + str((self.player.rect.x, self.player.rect.y)), False, (255, 255, 255)), (5, 45))
                self.window.blit(pygame.font.SysFont("Consolas, 'Courier New', monospace", 10).render(
                    "level: " + str(self.level_number), False, (255, 255, 255)), (745, 5))
                self.window.blit(pygame.font.SysFont("Consolas, 'Courier New', monospace", 10).render(
                    "FPS: " + str(int(self.clock.get_fps())), False, (255, 255, 255)), (750, 15))
                self.window.blit(pygame.font.SysFont("Consolas, 'Courier New', monospace", 10).render(
                    "invulnerable: " + str(self.invulnerable), False, (255, 255, 255)), (680, 25))
            pygame.display.update()
            self.clock.tick(self.config["fps"])
            if not self.enemies:
                self.level_number += 1
                self.result_screen(True)
        self.result_screen(False)

    def menu_screen(self):
        menu = True
        start = True
        pygame.mixer.music.load(f"sound{os.sep}menu_song.wav")
        pygame.mixer.music.play(-1)
        while menu:
            self.window.fill((190, 190, 190))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        start = not start
                    elif event.key == pygame.K_DOWN:
                        start = not start
                    elif event.key == pygame.K_RETURN:
                        if start:
                            menu = False
                        else:
                            pygame.quit()
                            quit()
            self.window.blit(pygame.font.SysFont("Arial, Helvetica, sans-serif",
                                                 40).render("Tanks", False, (0, 0, 255)), (380, 70))
            if start:
                self.window.blit(pygame.font.SysFont("Arial, Helvetica, sans-serif",
                                                     20).render("Starten", False, (0, 0, 150)), (380, 150))
                self.window.blit(pygame.font.SysFont("Arial, Helvetica, sans-serif",
                                                     20).render("Beenden", False, (0, 0, 0)), (380, 200))
            else:
                self.window.blit(pygame.font.SysFont("Arial, Helvetica, sans-serif",
                                                     20).render("Starten", False, (0, 0, 0)), (380, 150))
                self.window.blit(pygame.font.SysFont("Arial, Helvetica, sans-serif",
                                                     20).render("Beenden", False, (0, 0, 150)), (380, 200))
            pygame.display.update()
            self.clock.tick(60)
        pygame.mixer.music.stop()
        self.game_loop()

    def result_screen(self, won):
        text = {True: "Level geschafft.", False: "GAME OVER"}
        text_ = {True: "Weiter", False: "Erneut"}
        color = {True: (0, 150, 0), False: (255, 0, 0)}
        winner = True
        ok = True
        pygame.mixer.music.load(f"sound{os.sep}winner_song.wav")
        pygame.mixer.music.play(-1)
        while winner:
            self.window.fill((190, 190, 190))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        ok = not ok
                    elif event.key == pygame.K_LEFT:
                        ok = not ok
                    elif event.key == pygame.K_RETURN:
                        if ok:
                            winner = False
                        else:
                            pygame.quit()
                            quit()
            self.window.blit(pygame.font.SysFont("Arial, Helvetica, sans-serif",
                                                 50).render(text[won], False, color[won]), (260, 120))
            if ok:
                self.window.blit(pygame.font.SysFont("Arial, Helvetica, sans-serif",
                                                     20).render(text_[won], False, (0, 0, 150)), (290, 200))
                self.window.blit(pygame.font.SysFont("Arial, Helvetica, sans-serif",
                                                     20).render("Beenden", False, (0, 0, 0)), (430, 200))
            else:
                self.window.blit(pygame.font.SysFont("Arial, Helvetica, sans-serif",
                                                     20).render(text_[won], False, (0, 0, 0)), (290, 200))
                self.window.blit(pygame.font.SysFont("Arial, Helvetica, sans-serif",
                                                     20).render("Beenden", False, (0, 0, 150)), (430, 200))
            pygame.display.update()
            self.clock.tick(60)
        pygame.mixer.music.stop()
        self.game_loop()

    def splash_screen(self):
        self.window.blit(pygame.transform.smoothscale(pygame.image.load(
            f"images{os.sep}Evil Panda Studios Logo.png").convert_alpha(), (self.WIDTH, self.HEIGHT)), (0, 0))
        pygame.display.update()
        pygame.time.wait(3000)
        self.menu_screen()


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, speed, firerate):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load(f"images{os.sep}player{os.sep}player_up.png").convert_alpha(), pygame.image.load(f"images{os.sep}player{os.sep}player_left.png").convert_alpha(
        ), pygame.image.load(f"images{os.sep}player{os.sep}player_down.png").convert_alpha(), pygame.image.load(f"images{os.sep}player{os.sep}player_right.png").convert_alpha()]
        self.rect = self.images[0].get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.direction = 0
        self.firerate = firerate
        self.fire = 0

    def move(self, entities, HEIGHT, WIDTH):
        keys = pygame.key.get_pressed()
        if keys[ord("w")]:
            self.direction = 0
            self.rect.y -= self.speed
            if any(self.rect.colliderect(entity.rect) for entity in entities if entity != self) or self.rect.y <= 0:
                self.rect.y += self.speed
        elif keys[ord("a")]:
            self.direction = 1
            self.rect.x -= self.speed
            if any(self.rect.colliderect(entity.rect) for entity in entities if entity != self) or self.rect.x <= 0:
                self.rect.x += self.speed
        elif keys[ord("s")]:
            self.direction = 2
            self.rect.y += self.speed
            if any(self.rect.colliderect(entity.rect) for entity in entities if entity != self) or self.rect.y >= (HEIGHT - 32):
                self.rect.y -= self.speed
        elif keys[ord("d")]:
            self.direction = 3
            self.rect.x += self.speed
            if any(self.rect.colliderect(entity.rect) for entity in entities if entity != self) or self.rect.x >= (WIDTH - 32):
                self.rect.x -= self.speed

    def attack(self, bullets):
        keys = pygame.key.get_pressed()
        if keys[ord("k")]:
            if self.fire == 0:
                self.fire = self.firerate
                bullets.append(
                    Bullet(self.rect.x, self.rect.y, 4, self.direction))
            else:
                self.fire -= 1
        else:
            self.fire = 0

    def update(self, window):
        window.blit(self.images[self.direction], (self.rect.x, self.rect.y))


class Enemy(pygame.sprite.Sprite):

    def __init__(self, x, y, speed, firerate, color, detection_range, attack_range):
        pygame.sprite.Sprite.__init__(self)
        images = {
            "red": [pygame.image.load(f"images{os.sep}tank_red{os.sep}tank_red_up.png").convert_alpha(), pygame.image.load(f"images{os.sep}tank_red{os.sep}tank_red_left.png").convert_alpha(), pygame.image.load(f"images{os.sep}tank_red{os.sep}tank_red_down.png").convert_alpha(), pygame.image.load(f"images{os.sep}tank_red{os.sep}tank_red_right.png").convert_alpha()],
            "yellow": [pygame.image.load(f"images{os.sep}tank_yellow{os.sep}tank_yellow_up.png").convert_alpha(), pygame.image.load(f"images{os.sep}tank_yellow{os.sep}tank_yellow_left.png").convert_alpha(), pygame.image.load(f"images{os.sep}tank_yellow{os.sep}tank_yellow_down.png").convert_alpha(), pygame.image.load(f"images{os.sep}tank_yellow{os.sep}tank_yellow_right.png").convert_alpha()],
            "green": [pygame.image.load(f"images{os.sep}tank_green{os.sep}tank_green_up.png").convert_alpha(), pygame.image.load(f"images{os.sep}tank_green{os.sep}tank_green_left.png").convert_alpha(), pygame.image.load(f"images{os.sep}tank_green{os.sep}tank_green_down.png").convert_alpha(), pygame.image.load(f"images{os.sep}tank_green{os.sep}tank_green_right.png").convert_alpha(), pygame.image.load(f"images{os.sep}tank_green{os.sep}tank_green_right.png").convert_alpha()]
        }
        self.images = images[color]
        self.rect = self.images[0].get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.direction = 0
        self.detection_range = detection_range
        self.detected_player = False
        self.attack_range = attack_range
        self.firerate = firerate
        self.fire = self.firerate

    def move(self, entities, player, HEIGHT, WIDTH):
        if not self.detected_player:
            center_x = self.rect.x + 16
            center_y = self.rect.y + 16
            player_center_x = player.rect.x + 16
            player_center_y = player.rect.y + 16
            if abs(player_center_x - center_x) < self.detection_range \
                    and abs(player_center_y - center_y) < self.detection_range:
                self.detected_player = True
        if self.detected_player:
            if abs(player.rect.x - self.rect.x) > abs(player.rect.y - self.rect.y):
                if self.rect.x < player.rect.x:
                    self.direction = 3
                    self.rect.x += self.speed
                    if any(self.rect.colliderect(entity.rect) for entity in entities if entity != self) or self.rect.y <= 0:
                        self.rect.x -= self.speed
                elif self.rect.x > player.rect.x:
                    self.direction = 1
                    self.rect.x -= self.speed
                    if any(self.rect.colliderect(entity.rect) for entity in entities if entity != self) or self.rect.x <= 0:
                        self.rect.x += self.speed
            else:
                if self.rect.y < player.rect.y:
                    self.direction = 2
                    self.rect.y += self.speed
                    if any(self.rect.colliderect(entity.rect) for entity in entities if entity != self) or self.rect.y >= (HEIGHT - 32):
                        self.rect.y -= self.speed
                elif self.rect.y > player.rect.y:
                    self.direction = 0
                    self.rect.y -= self.speed
                    if any(self.rect.colliderect(entity.rect) for entity in entities if entity != self) or self.rect.x >= (WIDTH - 32):
                        self.rect.y += self.speed

    def attack(self, player, bullets):
        center_x = self.rect.x + 16
        center_y = self.rect.y + 16
        player_center_x = player.rect.x + 16
        player_center_y = player.rect.y + 16
        if abs(player_center_x - center_x) < self.attack_range and abs(player_center_y - center_y) < self.attack_range:
            if self.fire == 0:
                self.fire = self.firerate
                bullets.append(
                    Bullet(self.rect.x, self.rect.y, 4, self.direction))
            else:
                self.fire -= 1

    def update(self, window):
        window.blit(self.images[self.direction], (self.rect.x, self.rect.y))


class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y, speed, direction):
        pygame.sprite.Sprite.__init__(self)
        images = {
            0: pygame.image.load(f"images{os.sep}bullet{os.sep}bullet_y.png").convert(),
            1: pygame.image.load(f"images{os.sep}bullet{os.sep}bullet_x.png").convert(),
            2: pygame.image.load(f"images{os.sep}bullet{os.sep}bullet_y.png").convert(),
            3: pygame.image.load(f"images{os.sep}bullet{os.sep}bullet_x.png").convert()
        }
        x_ = {
            0: x + 16,
            1: x,
            2: x + 16,
            3: x + 32
        }
        y_ = {
            0: y,
            1: y + 16,
            2: y + 32,
            3: y + 16
        }
        self.image = images[direction]
        self.rect = self.image.get_rect()
        self.rect.x = x_[direction]
        self.rect.y = y_[direction]
        self.speed = speed
        self.direction = direction
        pygame.mixer.Sound(f"sound{os.sep}shot_sound.wav").play()

    def move(self, bullets, enemies, walls, player, HEIGHT, WIDTH, window):
        if self.direction == 0:
            self.rect.y -= self.speed
        elif self.direction == 1:
            self.rect.x -= self.speed
        elif self.direction == 2:
            self.rect.y += self.speed
        elif self.direction == 3:
            self.rect.x += self.speed
        if self.rect.x <= 0 or self.rect.x >= WIDTH or self.rect.y <= 0 or self.rect.y >= HEIGHT:
            bullets.remove(self)
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                enemies.remove(enemy)
                bullets.remove(self)
                pygame.mixer.Sound(f"sound{os.sep}explosion_sound.wav").play()
                window.blit(pygame.image.load(
                    f"images{os.sep}explosion.png").convert_alpha(), (self.rect.x, self.rect.y))
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                bullets.remove(self)
        if self.rect.colliderect(player.rect):
            pygame.mixer.Sound(f"sound{os.sep}explosion_sound.wav").play()
            window.blit(pygame.image.load(
                f"images{os.sep}explosion.png").convert_alpha(), (self.rect.x, self.rect.y))
            return True

    def update(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Wall(pygame.sprite.Sprite):

    def __init__(self, x, y, type_):
        pygame.sprite.Sprite.__init__(self)
        images = {
            "I_x": pygame.image.load(f"images{os.sep}wall{os.sep}wall_I_x.png").convert(),
            "I_y": pygame.image.load(f"images{os.sep}wall{os.sep}wall_I_y.png").convert()
        }
        self.image = images[type_]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))


Game().splash_screen()
