import os

import pygame


class Bullet(pygame.sprite.Sprite):

    def __init__(self, image, speed: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.speed = speed


class Player(pygame.sprite.Sprite):

    def __init__(self, image, x: int, y: int, speed: int, health: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.health = health

    def movex(self, x: int) -> None:
        self.rect.x += x
        if self.rect.x > 768:
            self.rect.x = 768
        elif self.rect.x < 0:
            self.rect.x = 0

    def movey(self, y: int) -> None:
        self.rect.y += y
        if self.rect.y > 368:
            self.rect.y = 368
        elif self.rect.y < 0:
            self.rect.y = 0

    def update(self) -> None:
        window.blit(self.image, (self.rect.x, self.rect.y))


class Tank(pygame.sprite.Sprite):

    def __init__(self, images, x: int, y: int, speed: int, health: int, radius: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.rect = self.images[0].get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.health = health
        self.radius = radius

    def move(self) -> int:
        if abs(player.rect.x - self.rect.x) > abs(player.rect.y - self.rect.y):
            if player.rect.x > self.rect.x:
                if abs(player.rect.x - self.rect.x) > self.radius:
                    self.rect.x += self.speed
                return 3
            elif player.rect.x < self.rect.x:
                if abs(player.rect.x - self.rect.x) > self.radius:
                    self.rect.x -= self.speed
                return 2
        else:
            if player.rect.y > self.rect.y:
                if abs(player.rect.y - self.rect.y) > self.radius:
                    self.rect.y += self.speed
                return 1
            elif player.rect.y < self.rect.y:
                if abs(player.rect.y - self.rect.y) > self.radius:
                    self.rect.y -= self.speed
                return 0

    def update(self, i) -> None:
        window.blit(self.images[i], (self))


pygame.init()
window = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()

PLAYER_IMAGE_UP = pygame.image.load(
    f"images{os.sep}player_up.png").convert_alpha()
PLAYER_IMAGE_DOWN = pygame.image.load(
    f"images{os.sep}player_down.png").convert_alpha()
PLAYER_IMAGE_LEFT = pygame.image.load(
    f"images{os.sep}player_left.png").convert_alpha()
PLAYER_IMAGE_RIGHT = pygame.image.load(
    f"images{os.sep}player_right.png").convert_alpha()
player = Player(PLAYER_IMAGE_UP, 400, 300, 3, 1)
entities = [Tank([PLAYER_IMAGE_UP, PLAYER_IMAGE_DOWN,
                  PLAYER_IMAGE_LEFT, PLAYER_IMAGE_RIGHT], 30, 30, 3, 1, 18)]

while True:
    window.fill((190, 190, 190))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == ord("a"):
                player.image = PLAYER_IMAGE_LEFT
            elif event.key == ord("d"):
                player.image = PLAYER_IMAGE_RIGHT
            elif event.key == ord("s"):
                player.image = PLAYER_IMAGE_DOWN
            elif event.key == ord("w"):
                player.image = PLAYER_IMAGE_UP
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
        i = entity.move()
        entity.update(i)
    pygame.display.update()
    clock.tick(60)
