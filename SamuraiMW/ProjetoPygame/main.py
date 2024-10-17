import random

import pygame
from pygame import mixer
import os
import csv

import button

# inicializa o pygame
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
pygame.init()

# tamanho da tela e título
screen_width = 1200
screen_height = int(screen_width * 0.5)

icone = pygame.image.load('cenario/icon.jpg')  # Substitua pelo caminho do seu ícone
pygame.display.set_icon(icone)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Samurai_War_Mitology')

# musicas
andar_terra = pygame.mixer.Sound("musica/andar terra.mp3")
andar_terra.set_volume(0.04)

andar_pedra = pygame.mixer.Sound("musica/andar pedra.mp3")
andar_pedra.set_volume(0.05)

jogo_musica = pygame.mixer.Sound("musica/musica_jogo.wav")
jogo_musica.set_volume(0.09)

final_musica = pygame.mixer.Sound("musica/final.wav")
final_musica.set_volume(0.1)

menu_musica = pygame.mixer.Sound("musica/menu.mp3")
menu_musica.set_volume(0.2)

ataque_corvo = pygame.mixer.Sound("musica/ataque_corvo.mp3")
ataque_corvo.set_volume(0.2)

boss_figth = pygame.mixer.Sound("musica/boss figth.mp3")
boss_figth.set_volume(0.08)

comeco_batalha = pygame.mixer.Sound("musica/comeco batalha.mp3")
comeco_batalha.set_volume(0.5)

risada_boss = pygame.mixer.Sound("musica/morte personagem.mp3")
risada_boss.set_volume(0.3)

dano_boss = pygame.mixer.Sound("musica/dano boss.mp3")
dano_boss.set_volume(0.2)

ataque_fx = pygame.mixer.Sound("musica/ataque.mp3")
ataque_fx.set_volume(0.2)

machucado_fx = pygame.mixer.Sound("musica/machucado.mp3")
machucado_fx.set_volume(0.2)

monstro_fx = pygame.mixer.Sound("musica/monstro.mp3")
monstro_fx.set_volume(0.2)

pulo_fx = pygame.mixer.Sound("musica/pulo.mp3")
pulo_fx.set_volume(0.2)

morte_fx = pygame.mixer.Sound("musica/morte.mp3")
morte_fx.set_volume(0.2)

morteH_fx = pygame.mixer.Sound("musica/morte humano.mp3")
morteH_fx.set_volume(0.2)

especial_solto_fx = pygame.mixer.Sound("musica/epsecial lancado.mp3")
especial_solto_fx.set_volume(0.1)

com_especial_fx = pygame.mixer.Sound("musica/esta com especial.mp3")
com_especial_fx.set_volume(0.4)

pegando_especial_fx = pygame.mixer.Sound("musica/pegando especial.mp3")
pegando_especial_fx.set_volume(0.2)

pegando_vida_fx = pygame.mixer.Sound("musica/pegando vida.mp3")
pegando_vida_fx.set_volume(0.2)

# framerate
clock = pygame.time.Clock()
FPS = 60

# variaveis
gravidade = 0.75
scroll_thresh = 500
level = 0
MAX_LEVELS = 3
rows = 16
cols = 150
start_game = False
final = False
start_intor = False

TILE_SIZE = screen_height // rows
TILE_TYPES = 20
screen_scroll = 0
bg_scroll = 0

# definir as variáves de movimentação do player
moving_left = False
moving_right = False
shoot = False
ataque = False

# load images
cidade1_img = pygame.image.load('cenario/cidade1.jpg').convert_alpha()
cidade2_img = pygame.image.load('cenario/cidade2.jpg').convert_alpha()
floresta_img = pygame.image.load('cenario/floresta.png').convert_alpha()
caverna_img = pygame.image.load('cenario/caverna.png').convert_alpha()
flecha_img = pygame.image.load("flecha/Arrow.png").convert_alpha()
especial_img = pygame.image.load("flecha/vento.png").convert_alpha()
corvo_img = pygame.image.load("flecha/corvo.png").convert_alpha()
fundo_img = pygame.image.load("cenario/dojoo (1).jpg").convert_alpha()
morte_personagem = pygame.image.load("cenario/oioi.png").convert_alpha()
tela_fadein = pygame.image.load("cenario/tela-preta (1).png")
# load os chaos
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'cenarios/{x}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

espada_img = pygame.image.load('katanas.png').convert_alpha()

recurso_vida_img = pygame.image.load('recursos/vida.png').convert_alpha()
recurso_especial_img = pygame.image.load('recursos/especial.png').convert_alpha()

recursos = {
    'curar': recurso_vida_img,
    'especial': recurso_especial_img
}

# fundo
BG = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# define font
font = pygame.font.SysFont('Futura', 30)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# função para resetar o level
def reset_level():
    enemy_group.empty()
    esqueleto_group.empty()
    anciao_group.empty()
    espada_group.empty()
    recursos_group.empty()
    decoracao_group.empty()
    water_group.empty()
    exit_group.empty()
    chefe_group.empty()
    flecha_group.empty()
    corvo_group.empty()
    # create empty tile list
    data = []
    for row in range(rows):
        r = [-1] * cols
        data.append(r)

    return data


