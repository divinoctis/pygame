import pygame

screen = pygame.display.set_mode((1600, 900))
clock = pygame.time.Clock()
color = (255, 0, 0)

class Player:

    def __init__(self):
        self.vel = 5
        self.keys = pygame.key.get_pressed()

    def update(self):
        self.rect = pygame.draw.rect(screen, color, pygame.Rect(30, 30, 60, 60))
        self.rect.center = screen.get_rect().center

    def draw(self, screen):
        screen.blit(self.rect)

    def playerMovement(self, direction):
        self.vx =  (direction.x * self.vel )
        self.vy =  (direction.y * self.vel )

        self.x += self.vx
        self.y += self.vy
            
        self.centerx = self.centerx % screen.get_width()
        self.centery = self.centery % screen.get_height()