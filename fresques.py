import pygame as py

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 0
        self.gravity = 4
        self.jumped = False

    def move(self, keys):
        if keys[py.K_d]:
            self.x += 5
        if keys[py.K_q]:
            self.x -= 5
        if keys[py.K_z] and self.y == 7900:
            self.speed = -80
            self.jumped = True

    def update_position(self):
        self.y += self.speed
        self.speed += self.gravity

        if self.y > 7900:
            self.y = 7900
            self.speed = 0
            self.jumped = False

class Game:
    def __init__(self):
        py.init()
        self.window_size = [1600, 900]
        self.clock = py.time.Clock()
        self.screen = py.display.set_mode(self.window_size)
        self.background = py.image.load("caveBG.png").convert()
        self.background = py.transform.scale(self.background, (1600, 900))
        self.player = Player(30, 7900)

    def draw_blocks(self, blockPosition):
        for pos in blockPosition:
            py.draw.rect(self.screen, (255, 0, 0), pos)

    def run(self):
        finished = False
        blockPosition = [[290, 400, 250, 400], [690, 400, 250, 400], [1090, 400, 250, 400]]

        while not finished:
            self.screen.blit(self.background, (0, 0))
            keys = py.key.get_pressed()
            self.player.move(keys)
            self.player.update_position()

            self.draw_blocks(blockPosition)

            py.draw.circle(self.screen, (0, 0, 0), (self.player.x, int(self.player.y / 10)), 10)
            py.draw.rect(self.screen, (0, 0, 0), [0, 800, self.window_size[0], 100])
            py.display.flip()
            self.clock.tick(60)

            for event in py.event.get():
                if event.type == py.QUIT:
                    finished = True

        py.quit()

if __name__ == "__main__":
    game = Game()
    game.run()