def draw_fundo():
    screen.fill(GREEN)
    width = cidade2_img.get_width()
    if level == 0:
        x = 0
        for y in range(4):
            screen.blit(cidade1_img, (((x + y) * width) - bg_scroll * 0.5, 0))
            x += 1
            screen.blit(cidade2_img, (((x + y) * width) - bg_scroll * 0.5, 0))
    elif level == 1:
        for x in range(4):
            screen.blit(floresta_img, ((x * width) - bg_scroll * 0.5, 0))
    elif level == 2:
        for x in range(2):
            screen.blit(caverna_img, ((x * width) - bg_scroll * 0.5, 0))
    elif level == 3:
        for x in range(3):
            screen.blit(floresta_img, ((x * width) - bg_scroll * 0.5, 0))


# classe boss

class boss(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, escala, vel):
        pygame.sprite.Sprite.__init__(self)
        self.vision = pygame.Rect(0, 0, 100, 20)
        self.ataque = pygame.Rect(0, 0, 60, 20)
        self.vivo = True
        self.spawn = False
        self.spawner = 0
        self.char_type = char_type
        self.vel = vel
        self.atacar_cooldown = 0
        self.vida = 500
        self.vida_max = self.vida
        self.vida_max = self.vida
        self.direcao = -1
        self.virar = True
        self.move_counter = 0
        self.move_cooldown = 1000
        self.shoot_cooldown = 100

        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        # animaçao

        animation_type = ['parado', 'andar', 'pulo', 'ataque', 'morte']
        for animation in animation_type:
            temp_list = []
            # precisa saber quantas imagens tem em um arquivo,e pra isso vai twer que usar uma funçao de um import
            num_of_frames = len(os.listdir(f'{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * escala), int(img.get_height() * escala)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update_animation(self):
        # para que as animaçoes tenham velocidades diferentes, fique a vontade de mudar a velo das animaçoes
        # mas saiba quye para m8dar a velocidade da animaçao do atque tem que casar com o cooldown do ataque
        if self.action == 1:
            ANIMATION_COOLDOWN = 130
        elif self.action == 3:
            ANIMATION_COOLDOWN = 100
        elif self.action == 2:
            ANIMATION_COOLDOWN = 150
        elif self.action == 3:
            ANIMATION_COOLDOWN = 100
        else:
            ANIMATION_COOLDOWN = 150
        self.image = self.animation_list[self.action][self.frame_index]
        # ver se ja passou o tempo necessario de uma imagem da animaçao para outra
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # isso é para que quando acabe a lista ele resete e recomece o loop da animação
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 4:
                self.frame_index = len(self.animation_list[self.action]) - 1

            else:
                self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    # IA boss

    def atacar(self):
        if self.atacar_cooldown == 0:

            self.ataque.center = (self.rect.centerx + 65 * self.direcao, self.rect.centery)
            self.atacar_cooldown = 50
            if self.ataque.colliderect(player.rect):
                if player.vida > 0:
                    machucado_fx.play()
                    player.vida -= 30

    def check_vivo(self):
        if self.vida <= 0:
            self.vida = 0
            self.vel = 0
            self.vivo = False

            self.update_action(4)

    def update(self):
        self.update_animation()
        self.check_vivo()
        if self.atacar_cooldown > 0:
            self.atacar_cooldown -= 1
        if self.move_cooldown > 0:
            self.move_cooldown -= 1
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.vida <= 400 and self.spawner == 0:
            player.vida = player.vida_max
            lobo = samurai('Lobisomen', 453 - bg_scroll, 442, 1, 3)
            enemy_group.add(lobo)
            esqueleto = samurai('Esqueleto', 272 - bg_scroll, 552, 1, 3)
            esqueleto_group.add(esqueleto)
            self.spawner += 1

        if self.vida <= 300 and self.spawner == 1:
            esqueleto = samurai('Esqueleto', 140 - bg_scroll, 442, 1, 3)
            esqueleto_group.add(esqueleto)
            esqueleto = samurai('Esqueleto', 1625 - bg_scroll, 442, 1, 3)
            esqueleto_group.add(esqueleto)
            self.spawner += 1

        if self.vida <= 200 and self.spawner == 2:
            lobo = samurai('Lobisomen', 741 - bg_scroll, 367, 1, 3)
            enemy_group.add(lobo)
            lobo = samurai('Lobisomen', 902 - bg_scroll, 552, 1, 3)
            enemy_group.add(lobo)
            self.spawner += 1
        if self.vida <= 100 and self.spawner == 3:
            lobo = samurai('Lobisomen', 272 - bg_scroll, 552, 1, 3)
            enemy_group.add(lobo)
            lobo = samurai('Lobisomen', 1336 - bg_scroll, 367, 1, 3)
            enemy_group.add(lobo)
            esqueleto = samurai('Esqueleto', 148 - bg_scroll, 442, 1, 3)
            esqueleto_group.add(esqueleto)
            esqueleto = samurai('Esqueleto', 1625 - bg_scroll, 442, 1, 3)
            esqueleto_group.add(esqueleto)

            self.spawner += 1

    def move(self, moving_left, moving_right):
        screen_scroll = 0
        dx = 0
        dy = 0

        if moving_left:
            dx = -self.vel
            self.virar = True
            self.direcao = -1
        if moving_right:
            self.virar = False
            self.direcao = 1
            dx = self.vel

        self.rect.x += dx
        self.rect.y += dy

    def ia(self):

        if self.vivo and player.vivo:

            if pygame.sprite.spritecollide(player, chefe_group, False):
                player.hitar = True
                if player.hit == 0 and player.hitar == True:
                    if player.vivo:
                        player.vida -= 30
                        machucado_fx.play()
                        player.hit = 100
            if self.vision.colliderect(player.rect):
                self.atacar()
                if self.atacar_cooldown > 25:
                    self.update_action(3)
                else:
                    self.update_action(0)

            else:

                if self.direcao == 1:
                    ia_move_right = True
                else:
                    ia_move_right = False

                ia_move_left = not ia_move_right
                if self.move_cooldown == 0:
                    self.vision.center = (3000, 0)

                    self.move(ia_move_left, ia_move_right)
                    self.move_counter += 1
                    self.update_action(1)
                    if self.move_counter > 310:
                        self.direcao *= -1
                        self.move_counter = 0
                        self.move_cooldown = 400
                        self.virar = not self.virar
                else:

                    self.vision.center = (self.rect.centerx + 75 * self.direcao, self.rect.centery)

                    if not self.vision.colliderect(player.rect):
                        self.shoot()
                        if self.shoot_cooldown > 60:
                            self.update_action(2)
                        else:
                            self.update_action(0)

    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 100
            corvooo = Corvos(self.rect.centerx, self.rect.centery, self.direcao, self.virar)
            corvo_group.add(corvooo)

            ataque_corvo.play()

    def draw(self, surface):
        screen.blit(pygame.transform.flip(self.image, self.virar, False), self.rect)

        self.rect.x += screen_scroll


class Fundo(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.animation_list = []
        self.frame_index = 0
        self.action = 0

        self.update_time = pygame.time.get_ticks()

        temp_list = []
        # precisa saber quantas imagens tem em um arquivo,e pra isso vai twer que usar uma funçao de um import
        num_of_frames = len(os.listdir(f'{self.char_type}/fundo'))
        for i in range(num_of_frames):
            img = pygame.image.load(f'{self.char_type}/fundo/{i}.jpg').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * 1), int(img.get_height() * 1)))
            temp_list.append(img)
            self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.update_animation()

    def update_animation(self):

        ANIMATION_COOLDOWN = 150

        self.image = self.animation_list[self.action][self.frame_index]
        # ver se ja passou o tempo necessario de uma imagem da animaçao para outra
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # isso é para que quando acabe a lista ele resete e recomece o loop da animação
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        screen.blit(pygame.transform.flip(self.image, False, False), self.rect)


