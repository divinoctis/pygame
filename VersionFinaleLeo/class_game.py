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



class Camera:   # cette classe permet se simuler le fait que la fenetre est fixer au perssonage
    def __init__(self, width, height):
        self.WINDOW_WIDTH = width
        self.WINDOW_HEIGHT = height
        self.camera_offset_x = 0

    def update_offset(self, player_x, player_width):
        self.camera_offset_x = self.WINDOW_WIDTH // 2 - player_x - player_width // 2


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        super().__init__()
        self.image = pygame.Surface((120, 240))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - 300
        self.vel_y = 0
        self.jump = False
        self.SCREEN_HEIGHT = y + 200
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
        self.delaylife = 60

        for num in range(1, 8):     # recupere les animation de marche et cree les diferent liste d'animation de droit et gauche
            img_right = pygame.image.load(f"VersionFinaleLeo/Indila Jaune Marche/Indila_Jaune_Marche_F{num}.png")
            img_right = pygame.transform.scale(img_right, (120, 240))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.imagesprit = self.images_right[0]

        for num in range(1,5):      # recuper les image d'animation d'idle
            img_idel = pygame.image.load(f"VersionFinaleLeo/Indila Jaune D/{num}.png")
            img_idel = pygame.transform.scale(img_idel,(120, 240))
            self.image_idel.append(img_idel)

        self.images_coeur = []
        for num in range(0, 4):     # recupere les image de la vie
            img_coeur = pygame.image.load(f"VersionFinaleLeo/coeur/c{num}.png")
            img_coeur = pygame.transform.scale(img_coeur, (160,60))
            self.images_coeur.append(img_coeur)

    def draw(self, screen): # afiche le player et sa zone de colision pour les test
        # screen.blit(self.image, (self.rect.x + self.game.camera_offset_x, self.rect.y))
        screen.blit(self.imagesprit, (self.rect.x + self.game.camera_offset_x, self.rect.y))

    def jump_action(self):      # capte si le joeur veut sauter
        if self.jump == False and self.lockjump == False:
            self.jump = True
            self.vel_y = -13

    def update(self, platforms, dt): # met a jour tout les fonction
        self.handle_movement(dt)
        self.handle_jump()
        self.handle_collisions(platforms)
        self.handle_animation()
        self.delaylife += 1

    def handle_movement(self,dt):       # permet de deplacer le perssonage de droite a gauche et de gauche a droit
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 0.3 * dt
            self.update_animation(self.images_left)
            self.direction=0
        elif keys[pygame.K_RIGHT]:
            self.rect.x += 0.3 * dt
            self.update_animation(self.images_right)
            self.direction = 2

    def handle_jump(self):      # permet de simuler un saut
        if self.jump:
            self.vel_y += 0.5
            if self.rect.y + self.vel_y >= self.SCREEN_HEIGHT+80:
                self.rect.y = self.SCREEN_HEIGHT-100
                self.jump = False

            else:
                self.rect.y += self.vel_y
                self.lockjump = True

    def handle_collisions(self, platforms):     # permet de gere les colision en haut et en bas pendant les saut
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

    def handle_animation(self):     # permet de gere l'animation idle en fonction du temps
        keys = pygame.key.get_pressed()
        if not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
            self.fpsimage += 1
            if self.fpsimage >= 20:
                self.fpsimage = 0
                if self.idelbin>=2:
                    self.idelbin=0
                self.imagesprit = self.image_idel[(self.idelbin)+self.direction]
                self.idelbin+=1



    def update_animation(self, image_list): # permet de gere les animation de deplacement en fonction du temp
        self.fpsimage += 1
        if self.fpsimage >= 8:
            self.fpsimage = 0
            self.imagesprit = image_list[self.compteimage]
            self.compteimage += 1
            if self.compteimage > 6:
                self.compteimage = 0

    def liane(self, coordonate):        # permet de savoir si e jouer est sur les lian et dans leur zone
        if coordonate[1][0] < self.rect.x < coordonate[1][0] + coordonate[0][0] and coordonate[1][1] < self.rect.y < \
                coordonate[1][1] + coordonate[0][1] and self.jump == False or \
                coordonate[1][0] < self.rect.x + 40 < coordonate[1][0] + coordonate[0][0] and \
                coordonate[1][1] < self.rect.y + 80 < coordonate[1][1] + coordonate[0][1] and self.jump == False:
            return True
        else:
            return False

    def moveliane(self, dt):        # permet de desactiver temporairement la graviter quand le joeur est sur les liane
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= 0.5 * dt
        if keys[pygame.K_RIGHT]:
            self.rect.x += 0.5 * dt
        if keys[pygame.K_UP]:
            self.rect.y -= 0.5 * dt
        if keys[pygame.K_DOWN]:
            self.rect.y += 0.5 * dt

    def veriftp(self, postptarget):      # permet de teleporter le player sur les coordoner fourni par le teleporteur
        if postptarget[0][0] < self.rect.x < postptarget[0][0] + 30 and postptarget[0][1] < self.rect.y < postptarget[0][1] + 80\
                or postptarget[0][0] < self.rect.x + 40 < postptarget[0][0] + 80 and postptarget[0][1] < self.rect.y + 30 < postptarget[0][1] + 30:
            self.rect.x = postptarget[1][0]
            self.rect.y = postptarget[1][1]

    def lifesystem(self, option):  # permet de verifier si le player gagne ou pert une vie ou si il est mort

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

    def drawlife(self, screen): # afiche l'imae de la vie corespondant
        screen.blit(self.images_coeur[self.life],( 50, 50))

    def givecoord(self):        # fournie les coordoner du player pour les autre class
        coordplayer = [self.rect.x,self.rect.y]
        return coordplayer

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, game):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.game = game

    def draw(self, screen):     # afiche la platforme
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

    def draw(self, screen):     # afiche le bouton
        screen.blit(self.image, (self.rect.x + self.game.camera_offset_x, self.rect.y))

    def activate(self):         # permet d'activer le bouton
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

    def draw(self, screen):     # afiche la porte ouvert ou fermer
        screen.blit(self.image, (self.rect.x + self.game.camera_offset_x, self.rect.y))

    def open(self):     # permet d'ouvrir la porte
        self.closed = False
        self.image.fill(WHITE)


