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
            if self.rect.x > width:
                entities.remove(self)
            self.image = 1
        elif self.direction == 2:
            self.rect.x -= self.speed
            if self.rect.x < 0:
                entities.remove(self)
            self.image = 1
        if self.direction == 1:
            self.rect.y += self.speed
            if self.rect.y > height:
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
            window.blit(self.explosion, (self.rect.x, self.rect.y))
        if True in [self.rect.colliderect(wall.rect) for wall in walls]:
            entities.remove(self)

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
        if self.rect.x > width - 32:
            self.rect.x = width - 32
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
        if self.rect.y > height - 32:
            self.rect.y = height - 32
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

    def update(self) -> None:
        """Updates the player on the screen."""
        window.blit(self.images[self.image], (self.rect.x, self.rect.y))


class Tank(pygame.sprite.Sprite):
    """Tank class, that provides the enemy."""

    def __init__(self, images: list, x: int, y: int, speed: int) -> None:
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
        else:
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

    def attack(self) -> None:
        """Spawns a bullet moving in the direction the tank is facing."""
        entities.append(Bullet(BULLET_IMAGES, self.rect.x,
                               self.rect.y, 5, self.image))

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
window = pygame.display.set_mode(flags=pygame.FULLSCREEN)
width, height = pygame.display.get_surface().get_size()
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
# image for explosion
EXPLOSION_IMAGE = pygame.image.load(
    f"images{os.sep}explosion.png").convert_alpha()

# creating player and tanks
player = Player(PLAYER_IMAGES, 400, 300, 2)
entities = [Tank(TANK_GREEN_IMAGES, 30, 30, 1), Tank(
    TANK_RED_IMAGES, 600, 50, 1), Tank(TANK_YELLOW_IMAGES, 600, 360, 1)]
walls = [Wall(WALL_I_X_IMAGE, 1000, 700)]

# main game loop
while True:
    window.fill((190, 190, 190))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
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
        entity.update()
    for wall in walls:
        wall.update()
    pygame.display.update()
    clock.tick(60)
