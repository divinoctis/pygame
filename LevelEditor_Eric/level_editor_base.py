import pygame
import button
import csv
import pickle

pygame.init()

clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
LOWER_MARGIN = 100
SIDE_MARGIN = 300


screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption('Level Editor')

ROWS = 16
MAX_COLS = 175
TILE_SIZE = SCREEN_HEIGHT // ROWS
SELECTED_TILE_SIZE = TILE_SIZE // 3

TILE_TYPES = 232 # nombre à changer en fonction du nombre de pièces environnement (+1 vu que ça part de 0)
level = 0
current_tile = 0
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 4

mountain_img = pygame.image.load('LevelEditor_Eric/decor/Montagnes.png').convert_alpha()
mountain_img = pygame.transform.scale(mountain_img, (800,500))
sky_img = pygame.image.load('LevelEditor_Eric/decor/Ciel.png').convert_alpha()
fondTemple = pygame.image.load('LevelEditor_Eric/decor/fondTemple.png').convert_alpha() # Leo, ici c'est l'image de fond du temple, si tu peux améliorer pour que ce soit nickel sur le level editor, fais le. La ligne du dessous permet de redimensionner
fondTemple = pygame.transform.scale(fondTemple, (1400, 400)) # check LIGNE 75 pour modifier la hauteur du fond

img_list = []
for x in range(TILE_TYPES):
	img = pygame.image.load(f'Assets/Environnement/{x}.png').convert_alpha()
	img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
	img_list.append(img)

img_list_copy = [pygame.transform.scale(img, (SELECTED_TILE_SIZE, SELECTED_TILE_SIZE)) for img in img_list]

save_img = pygame.image.load('LevelEditor_Eric/decor/save_btn.png').convert_alpha()
load_img = pygame.image.load('LevelEditor_Eric/decor/load_btn.png').convert_alpha()

OLIVE = (155, 154, 90)
WHITE = (255, 255, 255)
DARKOLIVE = (85,107,47)

font = pygame.font.SysFont('Futura', 30)

world_data = []
for row in range(ROWS):
	r = [-1] * MAX_COLS
	world_data.append(r)

for tile in range(0, MAX_COLS):
	world_data[ROWS - 1][tile] = 0

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

def draw_bg():
	screen.fill(OLIVE)
	width = sky_img.get_width() 
	width2 = mountain_img.get_width()
	for x in range((SCREEN_WIDTH + SIDE_MARGIN) // width2 + 1):
		screen.blit(sky_img, ((x * width) - scroll * 0.5, 0))
		screen.blit(mountain_img, ((x-1) * width2, SCREEN_HEIGHT - mountain_img.get_height() - 30))
		screen.blit(fondTemple, ((x-1) * width2, SCREEN_HEIGHT - fondTemple.get_height() - 30))

def draw_grid():

	for c in range(MAX_COLS + 1):
		pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, SCREEN_HEIGHT))

	for c in range(ROWS + 1):
		pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))

def draw_world():
	for y, row in enumerate(world_data):
		for x, tile in enumerate(row):
			if tile >= 0:
				screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))

save_button = button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 50, save_img, 1)
load_button = button.Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 50, load_img, 1)

button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
	tile_button = button.Button(SCREEN_WIDTH + (25 * button_col) + 50, 25 * button_row + 50, img_list_copy[i], 1)
	button_list.append(tile_button)
	button_col += 1
	if button_col == 10:
		button_row += 1
		button_col = 0

run = True
while run:

	clock.tick(FPS)

	draw_bg()
	draw_grid()
	draw_world()

	draw_text(f'Level: {level}', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
	draw_text('Press UP or DOWN to change level', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 60)

	if save_button.draw(screen):

		with open(f'level{level}_data.csv', 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter = ',')
			for row in world_data:
				writer.writerow(row)

	if load_button.draw(screen):

		scroll = 0
		with open(f'level{level}_data.csv', newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter = ',')
			for x, row in enumerate(reader):
				for y, tile in enumerate(row):
					world_data[x][y] = int(tile)

	pygame.draw.rect(screen, OLIVE, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))


	button_count = 0
	for button_count, i in enumerate(button_list):
		if i.draw(screen):
			current_tile = button_count

	pygame.draw.rect(screen, DARKOLIVE, button_list[current_tile].rect, 3)


	if scroll_left == True and scroll > 0:
		scroll -= 5 * scroll_speed
	if scroll_right == True and scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
		scroll += 5 * scroll_speed

	pos = pygame.mouse.get_pos()
	x = (pos[0] + scroll) // TILE_SIZE
	y = pos[1] // TILE_SIZE

	if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:

		if pygame.mouse.get_pressed()[0] == 1:
			if world_data[y][x] != current_tile:
				world_data[y][x] = current_tile
		if pygame.mouse.get_pressed()[2] == 1:
			world_data[y][x] = -1

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				level += 1
			if event.key == pygame.K_DOWN and level > 0:
				level -= 1
			if event.key == pygame.K_LEFT:
				scroll_left = True
			if event.key == pygame.K_RIGHT:
				scroll_right = True
			if event.key == pygame.K_RSHIFT:
				scroll_speed = 5

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				scroll_left = False
			if event.key == pygame.K_RIGHT:
				scroll_right = False
			if event.key == pygame.K_RSHIFT:
				scroll_speed = 1

	pygame.display.update()

pygame.quit()