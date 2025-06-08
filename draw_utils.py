# draw_utils.py
import pygame
from math import atan2, degrees
from math_utils import plano_para_pixel

def desenhar_parabola(screen, coeficientes, Pi_plano, Pf_plano, ORIGEM_PIXEL, ESCALA_X, ESCALA_Y, cor=(160, 32, 240), step=0.05):
    if coeficientes and Pi_plano and Pf_plano:
        a, b, c = coeficientes
        x_inicial = min(Pi_plano[0], Pf_plano[0])
        x_final = max(Pi_plano[0], Pf_plano[0])
        pontos_pixel = []
        x = x_inicial
        while x <= x_final:
            y = a * x ** 2 + b * x + c
            x_pixel, y_pixel = plano_para_pixel(x, y, ORIGEM_PIXEL, ESCALA_X, ESCALA_Y)
            pontos_pixel.append((x_pixel, y_pixel))
            x += step
        if len(pontos_pixel) > 1:
            pygame.draw.lines(screen, cor, False, pontos_pixel, 2)

def desenhar_pontos(screen, Pi_pixel, V_pixel, Pf_pixel):
    if Pi_pixel and V_pixel and Pf_pixel:
        pygame.draw.circle(screen, (255, 0, 0), Pi_pixel, 6)
        pygame.draw.circle(screen, (0, 255, 0), V_pixel, 6)
        pygame.draw.circle(screen, (0, 0, 255), Pf_pixel, 6)

def desenhar_equacao_com_imagem(screen, equacao_texto, board_surface, pos_x=780, pos_y=10, padding=20):
    if equacao_texto:
        fonte_titulo = pygame.font.SysFont(None, 32)
        fonte_maior = pygame.font.SysFont(None, 30)

        titulo = fonte_titulo.render("Função da parábola:", True, (0, 0, 0))
        equacao = fonte_maior.render(equacao_texto, True, (0, 0, 0))

        # Ajuste do tamanho da imagem (opcional, pode comentar se imagem já for do tamanho certo)
        largura = max(titulo.get_width(), equacao.get_width()) + 4 * padding
        altura = titulo.get_height() + equacao.get_height() + 3 * padding
        board_scaled = pygame.transform.scale(board_surface, (largura, altura))

        # Blit da imagem de fundo (board)
        screen.blit(board_scaled, (pos_x, pos_y))

        # Blit dos textos por cima da imagem
        screen.blit(titulo, (pos_x + padding +20, pos_y + padding ))
        screen.blit(equacao, (pos_x + padding +20, pos_y + padding + titulo.get_height() + 10))

def desenhar_legenda_pontos(screen, fonte, Pi_plano, V_plano, Pf_plano, Pi_pixel, V_pixel, Pf_pixel, legenda_x=250, legenda_y=20):
    pygame.draw.rect(screen, (0, 0, 0), (legenda_x - 10, legenda_y - 10, 170, 100), border_radius=10)
    pygame.draw.rect(screen, (255, 255, 255), (legenda_x - 10, legenda_y - 10, 170, 100), 2, border_radius=10)

    pygame.draw.circle(screen, (255, 255, 0), Pi_pixel, 7)
    screen.blit(fonte.render(f"Pi = ({Pi_plano[0]:.2f}, {Pi_plano[1]:.2f})", True, (255, 255, 0)), (legenda_x, legenda_y))

    pygame.draw.circle(screen, (255, 0, 0), V_pixel, 7)
    screen.blit(fonte.render(f"V  = ({V_plano[0]:.2f}, {V_plano[1]:.2f})", True, (255, 0, 0)), (legenda_x, legenda_y + 30))

    pygame.draw.circle(screen, (0, 255, 0), Pf_pixel, 7)
    screen.blit(fonte.render(f"Pf = ({Pf_plano[0]:.2f}, {Pf_plano[1]:.2f})", True, (0, 255, 0)), (legenda_x, legenda_y + 60))

def desenhar_barra_forca(screen, is_pressing, press_start_time, last_power_ratio,
                         max_power=34, max_press_duration=1000,
                         bar_position=(20, 51), bar_size=(30, 275), bar_border_color=(0, 0, 0)):
    
    def interpolar_cor_verde_vermelho(p):
        r = int(255 * p)
        g = int(255 * (1 - p))
        return (r, g, 0)

    # Desenha a borda da barra
    pygame.draw.rect(screen, bar_border_color, (*bar_position, *bar_size), 2, border_radius=10)

    # Calcula preenchimento atual
    if is_pressing and press_start_time is not None:
        current_duration = pygame.time.get_ticks() - press_start_time
        power_ratio = min(current_duration / max_press_duration, 1)
        fill_height = int(bar_size[1] * power_ratio)
        fill_y = bar_position[1] + bar_size[1] - fill_height
        fill_color = interpolar_cor_verde_vermelho(power_ratio)
        pygame.draw.rect(screen, fill_color, (bar_position[0], fill_y, bar_size[0], fill_height), border_radius=10)

    elif last_power_ratio is not None:
        fill_height = int(bar_size[1] * last_power_ratio)
        fill_y = bar_position[1] + bar_size[1] - fill_height
        fill_color = interpolar_cor_verde_vermelho(last_power_ratio)
        pygame.draw.rect(screen, fill_color, (bar_position[0], fill_y, bar_size[0], fill_height), border_radius=10)

def desenhar_direcao_lancamento(screen, origem, ponteiro_surface):
    """
    Desenha um ponteiro (ex: seta, canhão) rotacionado na direção do mouse a partir da origem fornecida.
    """
    mouse_x, mouse_y = pygame.mouse.get_pos()
    dx = mouse_x - origem[0]
    dy = mouse_y - origem[1]
    angle_deg = -degrees(atan2(dy, dx))
    ponteiro_rotacionado = pygame.transform.rotate(ponteiro_surface, angle_deg)
    ponteiro_rect = ponteiro_rotacionado.get_rect(center=origem)
    screen.blit(ponteiro_rotacionado, ponteiro_rect)
