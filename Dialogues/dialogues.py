import pygame

# BASE DIALOGUE, JUSTE POUR TESTER.

pygame.init()
screen = pygame.display.set_mode((1600, 900))
clock = pygame.time.Clock()

box = pygame.Rect(300, 200, 100, 100)
player = pygame.Rect(50, 50, 30, 30)

font = pygame.font.Font("Dialogues/04b_25__.ttf", 15)
texts = ['LORA CROUS: Avec mon tombe radar, impossible de louper le tresor !', 'DAFFY DOC: La route ? La ou on va, on n’a pas besoin de route !']
text_renders = [font.render(text, True, (255, 255, 255)) for text in texts]
index = -1
a_released = True

while True:
    clock.tick(60)
    screen.fill((0, 0, 0))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        player.x -= 3
    if keys[pygame.K_d]:
        player.x += 3
    if keys[pygame.K_s]:
        player.y += 3
    if keys[pygame.K_z]:
        player.y -= 3

    pygame.draw.rect(screen, (0, 255, 0), box, width=2)
    pygame.draw.rect(screen, (255, 0, 0), player)

    if player.colliderect(box):
        if keys[pygame.K_a] and a_released:
            a_released = False
            index = (index + 1) if (index + 1) != len(text_renders) else 0
        elif not keys[pygame.K_a]:
            a_released = True
    else:
        index = -1

    if index != -1:
        screen.blit(text_renders[index], (50, 50))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    pygame.display.update()