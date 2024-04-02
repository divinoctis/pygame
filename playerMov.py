import pygame

screen = pygame.display.set_mode((1600, 900))
clock = pygame.time.Clock()

class Player:

    def __init__(self):
        rect = pygame.Rect(0, 0, 20, 20)
        rect.center = screen.get_rect().center
        vel = 5
        keys = pygame.key.get_pressed()

    def playerMovement(self, direction):
        self.vx =  (direction.x * self.vel )
        self.vy =  (direction.y * self.vel )
        
        self.x += self.vx
        self.y += self.vy
            
        self.centerx = self.centerx % screen.get_width()
        self.centery = self.centery % screen.get_height()