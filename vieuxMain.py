import pygame
import time
import random

pygame.init()

# fenêtre de base
screen = pygame.display.set_mode((1600, 900))
image = pygame.image.load("C:\\Users\\mdubos\\Downloads\\square.png")
image = pygame.transform.scale(image, (60, 60))
x = 200
y = 800
velocity = 50
run = True
color = (255,0,0)

while run :
    screen.fill((0, 0, 0))
    screen.blit(image, (x, y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # event pour fermer la fenêtre
            run = False
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:    # event pour déplacer l'image
            if event.key == pygame.K_q:
                x -= velocity

            if event.key == pygame.K_d:
                x += velocity

            if event.key == pygame.K_z:
                y -= velocity

            if event.key == pygame.K_s:
                y += velocity

        pygame.display.update()

        pygame.draw.rect(screen, color, pygame.Rect(30, 30, 60, 60))
        pygame.display.flip()

pygame.quit()