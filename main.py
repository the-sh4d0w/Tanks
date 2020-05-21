import json
import os

import pygame


class Bullet(pygame.sprite.Sprite):
    """The bullet class, that provides the bullets shot by tanks."""

    def __init__(self, images: list, x: int, y: int, speed: int, direction: int) -> None:
        """Initiates the bullet and sets start values.
        Takes the variables images (list), x (integer), y (integer), speed (integer) and direction (integer).
        """
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = 0
        self.rect = self.images[self.image].get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.direction = direction
        self.explosion = EXPLOSION_IMAGE

    def move(self) -> None:
        """Moves the bullet in the direction the player or tank was facing when it was shot."""
        if self.direction == 3:
            self.rect.x += self.speed
            if self.rect.x > WIDTH:
                entities.remove(self)
            self.image = 1
        elif self.direction == 2:
            self.rect.x -= self.speed
            if self.rect.x < 0:
                entities.remove(self)
            self.image = 1
        if self.direction == 1:
            self.rect.y += self.speed
            if self.rect.y > HEIGHT:
                entities.remove(self)
            self.image = 0
        elif self.direction == 0:
            self.rect.y -= self.speed
            if self.rect.x < 0:
                entities.remove(self)
            self.image = 0
        collisions_tanks = [self.rect.colliderect(
            entity.rect) for entity in entities if self != entity]
        if True in collisions_tanks:
            entities.remove(self)
            entities.remove(entities[collisions_tanks.index(True)])
            window.blit(self.explosion, (self.rect.x - 10, self.rect.y - 10))
            pygame.mixer.music.load(EXPLOSION_SOUND_PATH)
            pygame.mixer.music.play()
        if True in [self.rect.colliderect(wall.rect) for wall in walls]:
            entities.remove(self)
        if self.rect.colliderect(player.rect):
            pygame.mixer.music.load(EXPLOSION_SOUND_PATH)
            pygame.mixer.music.play()
            game_over()

    def attack(self) -> None:
        pass

    def update(self) -> None:
        """Updates the bullet on the screen."""
        window.blit(self.images[self.image], (self.rect.x, self.rect.y))


class Player(pygame.sprite.Sprite):
    """The player class, provides the tank, that is controllable by the player."""

    def __init__(self, images: list, x: int, y: int, speed: int) -> None:
        """Initiates the player and sets start values.
        Takes the variables images (list), x (integer), y (integer) and speed (integer).
        """
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = 0
        self.rect = self.images[self.image].get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def movex(self, x: int) -> None:
        """Moves in x-direction with positive or negative speed.
        Takes variable x (int)."""
        self.rect.x += x
        if x > 0:
            self.image = 3
        else:
            self.image = 2
        if self.rect.x > WIDTH - self.rect.width:
            self.rect.x = WIDTH - self.rect.width
        elif self.rect.x < 0:
            self.rect.x = 0
        if True in [self.rect.colliderect(entity.rect) for entity in entities] \
                or True in [self.rect.colliderect(wall.rect) for wall in walls]:
            self.rect.x -= x

    def movey(self, y: int) -> None:
        """Moves in y-direction with positive or negative speed.
        Takes variable y (int)."""
        self.rect.y += y
        if y > 0:
            self.image = 1
        else:
            self.image = 0
        if self.rect.y > HEIGHT - self.rect.height:
            self.rect.y = HEIGHT - self.rect.height
        elif self.rect.y < 0:
            self.rect.y = 0
        if True in [self.rect.colliderect(entity.rect) for entity in entities] \
                or True in [self.rect.colliderect(wall.rect) for wall in walls]:
            self.rect.y -= y

    def attack(self) -> None:
        """Spawns a bullet moving in the direction the player is facing."""
        if self.image == 0:
            x = self.rect.x + 16
            y = self.rect.y
        elif self.image == 1:
            x = self.rect.x + 16
            y = self.rect.y + 32
        if self.image == 2:
            x = self.rect.x
            y = self.rect.y + 16
        elif self.image == 3:
            x = self.rect.x + 32
            y = self.rect.y + 16
        entities.append(Bullet(BULLET_IMAGES, x, y, 5, self.image))
        pygame.mixer.music.load(SHOT_SOUND_PATH)
        pygame.mixer.music.play()

    def update(self) -> None:
        """Updates the player on the screen."""
        window.blit(self.images[self.image], (self.rect.x, self.rect.y))