# criar uma classe de samurai.
class samurai(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, escala, vel):
        pygame.sprite.Sprite.__init__(self)
        self.vivo = True
        self.char_type = char_type
        self.vel = vel
        self.atacar_cooldown = 0
        self.super = False
        self.shoot_cooldown = 0
        self.super_cooldown = 0
        self.vida = 100
        self.hit = 0
        self.hit_lobo = 0
        self.hitar = False
        self.hitar_lobo = False
        self.morte = 55

        self.vida_max = self.vida
        self.especial = 0
        self.especial_max = 10
        self.max_vida = self.vida
        self.direcao = 1
        self.vel_y = 0
        self.pulo = False
        self.no_ar = True
        self.virar = False
        self.animation_list = []
        self.frame_index = 0

        # ia
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 70, 20)
        self.visione = pygame.Rect(0, 0, 600, 200)
        self.ataque = pygame.Rect(0, 0, 40, 20)
        self.idling = False
        self.idling_counter = 0

        # esse action é para determinar quAL TIPO DE ANIMAÇAO VAI SE USAR, SE ELE VAI USAR CORRER,PADADO,ATAQUE ENTRE OUTROS
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        animation_type = ['parado', 'andar', 'pulo', 'ataque', 'morte']
        for animation in animation_type:
            temp_list = []
            # precisa saber quantas imagens tem em um arquivo,e pra isso vai twer que usar uma funçao de um import
            num_of_frames = len(os.listdir(f'{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * escala), int(img.get_height() * escala)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.update_animation()
        self.check_vivo()
        # atualizar o ataque para que nao ataque toda hora
        if self.super_cooldown > 0:
            self.super_cooldown -= 1
        if self.atacar_cooldown > 0:
            self.atacar_cooldown -= 1
        if self.hit > 0:
            self.hit -= 1
        if self.hit_lobo > 0:
            self.hit_lobo -= 1
        if self.morte > 0 and self.vivo == False:
            self.morte -= 1

    def check_vivo(self):
        if self.vida <= 0:
            self.vida = 0
            self.vel = 0

            if player.vivo == True and player.vida <= 0:
                morteH_fx.play()
                risada_boss.play()
            self.vivo = False

            self.update_action(4)

    def move(self, moving_left, moving_right):
        screen_scroll = 0
        dx = 0
        dy = 0

        if moving_left and self.vivo == True:
            dx = -self.vel
            self.virar = True
            self.direcao = -1

        if moving_right and self.vivo == True:
            self.virar = False
            self.direcao = 1
            dx = self.vel

        # pulo
        if self.pulo == True and self.no_ar == False and self.vivo == True:
            self.vel_y = -14

            self.no_ar = True

        # botando gravidade
        self.vel_y += gravidade
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        # colisao com o chao
        for tile in world.obstacle_list:
            # checar colisao na direçao x
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0

            # checar colisao na direçao y
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.no_ar = False
                    dy = tile[1].top - self.rect.bottom

        # checar se o jogador encostou na água
        if pygame.sprite.spritecollide(self, water_group, False):
            self.vida = 0

        # checar colisao com a saida
        level_complete = False
        if pygame.sprite.spritecollide(self, exit_group, False):
            level_complete = True

        # checar se o jogador caiu do mapa
        if self.rect.bottom > screen_height:
            self.vida = 0

        # checar se o jogador saiu da tela
        if self.char_type == 'samurai':
            if self.rect.left + dx < 0 or self.rect.right + dx > screen_width:
                dx = 0

        if self.vivo == True:
            self.rect.x += dx
            self.rect.y += dy

        # update scroll baseado na posição do jogador
        if self.char_type == 'samurai':
            if (self.rect.right > screen_width - scroll_thresh and bg_scroll < (
                    world.level_length * TILE_SIZE) - screen_width) or (
                    self.rect.left < scroll_thresh and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll, level_complete

    def atacar(self):
        if self.super == True and self.char_type == "samurai" and self.especial == 10:
            self.ultimate()
            especial_solto_fx.play()
            self.super = False

        if self.atacar_cooldown == 0:
            if self.char_type == 'samurai':
                ataque_fx.play()

            # esse e´o cooldown do ataque,se quiser que o persobagem ataque mais rapido so diminuir o numero
            self.atacar_cooldown = 50
            if self.char_type == 'Lobisomen':
                self.ataque.center = (self.rect.centerx + 65 * self.direcao, self.rect.centery)
            else:
                self.ataque.center = (self.rect.centerx + 50 * self.direcao, self.rect.centery)

            if self.ataque.colliderect(player.rect):
                if player.vida > 0:
                    machucado_fx.play()
                    player.vida -= 10

            for boss in chefe_group:
                if self.ataque.colliderect(boss.rect):
                    if self.especial < 10:
                        self.especial += 2
                    dano_boss.play()
                    boss.vida -= 50

            for enemy in enemy_group:

                if self.ataque.colliderect(enemy.rect) and self.char_type=="samurai":
                    enemy.vida -= 50
                    if self.especial < 10 and enemy.vivo == True:
                        self.especial += 2
                if enemy.vida <= 0:
                    if enemy.vida == 0 and enemy.vivo == True:
                        monstro_fx.play()
                    item_lobo_ataque = random.randint(1, 5)
                    if item_lobo_ataque == 3 and enemy.vivo == True:
                        item_lobo_ataque2 = random.randint(1, 2)
                        if item_lobo_ataque2 == 1:
                            recurso = Recursos('curar', enemy.rect.x + 40, enemy.rect.y + 60)
                            recursos_group.add(recurso)
                        elif item_lobo_ataque2 == 2:
                            recurso = Recursos('especial', enemy.rect.x + 40, enemy.rect.y + 60)
                            recursos_group.add(recurso)
                    enemy.alive = False

            for esq in esqueleto_group:
                if self.ataque.colliderect(esq.rect):
                    esq.vida -= 50
                    if self.especial < 10 and esq.vivo == True:
                        self.especial += 2

                if esq.vida <= 0:
                    if esq.vida == 0 and esq.vivo == True:
                        monstro_fx.play()
                    item_esq_ataque = random.randint(1, 5)
                    if item_esq_ataque == 3 and esq.vivo == True:
                        item_esq_ataque2 = random.randint(1, 2)
                        if item_esq_ataque2 == 1:
                            recurso = Recursos('curar', esq.rect.x + 15, esq.rect.y + 60)
                            recursos_group.add(recurso)
                        elif item_esq_ataque2 == 2:
                            recurso = Recursos('especial', esq.rect.x + 15, esq.rect.y + 60)
                            recursos_group.add(recurso)
                    esq.alive = False

    def iaesqueleto(self):
        if self.alive and player.alive:
            if self.visione.colliderect(player.rect):
                self.shoot()
                if self.shoot_cooldown > 1:
                    self.update_action(3)
                else:
                    self.update_action(0)

            else:
                if self.direcao == 1:
                    ia_moving_right = True
                else:
                    ia_moving_right = False
                ia_moving_left = not ia_moving_right
                self.move(ia_moving_left, ia_moving_right)
                self.update_action(1)

                self.move_counter += 1
                self.visione.center = (self.rect.centerx + 300 * self.direcao, self.rect.centery)
                if self.move_counter > TILE_SIZE:
                    self.direcao *= -1
                    self.move_counter *= -1

        # scroll
        self.rect.x += screen_scroll

    def ultimate(self):
        if self.super_cooldown == 0:
            self.especial -= 10
            self.super_cooldown = 100
            superr = Especial(self.rect.centerx + (0.6 * self.rect.size[0]) * self.direcao, self.rect.centery,
                              self.direcao)
            super_group.add(superr)

    def updatesuper(self):
        if self.super_cooldown > 0:
            self.super_cooldown -= 1

    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 100
            flechas = Flecha(self.rect.centerx + (0.6 * self.rect.size[0]) * self.direcao, self.rect.centery,self.direcao)
            flecha_group.add(flechas)

    def updateesq(self):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def ia(self):
        if self.alive and player.alive:
            for enemy in enemy_group:
                if pygame.sprite.collide_rect(player, enemy) and enemy.vivo == True:
                    player.hitar_lobo = True

                    if player.hit_lobo == 0 and player.hitar_lobo == True:
                        if player.vivo == True:
                            player.vida -= 10
                            machucado_fx.play()
                            player.hit_lobo = 80

            if self.vision.colliderect(player.rect) and self.char_type != 'anciao':

                self.atacar()
                if self.atacar_cooldown > 20:
                    self.update_action(3)
                else:
                    self.update_action(1)


            else:
                if self.direcao == 1:
                    ia_moving_right = True
                else:
                    ia_moving_right = False
                ia_moving_left = not ia_moving_right
                if self.char_type != 'anciao':
                    self.move(ia_moving_left, ia_moving_right)
                if self.char_type != 'anciao':
                    self.update_action(1)
                else:
                    self.update_action(0)
                self.move_counter += 1
                self.vision.center = (self.rect.centerx + 75 * self.direcao, self.rect.centery)
                if self.move_counter > TILE_SIZE:
                    self.direcao *= -1
                    self.move_counter *= -1

        # scroll
        self.rect.x += screen_scroll

    def update_animation(self):
        # para que as animaçoes tenham velocidades diferentes, fique a vontade de mudar a velo das animaçoes
        # mas saiba quye para m8dar a velocidade da animaçao do atque tem que casar com o cooldown do ataque
        if self.action == 1:
            ANIMATION_COOLDOWN = 130
        elif self.action == 3 and self.char_type == 'Esqueleto':
            ANIMATION_COOLDOWN = 100
        elif self.action == 2:
            ANIMATION_COOLDOWN = 150
        elif self.action == 3:
            ANIMATION_COOLDOWN = 100
        else:
            ANIMATION_COOLDOWN = 150
        self.image = self.animation_list[self.action][self.frame_index]
        # ver se ja passou o tempo necessario de uma imagem da animaçao para outra
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # isso é para que quando acabe a lista ele resete e recomece o loop da animação
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 4:
                self.frame_index = len(self.animation_list[self.action]) - 1

            else:
                self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        screen.blit(pygame.transform.flip(self.image, self.virar, False), self.rect)


class Especial(pygame.sprite.Sprite):
    def __init__(self, x, y, direcao):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        if direcao == 1:
            self.image = especial_img
        else:
            self.image = pygame.transform.flip(especial_img, True, False)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direcao = direcao

    def update(self):
        self.rect.x += (self.direcao * self.speed)
        if self.rect.right < 0 or self.rect.left > screen_width:
            self.kill()
        for enemy in chefe_group:
            if pygame.sprite.spritecollide(enemy, super_group, False):
                if enemy.vivo:
                    enemy.vida -= 100
                    dano_boss.play()
                    self.kill()
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, super_group, False):
                if enemy.vivo:
                    enemy.vida -= 100

            if enemy.vida <= 0:
                if enemy.vida == 0 and enemy.vivo == True:
                    monstro_fx.play()
                lobo_item = random.randint(1, 5)
                if lobo_item == 3 and enemy.vivo == True:
                    lobo_item2 = random.randint(1, 2)
                    if lobo_item2 == 1:
                        recurso = Recursos('curar', enemy.rect.x + 40, enemy.rect.y + 60)
                        recursos_group.add(recurso)
                    elif lobo_item2 == 2:
                        recurso = Recursos('especial', enemy.rect.x + 40, enemy.rect.y + 60)
                        recursos_group.add(recurso)
                enemy.alive = False
        for esq in esqueleto_group:
            if pygame.sprite.spritecollide(esq, super_group, False):
                if esq.vivo:
                    esq.vida -= 100

            if esq.vida <= 0:
                if esq.vida == 0 and esq.vivo == True:
                    monstro_fx.play()

                item_esqueleto = random.randint(1, 5)
                if item_esqueleto == 3 and esq.vivo == True:
                    item_esqueleto2 = random.randint(1, 2)
                    if item_esqueleto2 == 1:
                        recurso = Recursos('curar', esq.rect.x + 15, esq.rect.y + 60)
                        recursos_group.add(recurso)
                    elif item_esqueleto2 == 2:
                        recurso = Recursos('especial', esq.rect.x + 15, esq.rect.y + 60)
                        recursos_group.add(recurso)

                esq.alive = False


class Flecha(pygame.sprite.Sprite):
    def __init__(self, x, y, direcao):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10

        if direcao == 1:
            self.image = flecha_img
        else:
            self.image = pygame.transform.flip(flecha_img, True, False)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direcao = direcao

    def update(self):
        self.rect.x += (self.direcao * self.speed) + screen_scroll

        if self.rect.right < 0 or self.rect.left > screen_width:
            self.kill()
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

        if pygame.sprite.spritecollide(player, flecha_group, False):
            if player.vivo:
                player.vida -= 20
                machucado_fx.play()
                self.kill()


class Corvos(pygame.sprite.Sprite):
    def __init__(self, x, y, direcao, virar):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10


        self.char_type = 'corvo'
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        animation_type = ['voar']
        for animation in animation_type:
            temp_list = []
            # precisa saber quantas imagens tem em um arquivo,e pra isso vai twer que usar uma funçao de um import
            num_of_frames = len(os.listdir(f'{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * 1), int(img.get_height() * 1)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()

        self.rect.center = (x, y)
        self.direcao = direcao


        self.virar=virar

    def update(self):
        self.update_animation()
        self.rect.x += (self.direcao * self.speed) + screen_scroll

        if self.rect.right < 0 or self.rect.left > screen_width:
            self.kill()
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

        if pygame.sprite.spritecollide(player, corvo_group, False):
            if player.vivo:
                player.vida -= 10
                machucado_fx.play()
                self.kill()


    def update_animation(self):
        # para que as animaçoes tenham velocidades diferentes, fique a vontade de mudar a velo das animaçoes
        # mas saiba quye para m8dar a velocidade da animaçao do atque tem que casar com o cooldown do ataque
        ANIMATION_COOLDOWN = 150
        self.update_action(0)
        self.image = self.animation_list[self.action][self.frame_index]
        # ver se ja passou o tempo necessario de uma imagem da animaçao para outra
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # isso é para que quando acabe a lista ele resete e recomece o loop da animação
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()



    def draw(self,surface):
        screen.blit(pygame.transform.flip(self.image, self.virar , False), self.rect)




class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        self.level_length = len(data[0])
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 6:
                        self.obstacle_list.append(tile_data)  # chao
                    elif tile >= 7 and tile <= 8:
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water)  # agua
                    elif tile >= 9 and tile <= 11:
                        decoracao = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoracao_group.add(decoracao)  # decoracao
                    elif tile == 12:  # inimigo
                        lobo = samurai('Lobisomen', x * TILE_SIZE, y * TILE_SIZE, 1, 3)
                        enemy_group.add(lobo)
                    elif tile == 13:
                        player = samurai('samurai', x * TILE_SIZE, y * TILE_SIZE, 1, 6)
                        vida = BarraDeVida(10, 10, player.vida, player.vida)
                    elif tile == 14:  # ultimate
                        recurso = Recursos('especial', x * TILE_SIZE, y * TILE_SIZE)
                        recursos_group.add(recurso)
                    elif tile == 15:  # cura
                        recurso = Recursos('curar', x * TILE_SIZE, y * TILE_SIZE)
                        recursos_group.add(recurso)
                    elif tile == 16:
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)
                    elif tile == 17:  # inimigo
                        esqueleto = samurai('Esqueleto', x * TILE_SIZE, y * TILE_SIZE, 1, 3)
                        esqueleto_group.add(esqueleto)
                    elif tile == 18:  # chefe
                        chefe = boss('Boss', x * TILE_SIZE, y * TILE_SIZE, 1, 5)
                        chefe_group.add(chefe)
                    elif tile == 19:
                        anciao = samurai('anciao', x * TILE_SIZE, y * TILE_SIZE, 1, 3)
                        anciao_group.add(anciao)

        return player, vida

    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])


