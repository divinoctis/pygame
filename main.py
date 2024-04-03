import pygame as py

class Player:
    def __init__(self):
        self.vel = 5
        self.color = (255, 0, 0)
        self.rect = py.Rect(30, 30, 60, 60)
        self.rect.center = (800, 450)

    def update(self):
        # à faire
        pass

    def draw(self, screen):
        py.draw.rect(screen, self.color, self.rect)

    def playerMovement(self, screen):
        self.keys = py.key.get_pressed()
        self.rect.x += (self.keys[py.K_d] - self.keys[py.K_q]) * self.vel
        self.rect.y += (self.keys[py.K_s] - self.keys[py.K_z]) * self.vel
        self.rect.centerx = self.rect.centerx % screen.get_width()
        self.rect.centery = self.rect.centery % screen.get_height()

class Surface:
    def __init__(self):
        self.ground = py.image.load("ground.png")
        self.ground = py.transform.scale(self.ground, (1600, 200))
    
    def draw(self, screen):
        screen.blit(self.ground, (0, screen.get_height() - self.ground.get_height()))

class Game:
    def __init__(self):
        py.init()
        self.clock = py.time.Clock()
        self.screen = py.display.set_mode((1600, 900))
        self.player = Player()
        self.surface = Surface()
        self.run = True

    def closeWindow(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                self.run = False

    def run_game(self):
        while self.run:
            self.screen.fill((0, 0, 0))
            self.closeWindow()
            self.surface.draw(self.screen)
            self.player.playerMovement(self.screen)
            self.player.update()
            self.player.draw(self.screen)
            py.display.flip()
            self.clock.tick(60)

        py.quit()

if __name__ == "__main__":
    game = Game()
    game.run_game()


# CHOSES A FAIRE :
# fonctions de collision pour le sol et les blocs
# fonction pour "grimper" sur des objets type liane
# fonction jump et rebond sur les murs