class Tank(pygame.sprite.Sprite):
    """Tank class, that provides the enemy."""

    def __init__(self, images: list, x: int, y: int, speed: int, radius: int) -> None:
        """Initiates the tank and sets start values.
        Takes the variables images (list), x (integer), y (integer) and speed (integer).
        """
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = 0
        self.rect = self.images[self.image].get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.radius = radius
        self.attack_allowed = 0

    def move(self) -> None:
        """Moves the tank in the direction of the player."""
        if abs(player.rect.x - self.rect.x) > abs(player.rect.y - self.rect.y):
            if player.rect.x > self.rect.x:
                self.rect.x += self.speed
                if True in [self.rect.colliderect(entity.rect) for entity in entities if entity != self] \
                        or self.rect.colliderect(player.rect) or True in [self.rect.colliderect(wall.rect) for wall in walls]:
                    self.rect.x -= self.speed
                self.image = 3
            elif player.rect.x < self.rect.x:
                self.rect.x -= self.speed
                if True in [self.rect.colliderect(entity.rect) for entity in entities if entity != self] \
                        or self.rect.colliderect(player.rect) or True in [self.rect.colliderect(wall.rect) for wall in walls]:
                    self.rect.x += self.speed
                self.image = 2
        elif abs(player.rect.x - self.rect.x) < abs(player.rect.y - self.rect.y):
            if player.rect.y > self.rect.y:
                self.rect.y += self.speed
                if True in [self.rect.colliderect(entity.rect) for entity in entities if entity != self] \
                        or self.rect.colliderect(player.rect) or True in [self.rect.colliderect(wall.rect) for wall in walls]:
                    self.rect.y -= self.speed
                self.image = 1
            elif player.rect.y < self.rect.y:
                self.rect.y -= self.speed
                if True in [self.rect.colliderect(entity.rect) for entity in entities if entity != self] \
                        or self.rect.colliderect(player.rect) or True in [self.rect.colliderect(wall.rect) for wall in walls]:
                    self.rect.y += self.speed
                self.image = 0
        else:
            if player.rect.x > self.rect.x:
                self.rect.x += self.speed
                if True in [self.rect.colliderect(entity.rect) for entity in entities if entity != self] \
                        or self.rect.colliderect(player.rect) or True in [self.rect.colliderect(wall.rect) for wall in walls]:
                    self.rect.x -= self.speed
                self.image = 3
            elif player.rect.x < self.rect.x:
                self.rect.x -= self.speed
                if True in [self.rect.colliderect(entity.rect) for entity in entities if entity != self] \
                        or self.rect.colliderect(player.rect) or True in [self.rect.colliderect(wall.rect) for wall in walls]:
                    self.rect.x += self.speed
                self.image = 2

    def attack(self) -> None:
        """Spawns a bullet moving in the direction the tank is facing
        if it is in a certain radius around the player."""
        if abs(player.rect.x - self.rect.x) < self.radius \
                and abs(player.rect.y - self.rect.y) < self.radius:
            if not self.attack_allowed:
                if self.image == 0:
                    x = self.rect.x + 16
                    y = self.rect.y
                elif self.image == 1:
                    x = self.rect.x + 16
                    y = self.rect.y + 32
                if self.image == 2:
                    x = self.rect.x
                    y = self.rect.y + 16
                elif self.image == 3:
                    x = self.rect.x + 32
                    y = self.rect.y + 16
                entities.append(Bullet(BULLET_IMAGES, x, y, 5, self.image))
                pygame.mixer.music.load(SHOT_SOUND_PATH)
                pygame.mixer.music.play()
                self.attack_allowed = 10
            else:
                self.attack_allowed -= 1

    def update(self) -> None:
        """Updates the tank on the screen."""
        window.blit(self.images[self.image], (self.rect.x, self.rect.y))


