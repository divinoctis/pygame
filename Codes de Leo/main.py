import pygame
import random
import sys
from class_game import*

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("GEODYSSEY")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
buttons = pygame.sprite.Group()

ground = Platform(0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20)
all_sprites.add(ground)
platforms.add(ground)

button = Button(450, SCREEN_HEIGHT - 250)
all_sprites.add(button)
buttons.add(button)

door = Door(750, SCREEN_HEIGHT - 120)
all_sprites.add(door)

player = Player(50, SCREEN_HEIGHT - 50,)
all_sprites.add(player)

windowSize = [800, 600]
camera_offset_x = 0
camera = Camera(windowSize[0], windowSize[1])

startMenu = True

FPS = 60
dtTarget = 1000/FPS
dt = 0

menuinstance = menu(0)
imagemenu = pygame.image.load("IMAGES\BG.png") #REMETTRE "back.jpg" POUR LE FINAL
menuB0 = menu(0)
sizefont = 24

for i in range(4):
    platform = Platform(50 + i * 100, SCREEN_HEIGHT - 100 - i * 50, 100, 20)
    all_sprites.add(platform)
    platforms.add(platform)

while 1:
    #menu
    while startMenu :
        screen.blit(menuinstance.imageMenu, (0, 0))
        detectQuit()
        menuinstance.drawfont(screen)
        menuB0.startmenu(screen,sizefont)
        startmenu([[pos[0] + camera.camera_offset_x, pos[1], pos[2], pos[3]] for pos in blockPosition]) #### à modifer jsp

        pos = pygame.mouse.get_pos()
        if menuB0.is_hover(pos):
            menuB0.color = menuB0.hovercColor
            for evenement in pygame.event.get():
                if evenement.type == pygame.MOUSEBUTTONDOWN:
                    menuB0.click()
                    startMenu = False
        else:
            menuB0.color = (175,175,175,0)
        pygame.display.flip()

    detectQuit()

    #game loop
    TickStart = pygame.time.get_ticks()

    screen.fill(BLACK)

    #event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump_action()

    hits = pygame.sprite.spritecollide(player, buttons, False)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        player.jump_action()

    if hits:
        button.activate()
        door.open()

    #update
    player.update(platforms)

    camera_offset_x = SCREEN_WIDTH // 2 - player.rect.x - player.rect.width // 2

    # draw

    screen.fill(BLACK)
    all_sprites.draw(screen)

    pygame.display.flip()

    TickEnd = pygame.time.get_ticks()
    dt = TickEnd - TickStart
    if (dt< dtTarget):
        pygame.time.wait(int(dtTarget - dt))
        dt = dtTarget