class menu:
    def __init__(self, Y):
        self.boutonimg = []
        self.image = pygame.image.load(f"VersionFinaleLeo/bouton/{Y}.png")
        self.image = pygame.transform.scale(self.image,(600,100))
        self.hovercColor = (100, 100, 100)
        self.spaceBetwen = (150 * Y) -1
        self.startPosition = [660,200+self.spaceBetwen]
        self.imageMenu = pygame.image.load("VersionFinaleLeo/back.png")  # REMETTRE "back.jpg" POUR LE FINAL
        self.rect = pygame.Rect((50, 150 + (100 * Y)),(600,100))

    def draw(self, screen):         # afiche les bouton
        screen.blit(self.image, (self.startPosition[0], self.startPosition[1]))

    def drawfont(self, win):        #afiche l'image de font
        win.blit(self.imageMenu, (0, 0))

    def detecteclick(self,pos):     # verifi si on clique sur un bouton et r'envoi vrais ou faux
        mouse = pygame.event.get()
        for event in mouse:
            if self.startPosition[0]<pos[0]<self.startPosition[0]+600 and self.startPosition[1]<pos[1]<self.startPosition[1]+100 and event.type == pygame.MOUSEBUTTONDOWN:
                return False
        return True

def detectQuit():       # permet de verifier si on veut fermer le jeu (pas sur d'etre encore utiliser)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    key = pygame.key.get_pressed()
    if key[pygame.K_ESCAPE]:
        exit()


class liane():
    def __init__(self,game, x,y):
        self.size = [50, 200]
        self.pos = [x,y]
        self.rect = pygame.Rect(self.pos, self.size)
        self.coordonate = [self.size, self.pos]
        self.game = game
        self.img = pygame.transform.scale(pygame.image.load("VersionFinaleLeo/lianes.png"),(50,200))

    def draw(self, screen):     # afiche la zone des liane
        pygame.draw.rect(screen, (0, 255, 0),(self.rect.x + self.game.camera_offset_x, self.rect.y, self.rect.w, self.rect.h))
        screen.blit(self.img,(self.pos[0] + self.game.camera_offset_x, self.pos[1], self.rect.w, self.rect.h))

    def getcoordonate(self):    # donne les coordoner de la zone des liane pour le player
        return self.coordonate


