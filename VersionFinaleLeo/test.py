import pygame

pygame.init()

win = pygame.display.set_mode((800,600))
color = (100,100,100)

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

class player (object):
    def __init__(self):
        self.player = pygame.rect.Rect((300,400,50,50))
        self.color = "white"

    def move(self,x_speed,y_speed):
        self.player.move_ip((x_speed,y_speed))

    def change_color(self,color):
        self.color=color

    def draw(self,game_screen):
        pygame.draw.rect(game_screen,self.color,self.player)

play= player()
play2 = player()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800,600))
color_list

while True :

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.JOYBUTTONDOWN:
            if pygame.joystick.Joystick(0).get_button(0):
                play.change_color("blue")
            if pygame.joystick.Joystick(0).get_button(1):
                play.change_color("red")
            if pygame.joystick.Joystick(0).get_button(2):
                play.change_color("yellow")
            if pygame.joystick.Joystick(0).get_button(3):
                play.change_color("green")

    x_speed = round(pygame.joystick.Joystick(0).get_axis(0))
    y_speed = round(pygame.joystick.Joystick(0).get_axis(1))
    play.move(x_speed, y_speed)
    x_speed = round(pygame.joystick.Joystick(0).get_axis(2))
    y_speed = round(pygame.joystick.Joystick(0).get_axis(3))
    play2.move(x_speed, y_speed)

    screen.fill((0,0,0))
    play.draw(screen)
    play2.draw(screen)
    pygame.display.update()
    clock.tick(180)


