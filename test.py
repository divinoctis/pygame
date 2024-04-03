import pygame as py

py.init()
windowSize = [800, 500]
clock = py.time.Clock()
screen = py.display.set_mode(windowSize)
white = py.color.Color('#FFFFFF')
black = py.color.Color('#000000')
jumped = False
x = 30
speed = 0
y = 4000
gravity = 2
finished = False

while not finished:
    screen.fill(white)
    keys = py.key.get_pressed()
    if keys[py.K_d]:
        x +=5
    if keys[py.K_q]:
        x -=5
    if keys[py.K_z] and y == 4000:
        speed = -100
    y += speed
    speed += gravity

    if y > 4000:
        y = 4000
        speed = 0
    py.draw.circle(screen, black, (x, int(y/10)), 10)
    py.draw.rect(screen, black, [0, 410, windowSize[0], 10])
    py.display.flip()
    clock.tick(50)

    for event in py.event.get():
        if event.type == py.QUIT:
            finished = True

py.quit()