class tprect():
    def __init__(self, game):
        self.imgpr = pygame.image.load("VersionFinaleLeo/portail.png")
        self.imgpr = pygame.transform.scale(self.imgpr, (100, 100))
        self.imgpb = pygame.image.load("VersionFinaleLeo/portail bleu.png")
        self.imgpb = pygame.transform.scale(self.imgpb, (100, 100))
        self.postp = [10, 960]
        self.colortp = [90, 90, 255]
        self.sizetp = [40, 80]
        self.recttp = pygame.Rect(self.postp, self.sizetp)
        self.postarget = [10000, 960]
        self.colortarget = [255, 128, 0]
        self.sizetarget = [40, 80]
        self.recttarget = pygame.Rect(self.postarget, self.sizetarget)
        self.tptargetpos = [self.postp, self.postarget]
        self.game = game




    def draw(self, screen):         # afiche les zone de tp de depart et d'ariver
        screen.blit(self.imgpb,(self.recttp[0] + self.game.camera_offset_x, self.recttp[1], self.recttp.w, self.recttp.h))
        screen.blit(self.imgpr,(self.recttarget[0] + self.game.camera_offset_x, self.recttarget[1], self.recttarget.w, self.recttarget.h))

    def getpostp(self):         # renvoi les coordoner d'ariver de la teleportation
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
        self.rectbox.x = 140
        self.rectbox.y = 100
        self.posbox_x = p_x - 20
        self.posbox_y = p_y + 30

        self.spikedomage = pygame.Surface((100, 80))
        self.spikedomage.fill(PURPEL)
        self.rectdomage = self.spike.get_rect()
        self.rectdomage.x = 100
        self.rectdomage.y = 80
        self.posdomage_x = p_x-20
        self.posdomage_y = p_y +30

        self.delaiactif = 15
        self.delaidesactive = 20
        self.timer = 0
        self.activat =False
        self.activattimer = False
        self.destroy = False
        self.game = game
        self.image = []
        self.imagenumber = 0
        self.imgpic = pygame.image.load("VersionFinaleLeo/pic.png")
        self.imgpic = pygame.transform.scale(self.imgpic,(100,20))
        self.imgbase = pygame.image.load("VersionFinaleLeo/base.png")
        self.imgbase = pygame.transform.scale(self.imgbase, (100, 60))

        self.chutepicspeed = 4
        self.comptpic = 0
        self.chuty = self.pos_y


    def draw(self,screen): # afiche la base du piege est la zone de colisiont puis les pique si il est activer
        screen.blit(self.spike,(self.pos_x + self.game.camera_offset_x,self.pos_y))
        screen.blit(self.spikebox, (self.posbox_x + self.game.camera_offset_x, self.posbox_y))
        if self.activat :
            screen.blit(self.spikedomage,(self.posdomage_x+20 + self.game.camera_offset_x,self.posdomage_y))
        screen.blit(self.imgpic, (self.posdomage_x + 20 + self.game.camera_offset_x, self.chuty+20))
        screen.blit(self.imgbase, (self.pos_x + self.game.camera_offset_x, self.pos_y-30))



    def update(self,coordonate):
        x = coordonate[0]
        y = coordonate[1]
        if not self.destroy and self.activat ==False :          # desactive l'activation si le piege est desactiver
            if self.posbox_x<x<self.posbox_x+self.rectbox.x and self.posbox_y<y<self.posbox_y+self.rectbox.y or \
                    self.posbox_x<x+40<self.posbox_x+self.rectbox.x and self.posbox_y<y+80<self.posbox_y+self.rectbox.y:
                self.activattimer=True

        if self.activat == True :
            self.chuty += self.chutepicspeed
            self.comptpic +=1
            if self.comptpic >= 60 :
                self.comptpic =0
                self.chuty = self.pos_y
            if self.chuty>1060 :
                pass



        if self.destroy :                   # permet de desactiver le piege temporairement
            self.timer += 1
            if self.timer == 250:
                self.timer = 0
                self.destroy=False

        if self.activattimer == True :       # active le piege avec un cour delais est afiche les pique
            self.timer +=1
            if self.timer >= 20 :
                self.activat = True
            if self.timer>=80 :
                self.activattimer =False
                self.activat=False
                self.destroy =True

        if self.activat and self.posdomage_x<x<self.posdomage_x+self.rectdomage.x and self.posdomage_y<y<self.posdomage_y +self.rectdomage.y or\
                self.activat and self.posdomage_x < x+40 < self.posdomage_x + self.rectdomage.x and self.posdomage_y < y+80 < self.posdomage_y + self.rectdomage.y :
            return True                      # si le joeur est toucher il prend des dega

