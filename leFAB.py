import pygame

WIDTH = 600
HEIGHT = 480
BACKGROUND = (0, 0, 0)
pygame.display.set_caption("HELL NAH BRUV")


class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, startx, starty):
        super().__init__()  # super() appelle le parent (ici pygame.sprite.Sprite). On peut aussi Ã©crire la ligne
        # pygame.sprite.Sprite.__init__()

        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()

        self.rect.center = [startx, starty]

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Sol(Sprite):
    def __init__(self, startx, starty):
        super().__init__("sol.png", startx, starty)


class Soul(Sprite):
    def __init__(self, startx, starty):
        super().__init__("soul.png", startx, starty)


class Score:

    def __init__(self):
        self.X = 0
        self.Y = 0
        self.__class__.score = 0
        self.font = pygame.font.Font('arial.ttf', 32)

    def update(self, Player, Soul):
        collision_sprite = pygame.sprite.spritecollideany(Player, Soul)
        if collision_sprite:
            Soul.remove(collision_sprite)
            self.__class__.score += 1

    def text(self, screen):
        text = self.font.render("Soul: " + str(self.__class__.score), True, (255, 255, 255))
        screen.blit(text, (10, 10))


class Player(Sprite):
    def __init__(self, startx, starty):
        super().__init__("miku idle1.png", startx, starty)  # super appelle Sprite

        self.speed = 5
        self.jumpForce = 10
        self.vsp = 0
        self.gravity = 1

    def update(self, sol):
        hsp = 0  #
        onground = self.check_collision(0, 1, sol)

        key = pygame.key.get_pressed()
        if key[pygame.K_q]:
            hsp = -self.speed
        elif key[pygame.K_d]:
            hsp = self.speed

        if key[pygame.K_z] and onground:
            self.vsp = -self.jumpForce

        if self.vsp < 10 and not onground:  # 9.8: rounded up
            self.vsp += self.gravity

            # stop falling when the ground is reached
        if self.vsp > 0 and onground:
            self.vsp = 0

        self.move(hsp, self.vsp, sol)

    def move(self, x, y, boxes):
        dx = x
        dy = y

        while self.check_collision(0, dy, boxes):
            dy -= 1

        while self.check_collision(dx, dy, boxes):
            dx -= dx / abs(dx)

        self.rect.move_ip([dx, dy])

    def check_collision(self, x, y, boxes):
        self.rect.move_ip([x, y])
        collide = pygame.sprite.spritecollideany(self, boxes)
        self.rect.move_ip([-x, -y])
        return collide


def main():
    running = True
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    player = Player(100, 200)

    score = Score()

    soul = pygame.sprite.Group()
    for i in range(0, 600, 100):
        soul.add(Soul(i, 268))

    sol = pygame.sprite.Group()
    for bx in range(0, 600, 32):
        sol.add(Sol(bx, 300))

    test = sol.add(Sol(500, 200))

    while running:
        pygame.event.pump()
        player.update(sol)
        score.update(player, soul)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw loop
        screen.fill(BACKGROUND)
        player.draw(screen)
        sol.draw(screen)
        soul.draw(screen)
        score.text(screen)
        pygame.display.update()

        clock.tick(60)


if __name__ == "__main__":
    main()