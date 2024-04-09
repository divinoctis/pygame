import pygame
import random
import sys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Camera:
    def __init__(self, width, height):
        self.WINDOW_WIDTH = width
        self.WINDOW_HEIGHT = height
        self.camera_offset_x = 0

    def update_offset(self, player_x, player_width):
        self.camera_offset_x = self.WINDOW_WIDTH // 2 - player_x - player_width // 2

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jump = False
        self.SCREEN_HEIGHT = y +50
        self.speedup = 0.5
        self.onliane = False

    def jump_action(self):
        if not self.jump:
            self.jump = True
            self.vel_y = -10

    def update(self, platforms):

        if self.jump:
            self.vel_y += 0.5
            if self.rect.y + self.vel_y >= self.SCREEN_HEIGHT - 30:
                self.rect.y = self.SCREEN_HEIGHT - 30
                self.jump = False
            else:
                self.rect.y += self.vel_y

        platform_collision = pygame.sprite.spritecollideany(self, platforms)

        if platform_collision:
            if self.vel_y > 0:
                self.rect.bottom = platform_collision.rect.top
                self.vel_y = 0
                self.jump = False

            elif self.vel_y < 0:
                self.rect.top = platform_collision.rect.bottom
                self.vel_y = 0
        elif not platform_collision and self.jump == False:
            self.rect.y += 5
            self.jump = False
        print(self.rect.x,"  ---  ",self.rect.y)


        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

    def liane(self,coordonate):
        if coordonate[1][0]< self.rect.x<coordonate[1][0]+coordonate[0][0] and coordonate[1][1]<self.rect.y< coordonate[1][1]+coordonate[1][0]:
            return True
        else :
            return False



    def moveliane(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_UP]:
            self.rect.y -= 5
        if keys[pygame.K_DOWN]:
            self.rect.y += 5

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.inactive_image = pygame.Surface((50, 20))
        self.inactive_image.fill(BLUE)
        self.active_image = pygame.Surface((50, 20))
        self.active_image.fill(GREEN)
        self.image = self.inactive_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.active = False

    def activate(self):
        self.active = True
        self.image = self.active_image

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 60))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.closed = True

    def open(self):
        self.closed = False
        self.image.fill(WHITE)

class menu:
    def __init__(self,Y):
        self.color = (175, 175, 175)
        self.hovercColor = (100, 100, 100)
        self.startPosition = [150, 50]
        self.spaceBetwen = [0, 100]
        self.imageMenu = pygame.image.load("IMAGES\BG.png") #REMETTRE "back.jpg" POUR LE FINAL
        size = [200, 50]
        self.rect = pygame.Rect((50, 150 +(100 * Y)),size)
        self.circl = 50, 175 +(100 * Y)
        textp =["play", "settings", "credits", "exit"]
        self.text =  textp[Y]

    def startmenu(self, win,sizefont):
        self.font = pygame.font.SysFont("Arial",sizefont)
        pygame.draw.rect(win, self.color, self.rect)
        pygame.draw.circle(win, self.color,self.circl,25)
        self.textplace = self.font.render(self.text, True, (0, 0, 0))
        self.textrect = self.textplace.get_rect(center=self.rect.center)
        win.blit(self.textplace, self.textrect)

    def is_hover(self, pos):
        return self.rect.collidepoint(pos)

    def drawfont(self, win):
        win.blit(self.imageMenu, (0, 0))

    def click(self):
        print("click")

def detectQuit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    key = pygame.key.get_pressed()
    if key[pygame.K_ESCAPE]:
        exit()

class liane():
    def __init__(self):
        self.size = [100,300]
        self.pos = [650,275]
        self.rect = pygame.Rect(self.pos, self.size)
        self.coordonate = [self.size,self.pos]

    def draw(self,screen):
        pygame.draw.rect(screen,(0,255,0),self.rect)

    def getcoordonate(self):
        print(self.coordonate)
        return self.coordonate