class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll


class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll


class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll


class Recursos(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = recursos[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        # scroll
        self.rect.x += screen_scroll
        # checar se o jogador pegou algum recurso
        if pygame.sprite.collide_rect(self, player):
            # checar qual foi o recurso pego
            if self.item_type == 'curar':
                pegando_vida_fx.play()
                player.vida += 25
                if player.vida > player.vida_max:
                    player.vida = player.vida_max

            elif self.item_type == 'especial':
                pegando_especial_fx.play()
                player.especial = 10
                if player.especial > player.especial_max:
                    player.especial = player.especial_max
            # deletar os recursos
            self.kill()


class BarraDeVida():
    def __init__(self, x, y, vida, vida_max):
        self.x = x
        self.y = y
        self.vida = vida
        self.vida_max = vida_max

    def draw(self, vida):
        # update com nova vida
        self.vida = vida

        ratio = self.vida / self.vida_max
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))

    def update(self):
        self.rect.x += screen_scroll


class BarraDeVida_Boss():
    def __init__(self, x, y, vida, vida_max):
        self.x = x
        self.y = y
        self.vida = vida
        self.vida_max = vida_max

    def draw(self, vida):
        # update com nova vida
        self.vida = vida

        ratio = self.vida / self.vida_max
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 964, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y, 960, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 960 * ratio, 20))

    def update(self):
        self.rect.x += screen_scroll


