import pygame
from math import *

pygame.init()
window = pygame.display.set_mode((1600, 900))
clock = pygame.time.Clock()

rect = pygame.Rect(0, 0, 20, 20)
rect.center = window.get_rect().center
vel = 5

run = True

def NormalizeQuiMarche(vector):

    length = sqrt(vector.x * vector.x + vector.y * vector.y)
    vector.x /= length
    vector.y /= length
    return vector

while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    
    v = pygame.Vector2()
    if v.x != 0 or v.y != 0 :
        NormalizeQuiMarche(v)
    
    v.x =  (keys[pygame.K_d] - keys[pygame.K_q]) * vel 
    v.y =  (keys[pygame.K_s] - keys[pygame.K_z]) * vel 
    
    rect.x += v.x
    rect.y += v.y
        
    rect.centerx = rect.centerx % window.get_width()
    rect.centery = rect.centery % window.get_height()

    window.fill(0)
    pygame.draw.rect(window, (255, 0, 0), rect)
    pygame.display.flip()

pygame.quit()
exit()