class Wall(pygame.sprite.Sprite):
    """Wall class, provides barriers."""

    def __init__(self, image, x: int, y: int) -> None:
        """Initiates the wall and sets start values.
        Takes the variables image (I son't really know), x (integer) and y (integer).
        """
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self) -> None:
        """Updates the wall on the screen."""
        window.blit(self.image, (self.rect.x, self.rect.y))


# initiating pygame
pygame.init()

# creating window
WIDTH, HEIGHT = 800, 400
window = pygame.display.set_mode(
    size=(WIDTH, HEIGHT), flags=pygame.SCALED | pygame.RESIZABLE)
pygame.display.set_caption("Tanks")
pygame.display.set_icon(pygame.image.load(
    f"images{os.sep}player{os.sep}player_up.png"))
clock = pygame.time.Clock()

# images for player tank
PLAYER_IMAGE_UP = pygame.image.load(
    f"images{os.sep}player{os.sep}player_up.png").convert_alpha()
PLAYER_IMAGE_DOWN = pygame.image.load(
    f"images{os.sep}player{os.sep}player_down.png").convert_alpha()
PLAYER_IMAGE_LEFT = pygame.image.load(
    f"images{os.sep}player{os.sep}player_left.png").convert_alpha()
PLAYER_IMAGE_RIGHT = pygame.image.load(
    f"images{os.sep}player{os.sep}player_right.png").convert_alpha()
PLAYER_IMAGES = [PLAYER_IMAGE_UP, PLAYER_IMAGE_DOWN,
                 PLAYER_IMAGE_LEFT, PLAYER_IMAGE_RIGHT]
# images for green tank
TANK_GREEN_IMAGE_UP = pygame.image.load(
    f"images{os.sep}tank_green{os.sep}tank_green_up.png").convert_alpha()
TANK_GREEN_IMAGE_DOWN = pygame.image.load(
    f"images{os.sep}tank_green{os.sep}tank_green_down.png").convert_alpha()
TANK_GREEN_IMAGE_LEFT = pygame.image.load(
    f"images{os.sep}tank_green{os.sep}tank_green_left.png").convert_alpha()
TANK_GREEN_IMAGE_RIGHT = pygame.image.load(
    f"images{os.sep}tank_green{os.sep}tank_green_right.png").convert_alpha()
TANK_GREEN_IMAGES = [TANK_GREEN_IMAGE_UP, TANK_GREEN_IMAGE_DOWN,
                     TANK_GREEN_IMAGE_LEFT, TANK_GREEN_IMAGE_RIGHT]
# images for red tank
TANK_RED_IMAGE_UP = pygame.image.load(
    f"images{os.sep}tank_red{os.sep}tank_red_up.png").convert_alpha()
TANK_RED_IMAGE_DOWN = pygame.image.load(
    f"images{os.sep}tank_red{os.sep}tank_red_down.png").convert_alpha()
TANK_RED_IMAGE_LEFT = pygame.image.load(
    f"images{os.sep}tank_red{os.sep}tank_red_left.png").convert_alpha()
TANK_RED_IMAGE_RIGHT = pygame.image.load(
    f"images{os.sep}tank_red{os.sep}tank_red_right.png").convert_alpha()
TANK_RED_IMAGES = [TANK_RED_IMAGE_UP, TANK_RED_IMAGE_DOWN,
                   TANK_RED_IMAGE_LEFT, TANK_RED_IMAGE_RIGHT]
