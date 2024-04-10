import pygame
import sys

# nickel 
pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 50
PLAYER_SPEED = 5
PROJECTILE_SPEED = 7
LANCER_COOLDOWN = 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jeu avec Pygame")


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.weapon = "pistolet"
        self.last_shot_time = pygame.time.get_ticks()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_UP]:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN]:
            self.rect.y += PLAYER_SPEED
        if keys[pygame.K_SPACE]:
            current_time = pygame.time.get_ticks()
            if self.weapon == "pistolet":
                if current_time - self.last_shot_time > 100:
                    self.last_shot_time = current_time
                    projectile = Projectile(self.rect.right, self.rect.centery)
                    all_sprites.add(projectile)
                    projectiles.add(projectile)
            elif self.weapon == "lance":
                if current_time - self.last_shot_time > LANCER_COOLDOWN:
                    self.last_shot_time = current_time
                    projectile = Lancer(self.rect.right, self.rect.centery)
                    all_sprites.add(projectile)
                    projectiles.add(projectile)

        if keys[pygame.K_r]:

            if self.weapon == "pistolet":
                self.weapon = "lance"
            else:
                self.weapon = "pistolet"

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.x += PROJECTILE_SPEED
        if self.rect.left > SCREEN_WIDTH:
            self.kill()


class Lancer(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 5))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.midright = (x, y)

    def update(self):
        self.rect.x += PROJECTILE_SPEED * 0.5
        if self.rect.left > SCREEN_WIDTH:
            self.kill()


all_sprites = pygame.sprite.Group()
projectiles = pygame.sprite.Group()


player = Player()
all_sprites.add(player)


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    all_sprites.update()


    screen.fill(BLACK)


    all_sprites.draw(screen)


    pygame.display.flip()


    pygame.time.Clock().tick(60)


pygame.quit()
sys.exit()
