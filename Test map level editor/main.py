import pygame
import random
import sys
from class_game import*

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("GEODYSSEY")
pygame.display.set_icon(pygame.image.load("IMAGES/logo.png"))
pygame.display.set_caption("indila jaune et les azteque")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
FPS = 60
dtTarget = 1000/FPS
dt = 0

class Game:
    def __init__(self):
        pygame.init()

        self.running = True
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()

        self.spikes = spike(-260, SCREEN_HEIGHT -150,self)

        self.button = Button(450, SCREEN_HEIGHT - 400, self)
        self.all_sprites.add(self.button)
        self.buttons.add(self.button)

        self.door = Door(750, SCREEN_HEIGHT - 120, self)
        self.all_sprites.add(self.door)

        self.player = Player(50, SCREEN_HEIGHT - 200, self)
        self.all_sprites.add(self.player)

        self.camera_offset_x = 0

        self.startMenu = True

        self.menuinstance = menu(0)
        self.imagemenu = pygame.image.load("IMAGES/BG.png") #REMETTRE "back.jpg" POUR LE FINAL
        self.menuB0 = menu(0)
        self.sizefont = 24
        self.pause = False

        self.lianes = liane(self)
        self.tp = tprect(self)

        self.coordonateliane = self.lianes.getcoordonate()
        self.onlian=False
        self.postptarget = self.tp.getpostp()
        self.dead = True

        self.ground = Platform(-300, SCREEN_HEIGHT -20, 1000, 20, self)
        self.all_sprites.add(self.ground)
        self.platforms.add(self.ground)

        for i in range(4):
            self.platform = Platform(50 + i * 100, SCREEN_HEIGHT - 100 - i * 100, 100, 20, self)
            self.all_sprites.add(self.platform)
            self.platforms.add(self.platform)

    def draw(self):
        screen.fill(BLACK)
        self.player.drawlife(screen)
        self.lianes.draw(screen)
        self.tp.draw(screen)
        self.spikes.draw(screen)
        for sprite in self.all_sprites:
            sprite.draw(screen)

        pygame.display.flip()

    def update(self,dt):

        #game loop


        #event

        hits = pygame.sprite.spritecollide(self.player, self.buttons, False)
        self.veriflian = pygame.key.get_pressed()

        if self.veriflian[pygame.K_e] or self.onlian == True:
            self.onlian = self.player.liane(self.coordonateliane)

        if self.onlian == True:
            self.player.moveliane(dt)

        if not self.onlian :
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.player.jump_action()
            if keys[pygame.K_p]:
                self.dead = self.player.lifesystem(1)
            if keys[pygame.K_m]:
                self.dead = self.player.lifesystem(-1)

            if hits:
                self.button.activate()
                self.door.open()

        #update
            self.player.update(self.platforms,dt)
            self.player.veriftp(self.postptarget)

        self.camera_offset_x = SCREEN_WIDTH // 2 - self.player.rect.x - self.player.rect.width // 2

        # draw

    def run(self,dt):

        while self.running :
            TickStart = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            while self.startMenu :
                screen.blit(self.menuinstance.imageMenu, (0, 0))
                detectQuit()
                self.menuinstance.drawfont(screen)
                self.menuB0.startmenu(screen,self.sizefont)

                pos = pygame.mouse.get_pos()
                if self.menuB0.is_hover(pos):
                    self.menuB0.color = self.menuB0.hovercColor
                    for evenement in pygame.event.get():
                        if evenement.type == pygame.MOUSEBUTTONDOWN:
                            self.startMenu = False
                else:
                    self.menuB0.color = (189,183,107)

                pygame.display.flip()

            if not self.dead:
                self.player.restart(50, SCREEN_HEIGHT - 50)

            self.update(dt)
            self.draw()

            TickEnd = pygame.time.get_ticks()
            dt = TickEnd - TickStart
            if (dt< dtTarget):
                pygame.time.wait(int(dtTarget - dt))
                dt = dtTarget

g = Game()
g.run(dt)