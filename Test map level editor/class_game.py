import pygame
import random
import sys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (16,42,42)
PURPEL = (128,0,128)
GRAY = (127,127,127)



class Camera:
    def __init__(self, width, height):
        self.WINDOW_WIDTH = width
        self.WINDOW_HEIGHT = height
        self.camera_offset_x = 0

    def update_offset(self, player_x, player_width):
        self.camera_offset_x = self.WINDOW_WIDTH // 2 - player_x - player_width // 2


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        super().__init__()
        self.image = pygame.Surface((40, 80))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jump = False
        self.SCREEN_HEIGHT = y + 50
        self.speedup = 0.5
        self.onliane = False
        self.game = game
        self.life = 3
        self.compteimage = 0
        self.images_right = []
        self.images_left = []
        self.fpsimage =7
        self.direction =2
        self.image_idel =[]
        self.idelbin = 0
        self.lockjump=False
        self.delaylife = 0

        for num in range(1, 8):
            img_right = pygame.image.load(f"class_game_images/Indila Jaune Marche/Indila_Jaune_Marche_F{num}.png")
            img_right = pygame.transform.scale(img_right, (40, 80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.imagesprit = self.images_right[0]

        for num in range(1,5):
            img_idel = pygame.image.load(f"class_game_images/Indila Jaune D/{num}.png")
            img_idel = pygame.transform.scale(img_idel,(40,80))
            self.image_idel.append(img_idel)

        self.images_coeur = []
        for num in range(0, 4):
            img_coeur = pygame.image.load(f"class_game_images/coeur/c{num}.png")
            img_coeur = pygame.transform.scale(img_coeur, (80,30))
            self.images_coeur.append(img_coeur)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x + self.game.camera_offset_x, self.rect.y))
        screen.blit(self.imagesprit, (self.rect.x + self.game.camera_offset_x, self.rect.y))

    def jump_action(self):
        if self.jump == False and self.lockjump == False:
            self.jump = True
            self.vel_y = -13

    def update(self, platforms, dt):
        self.handle_movement(dt)
        self.handle_jump()
        self.handle_collisions(platforms)
        self.handle_animation()

    def handle_movement(self,dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 0.3 * dt
            self.update_animation(self.images_left)
            self.direction=0
        elif keys[pygame.K_RIGHT]:
            self.rect.x += 0.3 * dt
            self.update_animation(self.images_right)
            self.direction = 2

    def handle_jump(self):
        if self.jump:
            self.vel_y += 0.5
            if self.rect.y + self.vel_y >= self.SCREEN_HEIGHT+80:
                self.rect.y = self.SCREEN_HEIGHT-100
                self.jump = False

            else:
                self.rect.y += self.vel_y
                self.lockjump = True

    def handle_collisions(self, platforms):
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
            self.lockjump = False

    def handle_animation(self):
        keys = pygame.key.get_pressed()
        if not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
            self.fpsimage += 1
            if self.fpsimage >= 20:
                self.fpsimage = 0
                if self.idelbin>=2:
                    self.idelbin=0
                self.imagesprit = self.image_idel[(self.idelbin)+self.direction]
                self.idelbin+=1



    def update_animation(self, image_list):
        self.fpsimage += 1
        if self.fpsimage >= 8:
            self.fpsimage = 0
            self.imagesprit = image_list[self.compteimage]
            self.compteimage += 1
            if self.compteimage > 6:
                self.compteimage = 0

    def liane(self, coordonate):
        if coordonate[1][0] < self.rect.x < coordonate[1][0] + coordonate[0][0] and coordonate[1][1] < self.rect.y < \
                coordonate[1][1] + coordonate[0][1] and self.jump == False or \
                coordonate[1][0] < self.rect.x + 30 < coordonate[1][0] + coordonate[0][0] and \
                coordonate[1][1] < self.rect.y + 30 < coordonate[1][1] + coordonate[0][1] and self.jump == False:
            return True
        else:
            return False

    def moveliane(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= 0.5 * dt
        if keys[pygame.K_RIGHT]:
            self.rect.x += 0.5 * dt
        if keys[pygame.K_UP]:
            self.rect.y -= 0.5 * dt
        if keys[pygame.K_DOWN]:
            self.rect.y += 0.5 * dt

    def veriftp(self, postptarget):
        if postptarget[0][0] < self.rect.x < postptarget[0][0] + 30 and postptarget[0][1] < self.rect.y < postptarget[0][1] + 80\
                or postptarget[0][0] < self.rect.x + 40 < postptarget[0][0] + 80 and postptarget[0][1] < self.rect.y + 30 < postptarget[0][1] + 30:
            print("ok")
            self.rect.x = postptarget[1][0]
            self.rect.y = postptarget[1][1]

    def lifesystem(self, option):
        self.delaylife +=1
        if self.delaylife >=60:
            if option < 0:
                self.life += option
                self.delaylife=0
            if option > 0:
                self.life += option
                self.delaylife = 0
            if self.life >3 :
                self.life = 3
            if self.life <= 0:
                return False
            else :
                return True

    def restart(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def drawlife(self, screen):
        screen.blit(self.images_coeur[self.life],( 50, 50))

    def givecoord(self):
        coordplayer = [self.rect.x,self.rect.y]
        return coordplayer

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, game):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.game = game

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x + self.game.camera_offset_x, self.rect.y))


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
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
        self.game = game

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x + self.game.camera_offset_x, self.rect.y))

    def activate(self):
        self.active = True
        self.image = self.active_image


