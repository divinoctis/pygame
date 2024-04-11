import pygame
import random

# CODE POUR L'IA DU MOB, A AMELIORER.

pygame.init()


screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("tentative 305000")

bg = pygame.image.load("LevelEditor_Eric/decor/Ciel.png")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2)
        self.speed = 1
        self.shoot_delay = 800
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.rect.x += self.speed
        if self.rect.left <= 0 or self.rect.right >= screen_width:
            self.speed *= -1

        # Tirer
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            arrow = Arrow(self.rect.centerx, self.rect.centery)
            all_sprites.add(arrow)
            arrow_group.add(arrow)


class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 2))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 2

    def update(self):
        self.rect.x += self.speed
        if self.rect.left >= screen_width:
            self.kill()


all_sprites = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()
mob = Mob()
all_sprites.add(mob)


running = True
clock = pygame.time.Clock()
while running:
    screen.fill(BLACK)
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    all_sprites.update()
    arrow_group.update()


    all_sprites.draw(screen)
    arrow_group.draw(screen)


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
