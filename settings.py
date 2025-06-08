import pygame

pygame.init()
LARGURA_TELA = 1200
ALTURA_TELA = 705
SCREEN_WIDTH, SCREEN_HEIGHT = LARGURA_TELA, ALTURA_TELA
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Cannon Game')
clock = pygame.time.Clock()
fonte = pygame.font.SysFont(None, 28)

ORIGEM_PIXEL = (599, 599)
ESCALA_X = 599 / 11
ESCALA_Y = 599 / 11

Y_CHÃO = 599
LARGURA_TELA = 1200
ALTURA_TELA = 705

max_power = 34
max_press_duration = 1000

gravity = 1

bar_position = (20, 51)
bar_size = (30, 275)
bar_border_color = (0, 0, 0)