class boul():       # piege de boule qui tombe est roule pour ecraser le joeur
    def __init__(self,x,y,d,game):
        self.image = pygame.image.load('boule.png')
        self.image = pygame.transform.scale(self.image, (160, 160))
        self.rect = self.image.get_rect()
        self.rect.x = 160
        self.rect.y = 160
        self.posx = x
        self.posy = y

        self.colisionactive = pygame.Surface((20, 300))
        self.colisionactive.fill(RED)
        self.rectcol = (BROWN)
        self.rectpx = 20
        self.rectpy = 300
        self.posax = self.posx +250
        self.posay = self.posy +300

        self.active = False
        self.chute = False
        self.destroiy = False
        self.speed = 0.35
        self.timedrop = 0.5
        self.compteur = 0
        self.rotation = 1
        self.distance = d
        self.game = game

    def draw(self,screen):                  # permet d'afiquer la boule et la zone d'activation pour les test
        screen.blit(self.colisionactive,(self.posax+ self.game.camera_offset_x,self.posay))
        if self.destroiy == False and self.chute==True or self.destroiy == False and self.active==True:
            screen.blit(self.image,(self.posx+ self.game.camera_offset_x,self.posy))

    def update(self,coordonate,dt):         # met a jour tout les parametre du piege
        x = coordonate[0]
        y = coordonate[1]
        self.move(dt)
        self.colideactive(x,y)
        dega = self.colidedomage(x,y)
        return dega

    def colideactive(self,x,y):             # verifi si le player est dans la zone d'activation du piege
        if self.posax < x < self.posax + self.rectpx and self.posay < y < self.posay + self.rectpy or \
                self.posax < x + 110 < self.posax + self.rectpx and self.posay < y + 110 < self.posay + self.rectpy:
            self.chute = True

    def colidedomage(self,x,y):             # verifit si le player et toucher
        if self.posx<x<self.posx+self.rect.x and self.posy<y<self.posy +self.rect.y or \
                self.posx < x+110 < self.posx + self.rect.x and self.posy < y+110 < self.posy + self.rect.y:
            return False
        else :
            return  True
    def move(self,dt):

        if self.chute == True :                     # fait tomber la boule
            self.compteur += 1
            self.posy += self.timedrop * dt
        if self.compteur >= 57:                     # permet de controlé la dure de la chute et activer l'vencer a la fin
            self.chute = False
            self.active = True
        if self.active == True and self.distance>0: # active l'avencer de la boule
            self.posx+=self.speed *dt
            self.distance -= self.speed *dt
        if self.posy+160>1060-110:                  # enpeche la boule de fusioner ou passer en dessou du sol
            self.posy = 1060-160
            self.chute = False
            self.active = True

class decord(pygame.sprite.Sprite):
    def __init__(self,x,y,num,game):
        super().__init__()
        self.image= pygame.transform.scale(pygame.image.load(f"VersionFinaleLeo/Environnement/{num}.png"),(80,80))
        self.posx = -180+(80*x)
        self.posy = -240+(80*y)
        self.game= game
    def draw(self,screen):
        screen.blit(self.image,(self.posx+self.game.camera_offset_x,self.posy))

class imgfond2(pygame.sprite.Sprite):
    def __init__(self,game,ran,i):
        super().__init__()
        self.x = (-180)+(26*90*i)
        self.y = 1.6*90
        self.ibf = pygame.image.load(f"VersionFinaleLeo/f{ran}.png")
        self.ibf = pygame.transform.scale(self.ibf, (30 * 80, 9.5 * 80))
        self.game = game
    def draw(self,screen):
        screen.blit(self.ibf,(self.x+self.game.camera_offset_x,self.y))

