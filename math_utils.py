import numpy as np
from math import atan2, cos, sin
from settings import ALTURA_TELA
import pygame

def pixel_para_plano(x_pixel, y_pixel, origem_pixel, escala_x, escala_y):
    x_cartesiano = (x_pixel - origem_pixel[0]) / escala_x
    y_cartesiano = (origem_pixel[1] - y_pixel) / escala_y
    return x_cartesiano, y_cartesiano

def plano_para_pixel(x_cartesiano, y_cartesiano, origem_pixel, escala_x, escala_y):
    x_pixel = int(origem_pixel[0] + x_cartesiano * escala_x)
    y_pixel = int(origem_pixel[1] - y_cartesiano * escala_y)
    return x_pixel, y_pixel

def calcular_parabola(p1, p2, p3):
    x = [p1[0], p2[0], p3[0]]
    y = [p1[1], p2[1], p3[1]]

    if len(set(x)) < 3:
        return None

    A = np.array([
        [x[0]**2, x[0], 1],
        [x[1]**2, x[1], 1],
        [x[2]**2, x[2], 1]
    ])
    y = np.array(y)

    try:
        a, b, c = np.linalg.solve(A, y)
        return a, b, c
    except np.linalg.LinAlgError:
        return None

def calcular_ponto_intermediario(p1, p2):
    x_m = (p1[0] + p2[0]) / 2
    y_m = (p1[1] + p2[1]) / 2
    return (x_m, y_m)

def calcular_raizes_e_equação(trail, Y_CHÃO, ORIGEM_PIXEL, ESCALA_X, ESCALA_Y):

    Pi_pixel = (trail[0][0], Y_CHÃO)
    V_pixel = min(trail, key=lambda p: p[1])
    Pf_pixel = (trail[-1][0], Y_CHÃO)
    Pi_plano = pixel_para_plano(*Pi_pixel, ORIGEM_PIXEL, ESCALA_X, ESCALA_Y)
    V_plano = pixel_para_plano(*V_pixel, ORIGEM_PIXEL, ESCALA_X, ESCALA_Y)
    Pf_plano = pixel_para_plano(*Pf_pixel, ORIGEM_PIXEL, ESCALA_X, ESCALA_Y)
    equacao_texto = "Função indefinida"
    coeficientes = None

    resultado = calcular_parabola(Pi_plano, V_plano, Pf_plano)
    if resultado:
        a, b, c = resultado
        xv = -b / (2 * a)
        yv = a * xv**2 + b * xv + c
        V_plano = (xv, yv)
        V_pixel = plano_para_pixel(xv, yv, ORIGEM_PIXEL, ESCALA_X, ESCALA_Y)
        equacao_texto = f"y = {a:.2f}x² + {b:.2f}x + {c:.2f}"
        coeficientes = (a, b, c)

    return Pi_pixel, V_pixel, Pf_pixel, Pi_plano, V_plano, Pf_plano, coeficientes, equacao_texto   

def calcular_lancamento(press_start_time, max_press_duration, max_power, ball_rect, trail):
    press_duration = pygame.time.get_ticks() - press_start_time
    power_ratio = min(press_duration / max_press_duration, 1)
    intensity = power_ratio * max_power

    mouse_x, mouse_y = pygame.mouse.get_pos()
    dx = mouse_x - ball_rect.centerx
    dy = mouse_y - ball_rect.centery
    angle = atan2(dy, dx)

    ball_vel_x = cos(angle) * intensity
    ball_vel_y = -abs(sin(angle)) * intensity
    if abs(ball_vel_y) < 5:
        ball_vel_y = -5

    # Limpar variáveis relacionadas ao estado do lançamento
    trail.clear()
    equacao_texto = ""
    Pi_pixel = V_pixel = Pf_pixel = None
    Pi_plano = V_plano = Pf_plano = None
    coeficientes = None
    impacto_calculado = False

    return (ball_vel_x, ball_vel_y, power_ratio, equacao_texto,
            Pi_pixel, V_pixel, Pf_pixel,
            Pi_plano, V_plano, Pf_plano,
            coeficientes, impacto_calculado)