class screenfade():
    def __init__(self, direcao, cor, speed):
        self.direcao = direcao
        self.cor = cor
        self.speed = speed
        self.fade_counter = 0

    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direcao == 1:
            pygame.draw.rect(screen, self.cor, (0 - self.fade_counter, 0, screen_width // 2, screen_height))
            pygame.draw.rect(screen, self.cor, (screen_width // 2 + self.fade_counter, 0, screen_width, screen_height))
            pygame.draw.rect(screen, self.cor, (0, 0 - self.fade_counter, screen_width, screen_height // 2))
            pygame.draw.rect(screen, self.cor, (0, screen_height // 2 + self.fade_counter, screen_width, screen_height))
        if self.direcao == 2:
            pygame.draw.rect(screen, self.cor, (0, 0, screen_width, 0 + self.fade_counter))
        if self.fade_counter >= screen_width - 600:
            fade_complete = True
        return fade_complete


# screen fade
intro_fade = screenfade(1, BLACK, 4)

# criação de grupos
decoracao_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

enemy_group = pygame.sprite.Group()
anciao_group = pygame.sprite.Group()
chefe_group = pygame.sprite.Group()

esqueleto_group = pygame.sprite.Group()
flecha_group = pygame.sprite.Group()
corvo_group = pygame.sprite.Group()

super_group = pygame.sprite.Group()

espada_group = pygame.sprite.Group()
recursos_group = pygame.sprite.Group()

world_data = []
for row in range(rows):
    r = [-1] * cols
    world_data.append(r)
# load in level data and create world
with open(f'level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

world = World()
player, vida = world.process_data(world_data)

# MENU
# fundo menu
fundomenu = Fundo("fundo animado", 600, 300)
fundofinal = Fundo("final real", 600, 300)
tutorial_fundo = Fundo("tutorial", 600, 300)
# button images
start_img = pygame.image.load('Button/play.png').convert_alpha()
more_img = pygame.image.load('Button/more.png').convert_alpha()
exit_img = pygame.image.load('Button/quit.png').convert_alpha()

restart_img = pygame.image.load('Button/play.png').convert_alpha()

# create buttons
start_button = button.Button(screen_width // 2 - 90, screen_height // 2 - 100, start_img, 1)
more_button = button.Button(screen_width // 2 - 90, screen_height // 2 + 50, more_img, 1)
exit_button = button.Button(screen_width // 2 - 90, screen_height // 2 + 200, exit_img, 1)

restart_button = button.Button(screen_width // 2 - 100, 30, restart_img, 1)
musica = 0
run = True

caminho_fonte_boss = "fonte/DemonLetter.ttf"
fontes = pygame.font.Font(caminho_fonte_boss, 36)

abertura_fonte = "fonte/Harukaze.ttf"
fonte_abertura = pygame.font.Font(abertura_fonte, 170)

especial_fonte = "fonte/Enchanted Land.otf"
fonte_especial = pygame.font.Font(especial_fonte, 40)

fundo = 30
linhas_texto = [
    "Meus parabens herói,você restaurou a balança natural do mundo entre o bem e o mal.",
    "Por sua bravura e habilidade o povo dessas terras viverão em paz e seguras.",
    "Porem, o mal se espreita nas sombras,portanto,esteja sempre pronto para uma nova batalha.",
]
caminho_fonte = "fonte/Zeyada-Regular.ttf"
fonte = pygame.font.Font(caminho_fonte, 36)
textos_renderizados = [fonte.render(linha, True, WHITE) for linha in linhas_texto]
retangulos_texto = [texto.get_rect() for texto in textos_renderizados]

for i, retangulo in enumerate(retangulos_texto):
    retangulo.topleft = (50, 450 + i * 40)
final_cooldown = 120
intro = True
tutorial = False

superficie_fade = pygame.Surface((1200, 600))
superficie_fade.fill((0, 0, 0))
alpha = 255
fade_in = True

superficie_fade_inicio = pygame.Surface((1200, 600))
superficie_fade_inicio.fill((0, 0, 0))
alpha_inicio = 255
fade_in_inicio = True

superficie_fade_morte = pygame.Surface((1200, 600))
superficie_fade_morte.fill((0, 0, 0))
alpha_morte = 255
fade_in_morte = False

superficie_fade_level = pygame.Surface((1200, 600))
superficie_fade_level.fill((0, 0, 0))
alpha_level = 255
fade_in_level = False


linhas_texto_anciao = [
    "Ola herói, estava a sua espera.",
    "Raum,o conde do inferno,despertou e esta usando de sua magia para dominar essas terras.",
    "Você precisa derrota-lo e restaurar a paz no nosso mundo pelo bem de toda a humanidade.",
    "Boa sorte herói, o destino do mundo esta na ponta de sua espada.",
]

cor_balao = (0, 0, 0)
cor_texto = (255, 255, 255)
fonte_anciao = pygame.font.Font("fonte/Minecraftia-Regular.ttf", 15)
while run:
    clock.tick(FPS)

    if level == 2 and intro == True:
        jogo_musica.stop()
        comeco_batalha.play()
        boss_figth.play(loops=-1)

        intro = False

    if final == True:

        if fundo >= 0:
            fundo -= 1
            start_intor = True
            boss_figth.stop()


        elif fundo < 30:
            final_musica.play(loops=-1)
            fundofinal.update()
            fundofinal.draw(screen)
            for i, texto in enumerate(textos_renderizados):
                screen.blit(texto, retangulos_texto[i])
    else:
        if tutorial == True:
            screen.blit(fundo_img, (0, 0))
            tutorial_fundo.update()
            tutorial_fundo.draw(screen)
        else:
            if start_game == False and final == False:
                # draw menu
                menu_musica.play(loops=-1)
                fundomenu.update()
                fundomenu.draw(screen)
                draw_text(f'Samurai Mitology War', fonte_abertura, RED, 100, 10)

                # add buttons
                if start_button.draw(screen):
                    menu_musica.stop()
                    if final == False:
                        jogo_musica.play(loops=-1)

                    start_game = True
                if more_button.draw(screen):
                    tutorial = True
                if exit_button.draw(screen):
                    run = False
            else:

                draw_fundo()
                world.draw()

                # mostrar vida
                vida.draw(player.vida)

                # mostrar especial

                # samurai
                player.update()

                player.draw(screen)

                # inimigo
                for enemy in enemy_group:
                    enemy.ia()
                    enemy.update()
                    enemy.draw(screen)


                for anciao in anciao_group:
                    anciao.ia()
                    anciao.update()
                    anciao.draw(screen)

                for enemy in esqueleto_group:
                    enemy.iaesqueleto()
                    enemy.update()
                    enemy.updateesq()
                    enemy.draw(screen)

                for chefe in chefe_group:
                    chefe.draw(screen)
                    chefe.update()
                    chefe.ia()
                    chefe.check_vivo()

                    draw_text(f'Raum: ', fontes, BLACK, 10, 548)
                    vidas = BarraDeVida_Boss(120, 565, chefe.vida, chefe.vida_max)
                    vidas.draw(chefe.vida)
                    if chefe.vivo == False:
                        final_cooldown -= 1
                        if final_cooldown <= 0:
                            final = True
                for corvo in corvo_group:
                    corvo.update()
                    corvo.draw(screen)


                # update groups
                decoracao_group.update()
                water_group.update()
                exit_group.update()
                espada_group.update()
                recursos_group.update()
                flecha_group.update()
                super_group.update()

                flecha_group.draw(screen)
                super_group.draw(screen)
                recursos_group.draw(screen)
                decoracao_group.draw(screen)
                water_group.draw(screen)
                exit_group.draw(screen)


                if player.super == True:
                    draw_text(f'especial: ', fonte_especial, WHITE, 10, 26)
                else:
                    draw_text(f'especial: ', fonte_especial, BLACK, 10, 26)
                for x in range(player.especial):
                    screen.blit(recurso_especial_img, (100 + (x * 20), 40))
                if fade_in_inicio:
                    superficie_fade.set_alpha(alpha_inicio)
                    screen.blit(superficie_fade, (0, 0))

                    pygame.display.flip()

                # Atualiza a transparência
                if fade_in_inicio:
                    alpha_inicio -= 1
                    if alpha_inicio <= 0:
                        alpha_inicio = 0
                        fade_in_inicio = False
                # colocar a condiçao dele estar vivo porque senao nosso pernagem vai fazer coisas enquanto estiver morto ai nosso personagem seria um zumbi kkkkk
                if player.vivo:

                    # atualizar a açao do samurai
                    if ataque:
                        player.atacar()

                    # esse forma de por a animaçao de ataque nao é muito eficiente se conseguir oputro metodo me fala dps pff
                    if player.atacar_cooldown > 20:
                        player.update_action(3)

                    elif player.no_ar:
                        player.update_action(2)  # pular
                    elif moving_left or moving_right:
                        player.update_action(1)  # correr
                    else:
                        player.update_action(0)  # parado
                    if player.vivo:
                        screen_scroll, level_complete = player.move(moving_left, moving_right)
                        bg_scroll -= screen_scroll

                    # checar se o jogador completou o level
                    if level_complete:
                        fade_in_level = True
                        level += 1
                        bg_scroll = 0
                        world_data = reset_level()
                        if level <= MAX_LEVELS:
                            with open(f'level{level}_data.csv', newline='') as csvfile:
                                reader = csv.reader(csvfile, delimiter=',')
                                for x, row in enumerate(reader):
                                    for y, tile in enumerate(row):
                                        world_data[x][y] = int(tile)

                            world = World()
                            player, vida = world.process_data(world_data)


                if pygame.sprite.spritecollide(player, anciao_group, False):
                    textos_renderizados_anciao = []

                    # Renderiza cada linha de texto individualmente
                    for linha in linhas_texto_anciao:
                        texto_renderizado12 = fonte_anciao.render(linha, True, (255, 255, 255))
                        textos_renderizados_anciao.append(texto_renderizado12)
                    retangulo = pygame.Surface((1000, 150), pygame.SRCALPHA)
                    retangulo.fill((0, 0, 255, 128))
                    screen.blit(retangulo, (100, 450))
                    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(100, 450, 1000, 150), 4)
                    y_pos = 470
                    for texto_renderizadoo in textos_renderizados_anciao:
                        screen.blit(texto_renderizadoo, (120, y_pos))
                        y_pos += 30
                    for linha in linhas_texto_anciao:
                        textos_renderizados_anciao = fonte.render(linha, True, WHITE)

                    # Desenha o balão de texto


                else:
                    if player.morte == 0:

                        screen_scroll = 0

                        screen.blit(morte_personagem, (0, 0))  # Desenha a imagem de fundo
                        # Ajusta a transparência da superfície de fade
                        if fade_in:
                            superficie_fade.set_alpha(alpha)
                            screen.blit(superficie_fade, (0, 0))

                            pygame.display.flip()

                        # Atualiza a transparência
                        if fade_in:
                            alpha -= 1
                            if alpha <= 0:
                                alpha = 0
                                fade_in = False

                        if restart_button.draw(screen):

                            bg_scroll = 0
                            world_data = reset_level()
                            with open(f'level{level}_data.csv', newline='') as csvfile:
                                reader = csv.reader(csvfile, delimiter=',')
                                for x, row in enumerate(reader):
                                    for y, tile in enumerate(row):
                                        world_data[x][y] = int(tile)

                            world = World()
                            player, vida = world.process_data(world_data)
                            fade_in_morte = True

    if fade_in_morte:
        superficie_fade_morte.set_alpha(alpha_morte)
        screen.blit(superficie_fade_morte, (0, 0))

        pygame.display.flip()

    # Atualiza a transparência
    if fade_in_morte:
        alpha_morte -= 1
        if alpha_morte <= 0:
            alpha_morte = 0
            fade_in_morte = False
    if level == 2 and alpha_level==255:
        fade_in_level = True

    if fade_in_level:
        superficie_fade_level.set_alpha(alpha_level)
        screen.blit(superficie_fade_level, (0, 0))

        pygame.display.flip()

    # Atualiza a transparência
    if fade_in_level:
        alpha_level -= 1
        if alpha_level <= 0:
            if level==2:
                alpha_level=254.99
            else:
                alpha_level = 255

            fade_in_level = False

    for event in pygame.event.get():
        # sair do jogo
        if event.type == pygame.QUIT:
            run = False

        # botão pressionado
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
                if level == 2:
                    andar_pedra.play(loops=-1)
                else:
                    andar_terra.play(loops=-1)
            if event.key == pygame.K_d:
                moving_right = True
                if level == 2:
                    andar_pedra.play(loops=-1)
                else:
                    andar_terra.play(loops=-1)
            if event.key == pygame.K_w and player.vivo:
                player.pulo = True
                pulo_fx.play()
            if event.key == pygame.K_SPACE and player.vivo:
                player.atacando = True
                ataque = True
            if event.key == pygame.K_e and player.vivo:
                player.super = not player.super
                if player.super == True and player.especial == 10:
                    com_especial_fx.play()
            if event.key == pygame.K_ESCAPE:
                if tutorial == True:
                    tutorial = False

        # botão solto
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
                if level == 2:
                    andar_pedra.stop()
                else:
                    andar_terra.stop()
            if event.key == pygame.K_d:
                moving_right = False
                if level == 2:
                    andar_pedra.stop()
                else:
                    andar_terra.stop()
            if event.key == pygame.K_w:
                player.pulo = False
            if event.key == pygame.K_SPACE and player.vivo:
                ataque = False

    pygame.display.update()

# termina o pygame
pygame.quit()
