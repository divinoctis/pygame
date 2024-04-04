import pygame as py

WIDTH = 1600
HEIGHT = 900
BACKGROUND = (0, 128, 0)
py.display.set_caption("GEODYSSEY")

class Sprite(py.sprite.Sprite):
    def __init__(self, image, startx, starty):
        super().__init__()
        self.image = py.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = [startx, starty]

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Ground(Sprite):
    def __init__(self, startx, starty):
        super().__init__("ground.jpg", startx, starty)

class Player(Sprite):
    def __init__(self, startx, starty):
        super().__init__("circle.png", startx, starty)
        self.image = py.transform.scale(self.image, (1500, 1500))
        self.speed = 5
        self.jump = 10
        self.verticalSpeed = 0
        self.gravity = 1

    def update(self, ground):
        horizontalSpeed = 0
        onGround = self.checkCollision(0, 1, ground)

        key = py.key.get_pressed()
        if key[py.K_q]:
            horizontalSpeed = -self.speed
        elif key[py.K_d]:
            horizontalSpeed = self.speed

        if key[py.K_z] and onGround:
            self.verticalSpeed = -self.jump

        if self.verticalSpeed < 10 and not onGround:
            self.verticalSpeed += self.gravity
        
        if self.verticalSpeed > 0 and onGround:
            self.verticalSpeed = 0
        
        self.move(horizontalSpeed, self.verticalSpeed, ground)

    def move(self, x, y, boxes):
        directionX = x
        directionY = y

        while self.checkCollision(0, directionY, boxes):
            directionY -= 1

        while self.checkCollision(directionX, directionY, boxes):
            directionX -= directionX / abs(directionX)
        
        self.rect.move_ip([directionX, directionY])

    def checkCollision(self, x, y, boxes):
        self.rect.move_ip([x, y])
        collide = py.sprite.spritecollideany(self, boxes)
        self.rect.move_ip([-x, -y])
        return collide
    
def main():
    run = True
    py.init()
    screen = py.display.set_mode((WIDTH, HEIGHT))
    clock = py.time.Clock()
    player = Player(100, 200)
    ground = py.sprite.Group()

    for bx in range(0, 800, 32):
        ground.add(Ground(bx, 1100))

    while run:
        py.event.pump()
        player.update(ground)

        for event in py.event.get():
            if event.type == py.QUIT:
                run = False

        screen.fill(BACKGROUND)
        player.draw(screen)
        ground.draw(screen)
        py.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()