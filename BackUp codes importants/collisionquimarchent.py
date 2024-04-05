# CODE POUR TESTER LES COLLISIONS.

import pygame
import sys

class makeForm:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

class Game:
    def __init__(self):
        pygame.init()

        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 600
        self.window = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.rect1 = makeForm(100, 100, 50, 50, self.RED)
        self.rect2 = makeForm(200, 200, 50, 50, self.GREEN)

    def closeWindow(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def run(self):
        running = True

        while running:
            self.closeWindow()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.rect1.rect.x -= 1
                if self.rect1.rect.colliderect(self.rect2.rect):
                    self.rect1.rect.x += 1
            if keys[pygame.K_RIGHT]:
                self.rect1.rect.x += 1
                if self.rect1.rect.colliderect(self.rect2.rect):
                    self.rect1.rect.x -= 1
            if keys[pygame.K_UP]:
                self.rect1.rect.y -= 1
                if self.rect1.rect.colliderect(self.rect2.rect):
                    self.rect1.rect.y += 1
            if keys[pygame.K_DOWN]:
                self.rect1.rect.y += 1
                if self.rect1.rect.colliderect(self.rect2.rect):
                    self.rect1.rect.y -= 1

            self.window.fill(self.WHITE)
            self.rect1.draw(self.window)
            self.rect2.draw(self.window)
            pygame.display.flip()
            pygame.time.Clock().tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()