import pygame
from interface import tela_pausa, desenhar_botao_pause
from math_utils import calcular_raizes_e_equação, calcular_lancamento
from draw_utils import desenhar_parabola, desenhar_pontos, desenhar_equacao_com_imagem, desenhar_legenda_pontos, desenhar_barra_forca, desenhar_direcao_lancamento
from game_utils import resetar_baggete

from settings import screen, clock, fonte, gravity, max_power, max_press_duration, ORIGEM_PIXEL, ESCALA_X, ESCALA_Y, Y_CHÃO, LARGURA_TELA, ALTURA_TELA
from assets import plane_surface_freeMode, baggete_start_pos, arrow_surface, baggete_frames, board_surface

def run_modo_livre():

    baggete_rect = baggete_frames[0].get_rect(midbottom=baggete_start_pos)
    baggete_velocity_x = 0.0
    baggete_velocity_y = 0.0
    baggete_pos_x = float(baggete_rect.midbottom[0])
    baggete_pos_y = float(baggete_rect.midbottom[1])

    baggete_frame_index = 0
    baggete_frame_timer = 0
    frame_duration = 50  # ms entre frames

    press_start_time = None
    is_pressing = False
    last_power_ratio = None
    can_launch = True

    trail = []

    equacao_texto = ""

    Pi_pixel = V_pixel = Pf_pixel = None
    Pi_plano = V_plano = Pf_plano = None
    coeficientes = None

    impacto_calculado = False

    running = True
    while running:
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
             if btn_pause.collidepoint(event.pos):
                 acao = tela_pausa(screen, fonte, clock)
                 if acao == "menu":
                    # Voltar ao menu, sai do modo livre
                    return "menu"
                # Se continuar, só volta pro loop normalmente

            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                acao = tela_pausa(screen, fonte, clock)
                if acao == "menu":
                    # Voltar ao menu, sai do modo livre
                    return "menu"
                # Se continuar, só volta pro loop normalmente

            if event.type == pygame.QUIT:
                # Fecha o modo livre e volta ao menu
                return "menu"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and can_launch:
                    press_start_time = pygame.time.get_ticks()
                    is_pressing = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE and is_pressing and can_launch:
                    (baggete_velocity_x, baggete_velocity_y, last_power_ratio, equacao_texto,
                     Pi_pixel, V_pixel, Pf_pixel,
                     Pi_plano, V_plano, Pf_plano,
                     coeficientes, impacto_calculado) = calcular_lancamento(
                        press_start_time,
                        max_press_duration,
                        max_power,
                        baggete_rect,
                        trail
                    )

                    is_pressing = False
                    press_start_time = None
                    can_launch = False

        # Atualização física da bola
        baggete_velocity_y += gravity
        baggete_pos_x += baggete_velocity_x
        baggete_pos_y += baggete_velocity_y
        baggete_rect.midbottom = (int(baggete_pos_x), int(baggete_pos_y))

        # Controle do rastro
        if 0 <= baggete_rect.centerx <= LARGURA_TELA and 0 <= baggete_rect.centery <= ALTURA_TELA:
            trail.append(baggete_rect.center)

        # Colisão com o "chão"
        if baggete_rect.bottom >= Y_CHÃO:
            baggete_rect.bottom = Y_CHÃO
            baggete_pos_y = Y_CHÃO
            baggete_velocity_y = 0
            baggete_velocity_x = 0
            if not can_launch:
                can_launch = True
                if not impacto_calculado and len(trail) >= 3:
                    impacto_calculado = True

                (
                    Pi_pixel, V_pixel, Pf_pixel,
                    Pi_plano, V_plano, Pf_plano,
                    coeficientes, equacao_texto
                ) = calcular_raizes_e_equação(trail, Y_CHÃO, ORIGEM_PIXEL, ESCALA_X, ESCALA_Y)

        else:
            impacto_calculado = False

        # Reset se sair da tela
        if (baggete_rect.right < 0 or baggete_rect.left > LARGURA_TELA or
            baggete_rect.bottom < 0 or baggete_rect.top > ALTURA_TELA):
            (
                baggete_pos_x, baggete_pos_y,
                baggete_velocity_x, baggete_velocity_y,
                can_launch, equacao_texto, impacto_calculado,
                trail,
                Pi_pixel, V_pixel, Pf_pixel,
                Pi_plano, V_plano, Pf_plano,
                coeficientes
            ) = resetar_baggete(baggete_rect, baggete_start_pos)

        # Atualização da animação da bola (somente se estiver em movimento)
        if baggete_velocity_x != 0 or baggete_velocity_y != 0:
            baggete_frame_timer += clock.get_time()
            if baggete_frame_timer >= frame_duration:
                baggete_frame_timer = 0
                baggete_frame_index = (baggete_frame_index + 1) % len(baggete_frames)
        else:
            baggete_frame_index = 0  # volta para o primeiro quadro quando parado

        # --- DESENHOS ---
        screen.blit(plane_surface_freeMode, (0, 0))
        screen.blit(baggete_frames[baggete_frame_index], baggete_rect)

        desenhar_barra_forca(screen, is_pressing, press_start_time, last_power_ratio)

        btn_pause = desenhar_botao_pause(screen)

        if coeficientes and Pi_plano and Pf_plano:
            desenhar_parabola(screen, coeficientes, Pi_plano, Pf_plano, ORIGEM_PIXEL, ESCALA_X, ESCALA_Y)

        if can_launch:
            desenhar_direcao_lancamento(screen, baggete_rect.center, arrow_surface)

        if equacao_texto:
            desenhar_equacao_com_imagem(screen, equacao_texto, board_surface)

        if Pi_pixel and V_pixel and Pf_pixel:
            desenhar_pontos(screen, Pi_pixel, V_pixel, Pf_pixel)
            desenhar_legenda_pontos(screen, fonte, Pi_plano, V_plano, Pf_plano, Pi_pixel, V_pixel, Pf_pixel)

        pygame.display.update()
        clock.tick(60)

    return "menu"  # fallback para sair do modo livre
