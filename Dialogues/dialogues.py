import pygame

# BASE DIALOGUE, JUSTE POUR TESTER.

pygame.init()
screen = pygame.display.set_mode((1600, 900))
clock = pygame.time.Clock()
temp_img = 0

background = pygame.image.load('IMAGES/fond entier 1.png')

loraCrous = pygame.image.load('Dialogues/LoraCrousG.png').convert_alpha()
loraCrous = pygame.transform.scale(loraCrous, (90, 130))
daffyDoc = pygame.image.load('Dialogues/DaffyDocD.png').convert_alpha()
daffyDoc = pygame.transform.scale(daffyDoc, (80, 130))

bubblespeechDoc = pygame.image.load('Dialogues/DaffyDoc.png').convert_alpha()
bubblespeechDoc = pygame.transform.scale(bubblespeechDoc, (200, 120))

bubblespeechLora = pygame.image.load('Dialogues/LoraCrous.png').convert_alpha()
bubblespeechLora = pygame.transform.scale(bubblespeechLora, (200, 120))

while True:
    start = pygame.time.get_ticks()
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    screen.blit(loraCrous, (700, 710))
    screen.blit(daffyDoc, (1000, 710))

    if temp_img <= 0:
        imageVisible = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            temp_img = 3
            if event.key == pygame.K_a:
                    imageVisible = True

    if imageVisible:
        screen.blit(bubblespeechLora, (550, 580))
        temp_img -= dt

    dt = (pygame.time.get_ticks() - start) / 1000

    pygame.display.flip()

    pygame.display.update()