class Door(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        super().__init__()
        self.image = pygame.Surface((30, 60))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.closed = True
        self.game = game

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x + self.game.camera_offset_x, self.rect.y))

    def open(self):
        self.closed = False
        self.image.fill(WHITE)


class menu:
    def __init__(self, Y):
        self.color = (175, 175, 175)
        self.hovercColor = (100, 100, 100)
        self.startPosition = [150, 50]
        self.spaceBetwen = [0, 100]
        self.imageMenu = pygame.image.load("IMAGES/GeOdyssey.png")  # REMETTRE "back.jpg" POUR LE FINAL
        size = [200, 50]
        self.rect = pygame.Rect((50, 150 + (100 * Y)), size)
        self.circl = 50, 175 + (100 * Y)
        textp = ["play", "settings", "credits", "exit"]
        self.text = textp[Y]

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def startmenu(self, win, sizefont):
        self.font = pygame.font.SysFont("Arial", sizefont)
        pygame.draw.rect(win, self.color, self.rect)
        pygame.draw.circle(win, self.color, self.circl, 25)
        self.textplace = self.font.render(self.text, True, (0, 0, 0))
        self.textrect = self.textplace.get_rect(center=self.rect.center)
        win.blit(self.textplace, self.textrect)

    def is_hover(self, pos):
        return self.rect.collidepoint(pos)

    def drawfont(self, win):
        win.blit(self.imageMenu, (0, 0))


def detectQuit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    key = pygame.key.get_pressed()
    if key[pygame.K_ESCAPE]:
        exit()


class liane():
    def __init__(self, game):
        self.size = [100, 300]
        self.pos = [600, 275]
        self.rect = pygame.Rect(self.pos, self.size)
        self.coordonate = [self.size, self.pos]
        self.game = game

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0),(self.rect.x + self.game.camera_offset_x, self.rect.y, self.rect.w, self.rect.h))

    def getcoordonate(self):
        return self.coordonate

class tprect():
    def __init__(self, game):
        self.postp = [10, 500]
        self.colortp = [90, 90, 255]
        self.sizetp = [40, 80]
        self.recttp = pygame.Rect(self.postp, self.sizetp)
        self.postarget = [400, 50]
        self.colortarget = [255, 128, 0]
        self.sizetarget = [40, 80]
        self.recttarget = pygame.Rect(self.postarget, self.sizetarget)
        self.tptargetpos = [self.postp, self.postarget]
        self.game = game

    def draw(self, screen):
        pygame.draw.rect(screen, self.colortp,
                        (self.recttp[0] + self.game.camera_offset_x, self.recttp[1], self.recttp.w, self.recttp.h))
        pygame.draw.rect(screen, self.colortarget, (
            self.recttarget[0] + self.game.camera_offset_x, self.recttarget[1], self.recttarget.w, self.recttarget.h))

    def getpostp(self):
        return self.tptargetpos

class spike():
    def __init__(self,p_x,p_y,game):
        self.spike = pygame.Surface((100,30))
        self.spike.fill(GRAY)
        self.rect = self.spike.get_rect()
        self.pos_x = p_x
        self.pos_y = p_y

        self.spikebox = pygame.Surface((140, 100))
        self.spikebox.fill(BROWN)
        self.rectbox = self.spike.get_rect()
        self.rectbox.x = 60
        self.rectbox.y = 80
        self.posbox_x = p_x - 20
        self.posbox_y = p_y + 30

        self.spikedomage = pygame.Surface((100, 80))
        self.spikedomage.fill(PURPEL)
        self.rectdomage = self.spike.get_rect()
        self.rectdomage.x = 40
        self.rectdomage.y = 80
        self.posdomage_x = p_x -20
        self.posdomage_y = p_y +30

        self.delaiactif = 15
        self.delaidesactive = 20
        self.timer = 0
        self.activat =False
        self.activattimer = False
        self.game = game

    def draw(self,screen):

        screen.blit(self.spike,(self.pos_x + self.game.camera_offset_x,self.pos_y))
        screen.blit(self.spikebox,(self.posbox_x + self.game.camera_offset_x,self.posbox_y))
        if self.activat :
            screen.blit(self.spikedomage,(self.posdomage_x + self.game.camera_offset_x,self.posdomage_y))

    def update(self,x,y):

        if not self.destroy :
            if self.posbox_x<x<self.posbox_x+self.rectbox.x and self.posbox_y<y<self.posbox_y+self.rectbox.y or \
                    self.posbox_x<x+40<self.posbox_x+self.rectbox.x and self.posbox_y<y+80<self.posbox_y+self.rectbox.y:
                self.activattimer=True

        if self.activattimer == True :
            self.time +=1
            if self.timer >= 20 :
                self.activat = True
            if self.timer>=40 :
                self.activattimer =False
                self.activat=False

        if self.activat and self.posdomage_x<x<self.posdomage_x+self.rectdomage.x and self.posdomage_y<y<self.posdomage_y or \
                self.activat and self.posdomage_x < x+40 < self.posdomage_x + self.rectdomage.x and self.posdomage_y < y+80 < self.posdomage_y :
            return True