# images for yellow tank
TANK_YELLOW_IMAGE_UP = pygame.image.load(
    f"images{os.sep}tank_yellow{os.sep}tank_yellow_up.png").convert_alpha()
TANK_YELLOW_IMAGE_DOWN = pygame.image.load(
    f"images{os.sep}tank_yellow{os.sep}tank_yellow_down.png").convert_alpha()
TANK_YELLOW_IMAGE_LEFT = pygame.image.load(
    f"images{os.sep}tank_yellow{os.sep}tank_yellow_left.png").convert_alpha()
TANK_YELLOW_IMAGE_RIGHT = pygame.image.load(
    f"images{os.sep}tank_yellow{os.sep}tank_yellow_right.png").convert_alpha()
TANK_YELLOW_IMAGES = [TANK_YELLOW_IMAGE_UP, TANK_YELLOW_IMAGE_DOWN,
                      TANK_YELLOW_IMAGE_LEFT, TANK_YELLOW_IMAGE_RIGHT]
# images for bullet
BULLET_X_IMAGE = pygame.image.load(
    f"images{os.sep}bullet{os.sep}bullet_x.png").convert_alpha()
BULLET_Y_IMAGE = pygame.image.load(
    f"images{os.sep}bullet{os.sep}bullet_y.png").convert_alpha()
BULLET_IMAGES = [BULLET_X_IMAGE, BULLET_Y_IMAGE]
# images for walls
WALL_I_X_IMAGE = pygame.image.load(f"images{os.sep}wall{os.sep}wall_I_x.png")
WALL_I_Y_IMAGE = pygame.image.load(f"images{os.sep}wall{os.sep}wall_I_y.png")
# image for explosion
EXPLOSION_IMAGE = pygame.image.load(
    f"images{os.sep}explosion.png").convert_alpha()

colors = {"green": TANK_GREEN_IMAGES,
          "red": TANK_RED_IMAGES, "yellow": TANK_YELLOW_IMAGES}
wall_types = {"I_x": WALL_I_X_IMAGE, "I_y": WALL_I_Y_IMAGE}
player = None
entities = None
walls = None
level = 1

# music
BACKGROUND_MUSIC_PATH = f"sound{os.sep}background_song.wav"
MENU_MUSIC_PATH = f"sound{os.sep}menu_song.wav"
GAME_OVER_MUSIC_PATH = f"sound{os.sep}game_over_song.wav"
WINNER_MUSIC_PATH = f"sound{os.sep}winner_song.wav"
# sounds
EXPLOSION_SOUND_PATH = f"sound{os.sep}explosion_sound.wav"
SHOT_SOUND_PATH = f"sound{os.sep}shot_sound.wav"


def load_level(level_nummer: int) -> None:
    """Loads level from json file."""
    global player
    global entities
    global walls
    with open(f"level_{level_nummer}.json", "r") as f:
        level = json.load(f)
    spawn_x, spawn_y = tuple(level["spawn"])
    tanks = level["enemies"]
    walls_ = level["walls"]
    player = Player(PLAYER_IMAGES, spawn_x, spawn_y, 2)
    entities = []
    for tank in tanks:
        x, y = tuple(tank["spawn"])
        entities.append(Tank(colors[tank["color"]], x, y, 1, 50))
    walls = []
    for wall in walls_:
        x, y = tuple(wall["position"])
        walls.append(Wall(wall_types[wall["type"]], x, y))


