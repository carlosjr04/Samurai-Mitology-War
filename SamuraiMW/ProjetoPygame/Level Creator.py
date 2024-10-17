from typing import List

import pygame
import button
import csv


pygame.init()

clock = pygame.time.Clock()
FPS = 60

#janela
screen_width = 1000
screen_height = 600
LOWER_MARGIN = 100
SIDE_MARGIN = 300

screen = pygame.display.set_mode((screen_width+SIDE_MARGIN , screen_height + LOWER_MARGIN))
pygame.display.set_caption('Level Creator')


#definir variáveis do jogo
level=0
linhas = 16
MAX_COLUNAS = 150
TILE_SIZE = screen_height // linhas
TILE_TYPES = 20
current_tile = 0
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1





#load images
cidade1_img = pygame.image.load('cenario/cidade1.jpg').convert_alpha()
cidade2_img = pygame.image.load('cenario/cidade2.jpg').convert_alpha()
floresta_img = pygame.image.load('cenario/floresta.png').convert_alpha()
caverna_img = pygame.image.load('cenario/caverna.png').convert_alpha()
chao_img = pygame.image.load('cenario/chao.jpg').convert_alpha()

#store tiles em uma lista
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'cenarios/{x}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

#botao de salvar
save_img = pygame.image.load(f'Button/save.png')
load_img = pygame.image.load(f'Button/load.png')
#cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (144, 201, 120)
RED = (200, 25, 25)

font = pygame.font.SysFont('Futura',30)
#criar uma lista vazia que possui toda informaçao da fase
world_data=[]

for row in range(linhas):
    r = [-1] * MAX_COLUNAS
    world_data.append(r)
#criar chao

for tile in range(0,MAX_COLUNAS):
    world_data[linhas-3][tile] = 4
    world_data[linhas - 2][tile] = 5
    world_data[linhas - 1][tile] = 5


def draw_text(text,font,text_col,x,y):
    img = font.render(text,True,text_col)
    screen.blit(img,(x,y))


#função para desenhar o fundo
def draw_bg():
    screen.fill(GREEN)
    width = cidade2_img.get_width()
    if level==0:
        x=0
        for y in range(4):
            screen.blit(cidade1_img, (((x+y) * width) - scroll * 0.5, 0))
            x+=1
            screen.blit(cidade2_img, (((x+y) * width) - scroll * 0.5, 0))
    elif level==1:
        for x in range(3):
            screen.blit(floresta_img, ((x * width) - scroll * 0.5, 0))
    elif level==2:
        for x in range(2):
            screen.blit(caverna_img, ((x * width) - scroll * 0.5, 0))
    elif level==3:
        for x in range(3):
            screen.blit(floresta_img, ((x * width) - scroll * 0.5, 0))


#draw grid
def draw_grid():
    #linhas verticais
    for c in range(MAX_COLUNAS + 1):
        pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, screen_height))

    #linhas horizontais
    for l in range(linhas + 1):
        pygame.draw.line(screen, WHITE, (0, l * TILE_SIZE), (screen_width, l * TILE_SIZE))


#funçao para desenhar os blocos
def draw_world():
    for y,row in enumerate(world_data):
        for x,tile in enumerate(row):
            if tile >=0:
                screen.blit(img_list[tile],(x * TILE_SIZE - scroll,  y * TILE_SIZE))


save_button = button.Button(screen_width//2,screen_height+ LOWER_MARGIN - 50,save_img,1)
load_button = button.Button(screen_width//2 +200 ,screen_height+ LOWER_MARGIN - 50,load_img,1)

button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
    tile_button = button.Button(screen_width + (75 * button_col) + 50, 75 * button_row + 50, img_list[i],1)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
        button_row += 1
        button_col = 0

run = True
while run:

    clock.tick(FPS)

    draw_bg()
    draw_world()
    draw_grid()
    draw_text(f'level:{level}',font,WHITE,10,screen_height+LOWER_MARGIN-90)
    draw_text(f'Aperte UP ou DOWN para mudar de nivel:{level}',font,WHITE,10,screen_height+LOWER_MARGIN-60)


    #save e load
    if save_button.draw(screen):
        # save level data
        with open(f'level{level}_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for row in world_data:
                writer.writerow(row)


    if load_button.draw(screen):
        #carregar o level
        scroll = 0
        with open(f'level{level}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for x,row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] =int(tile)



    pygame.draw.rect(screen,GREEN,(screen_width, 0, SIDE_MARGIN, screen_height))
    button_count = 0
    for button_count,i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count
    pygame.draw.rect(screen,RED, button_list[current_tile].rect, 3)



    #scroll the MAP
    if scroll_left == True and scroll > 0:
        scroll -= 5 * scroll_speed
    if scroll_right == True and scroll < (MAX_COLUNAS * TILE_SIZE)-screen_width:
        scroll += 5 * scroll_speed

    #adicionar blocos no mapa
    pos = pygame.mouse.get_pos()
    print(pos)
    x = ((pos[0]+ scroll) // TILE_SIZE)
    y = pos[1] // TILE_SIZE
    #CHECAR SE O MOUSE TA NO MAPA
    if pos[0] < screen_width and pos[1] < screen_height:
        if pygame.mouse.get_pressed()[0] == 1:
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile

        if pygame.mouse.get_pressed()[2]==1:
            world_data[y][x] = -1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        #botao pressionado
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_UP:
                level+=1
            if event.key == pygame.K_DOWN and level>0:
                level-=1
            if event.key == pygame.K_a:
                scroll_left = True
            if event.key == pygame.K_d:
                scroll_right = True
            if event.key == pygame.K_LSHIFT:
                scroll_speed = 5

        #botao solto
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                scroll_left = False
            if event.key == pygame.K_d:
                scroll_right = False
            if event.key == pygame.K_LSHIFT:
                scroll_speed = 1

    pygame.display.update()

pygame.quit()