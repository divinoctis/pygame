import pygame
import sys
from class_game import*

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("GEODYSSEY")
pygame.display.set_icon(pygame.image.load("IMAGES/Logo.png"))
pygame.display.set_caption("indila jaune et les azteque")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
FPS = 6000
dtTarget = 1000/FPS
dt = 0

class Game:
    def __init__(self):
        pygame.init()

        self.font = pygame.font.Font(None, 100)
        self.text = self.font.render("hello",1,(0,0,0))

        self.running = True
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()

        self.spikes = spike(-260, SCREEN_HEIGHT -150,self)

        self.boule = boul(1000,SCREEN_HEIGHT -20-600,1000,self)

        self.button = Button(450, SCREEN_HEIGHT - 450, self)
        self.all_sprites.add(self.button)
        self.buttons.add(self.button)

        self.door = Door(750, SCREEN_HEIGHT - 120, self)
        self.all_sprites.add(self.door)

        self.player = Player(50, SCREEN_HEIGHT - 200, self)
        self.all_sprites.add(self.player)

        self.camera_offset_x = 0

        self.startMenu = True

        self.menuinstance = menu(1)
        self.imagemenu = pygame.image.load("LevelEditor_Eric/decor/Ciel.png")
        self.menuB0 = menu(1)
        self.menuB1 = menu(2)
        self.menuB2 = menu(3)
        self.menuB3 = menu(4)

        self.lianes = liane(self,600,1080-220)
        self.lianes1 = liane(self, 600, 1080 - 420)
        self.lianes2 = liane(self, 600, 1080 - 620)
        self.tp = tprect(self)

        self.coordonatelianel1 = self.lianes.getcoordonate()
        self.coordonatelianel2 = self.lianes1.getcoordonate()
        self.coordonatelianel3 = self.lianes2.getcoordonate()
        self.onlian=False
        self.postptarget = self.tp.getpostp()
        self.dead = True
        self.kill = False
        self.fpsafiche  = 0

        self.ground = Platform(-300, SCREEN_HEIGHT -20, 2000, 20, self)
        self.all_sprites.add(self.ground)
        self.platforms.add(self.ground)

        for i in range(4):
            self.platform = Platform(50 + i * 100, SCREEN_HEIGHT - 150 - i * 100, 100, 20, self)
            self.all_sprites.add(self.platform)
            self.platforms.add(self.platform)

    def draw(self):
        screen.blit(pygame.transform.scale(pygame.image.load("LevelEditor_Eric/decor/Ciel.png"),(1920,1080)),(0,0))
        self.player.drawlife(screen)
        self.lianes.draw(screen)
        self.lianes1.draw(screen)
        self.lianes2.draw(screen)
        self.tp.draw(screen)
        self.spikes.draw(screen)
        self.boule.draw(screen)
        for sprite in self.all_sprites:
            sprite.draw(screen)
        screen.blit(self.text,(1770,20))

        pygame.display.flip()

    def update(self,dt):

        self.text = self.font.render(f"{self.fpsafiche}", 1, (0, 0, 0))

        self.coordonateplayer = self.player.givecoord()
        domage = self.spikes.update(self.coordonateplayer)

        hits = pygame.sprite.spritecollide(self.player, self.buttons, False)
        self.veriflian = pygame.key.get_pressed()

        if self.veriflian[pygame.K_e] or self.onlian == True:
            self.onlian = self.player.liane(self.coordonatelianel1)
            self.onlian = self.player.liane(self.coordonatelianel2)
            self.onlian = self.player.liane(self.coordonatelianel3)

        if self.onlian == True:
            self.player.moveliane(dt)

        if not self.onlian :
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.player.jump_action(self.fpsafiche)

            if hits:
                self.button.activate()
                self.door.open()
            self.player.update(self.platforms,dt)
            self.player.veriftp(self.postptarget)

            self.dead = self.boule.update(self.coordonateplayer,dt)

        self.camera_offset_x = SCREEN_WIDTH // 2 - self.player.rect.x - self.player.rect.width // 2

        if domage:
            self.dead = self.player.lifesystem(-1)

    def run(self,dt):

        while self.running :
            TickStart = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            while self.startMenu :
                screen.blit(self.menuinstance.imageMenu, (0, 0))
                detectQuit()
                pos = pygame.mouse.get_pos()
                self.menuinstance.drawfont(screen)
                self.menuB0.draw(screen)
                self.startMenu= self.menuB0.detecteclick(pos)
                self.menuB1.draw(screen)
                self.menuB2.draw(screen)
                self.menuB3.draw(screen)
                self.running = self.menuB3.detecteclick(pos)

                pygame.display.flip()

            if self.dead == False:
                self.running =False

            self.update(dt)
            self.draw()

            TickEnd = pygame.time.get_ticks()
            dt = TickEnd - TickStart
            self.fpsafiche = dt
            if (dt< dtTarget):
                pygame.time.wait(int(dtTarget - dt))
                dt = dtTarget


while 1:
    g = Game()
    g.run(dt)