def menu_screen() -> None:
    """Starts the menu screen."""
    menu = True
    start = True
    pygame.mixer.music.load(MENU_MUSIC_PATH)
    pygame.mixer.music.play(-1)
    while menu:
        window.fill((190, 190, 190))
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
        window.blit(pygame.font.SysFont("", 40).render(
            "Tanks", False, (0, 0, 255)), (380, 70))
        if start:
            window.blit(pygame.font.SysFont("", 20).render(
                "Starten", False, (0, 0, 150)), (380, 150))
            window.blit(pygame.font.SysFont("", 20).render(
                "Beenden", False, (0, 0, 0)), (380, 200))
        else:
            window.blit(pygame.font.SysFont("", 20).render(
                "Starten", False, (0, 0, 0)), (380, 150))
            window.blit(pygame.font.SysFont("", 20).render(
                "Beenden", False, (0, 0, 150)), (380, 200))
        pygame.display.update()
        clock.tick(60)
    pygame.mixer.music.stop()
    game_loop()


def winner_screen() -> None:
    """The winner screen."""
    global level
    level += 1
    game_over_ = True
    ok = True
    pygame.mixer.music.load(WINNER_MUSIC_PATH)
    pygame.mixer.music.play(-1)
    while game_over_:
        window.fill((190, 190, 190))
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
                        game_over_ = False
                    else:
                        pygame.quit()
                        quit()
        window.blit(pygame.font.SysFont("", 50).render(
            "Du hast gewonnen!", False, (0, 155, 0)), (240, 150))
        if ok:
            window.blit(pygame.font.SysFont("", 20).render(
                "Weiter", False, (0, 0, 150)), (280, 200))
            window.blit(pygame.font.SysFont("", 20).render(
                "Beenden", False, (0, 0, 0)), (420, 200))
        else:
            window.blit(pygame.font.SysFont("", 20).render(
                "Weiter", False, (0, 0, 0)), (280, 200))
            window.blit(pygame.font.SysFont("", 20).render(
                "Beenden", False, (0, 0, 150)), (420, 200))
        pygame.display.update()
        clock.tick(60)
    pygame.mixer.music.stop()
    game_loop()


def game_over() -> None:
    """The game over screen."""
    global level
    level = 1
    game_over_ = True
    ok = True
    pygame.mixer.music.load(GAME_OVER_MUSIC_PATH)
    pygame.mixer.music.play(-1)
    while game_over_:
        window.fill((190, 190, 190))
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
                        game_over_ = False
                    else:
                        pygame.quit()
                        quit()
        window.blit(pygame.font.SysFont("", 50).render(
            "GAME OVER", False, (255, 0, 0)), (300, 150))
        if ok:
            window.blit(pygame.font.SysFont("", 20).render(
                "OK", False, (0, 0, 150)), (300, 200))
            window.blit(pygame.font.SysFont("", 20).render(
                "Beenden", False, (0, 0, 0)), (420, 200))
        else:
            window.blit(pygame.font.SysFont("", 20).render(
                "OK", False, (0, 0, 0)), (300, 200))
            window.blit(pygame.font.SysFont("", 20).render(
                "Beenden", False, (0, 0, 150)), (420, 200))
        pygame.display.update()
        clock.tick(60)
    pygame.mixer.music.stop()
    game_loop()


def game_loop() -> None:
    """The main game loop that updates everyting."""
    global level
    try:
        load_level(level)
    except:
        level = 1
        load_level(level)
    game = True
    pygame.mixer.music.load(BACKGROUND_MUSIC_PATH)
    pygame.mixer.music.play(-1)
    while game:
        window.fill((190, 190, 190))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game = False
                if event.key == ord("k"):
                    player.attack()
        keys = pygame.key.get_pressed()
        if keys[ord("a")]:
            player.movex(-player.speed)
        elif keys[ord("d")]:
            player.movex(player.speed)
        elif keys[ord("s")]:
            player.movey(player.speed)
        elif keys[ord("w")]:
            player.movey(-player.speed)
        player.update()
        for entity in entities:
            entity.move()
            entity.attack()
            entity.update()
        for wall in walls:
            wall.update()
        pygame.display.update()
        clock.tick(60)
        if not entities:
            winner_screen()
    pygame.mixer.music.stop()
    menu_screen()


menu_screen()
