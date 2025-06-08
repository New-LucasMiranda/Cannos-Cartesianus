import pygame
from interface import tela_pausa, tela_sucesso_fase, tela_fim_de_jogo, gerenciar_proxima_fase, desenhar_botao_pause
from fases import fases
from math_utils import calcular_raizes_e_equação, calcular_lancamento
from draw_utils import desenhar_parabola, desenhar_pontos, desenhar_legenda_pontos, desenhar_barra_forca
from game_utils import resetar_baggete, construir_conjunto_canhao

from settings import screen, clock, fonte, gravity, max_power, max_press_duration, ORIGEM_PIXEL, ESCALA_X, ESCALA_Y, Y_CHÃO, LARGURA_TELA, ALTURA_TELA
from assets import plane_surface_phaseMode, descartes_surface, hobbes_surface, baggete_frames, groundShield_surface, wood_surface, base_surface, cannon_surface, flying_surface
import math

def run_modo_fases():
    fase_atual = 0

    def iniciar_fase(fase_idx):
            
        fase = fases[fase_idx]

        base_pos = fase.get("base_pos")
        base_rect, cannon_rect, baggete_rect = construir_conjunto_canhao(base_pos)

            # Valores iniciais da baguete
        baggete_pos_x = float(baggete_rect.centerx)
        baggete_pos_y = float(baggete_rect.centery)

        baggete_pos_inicial = baggete_rect.midbottom

        descartes_pos_inicial = fase.get("descartes_pos")
        descartes_rect = descartes_surface.get_rect(midbottom=descartes_pos_inicial)

        hobbes_pos_inicial = fase.get("hobbes_pos")
        hobbes_rect = hobbes_surface.get_rect(midbottom=hobbes_pos_inicial)

        plataforma_pos_inicial = fase.get("plataforma")
        plataforma_rec = None

        if plataforma_pos_inicial:
            plataforma_rec = flying_surface.get_rect(midbottom=plataforma_pos_inicial)
            plataforma_hitbox = pygame.Rect(plataforma_rec.left - 5,
        plataforma_rec.bottom,  # desloca a hitbox 5 pixels para baixo
        plataforma_rec.width,
        10  # altura da hitbox
        )
        else:
            plataforma_rec = None
            plataforma_hitbox = None

        obstaculos_config = fase.get("obstaculos",[])
        obstaculos = []
        for config in obstaculos_config:
            tipo = config["tipo"]
            pos = config["pos"]
            escala = config.get("escala", (1.0, 1.0))  # valor padrão = sem escala
            rotacao = config.get("rotacao", 0)
            if tipo == "ground":
                surface = groundShield_surface
            elif tipo == "wood":
                surface = wood_surface
            else:
                continue
            largura = int(surface.get_width() * escala[0])
            altura = int(surface.get_height() * escala[1])
            surface = pygame.transform.scale(surface, (largura, altura))

            if rotacao != 0:
                surface = pygame.transform.rotate(surface, rotacao)

            rect = surface.get_rect(midbottom=pos)
            obstaculos.append({"surface": surface, "rect": rect})

        return (obstaculos, baggete_pos_inicial, baggete_rect,
                descartes_rect, hobbes_rect,
                baggete_pos_x, baggete_pos_y,
                0.0, 0.0, base_rect, cannon_rect, plataforma_rec, plataforma_hitbox)


    obstaculos, baggete_pos_inicial, baggete_rect, descartes_rect, hobbes_rect, baggete_pos_x, baggete_pos_y, ball_vel_x, ball_vel_y, base_rect, cannon_rect, plataforma_rec, plataforma_hitbox = iniciar_fase(fase_atual)

    is_pressing = False
    press_start_time = None
    last_power_ratio = 0
    can_launch = True
    trail = []
    equacao_texto = ""
    Pi_pixel = V_pixel = Pf_pixel = None
    Pi_plano = V_plano = Pf_plano = None
    coeficientes = None
    impacto_calculado = False

    baggete_frame_index = 0
    baggete_frame_timer = 0
    frame_duration = 50

    baggete_mask = pygame.mask.from_surface(baggete_frames[0])
    hobbes_mask = pygame.mask.from_surface(hobbes_surface)

    running = True
    
    while running:

        dt = clock.tick(60)

        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
             print(mouse_x,mouse_y)
             if btn_pause.collidepoint(event.pos):
                 acao = tela_pausa(screen, fonte, clock)
                 if acao == "menu":
                    # Voltar ao menu, sai do modo livre
                    return "menu"

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_p:

                    resposta = tela_pausa(screen, fonte, clock)

                    if resposta == "sair":
                        running = False
                        
                    elif resposta == "menu":
                        return
                    
                elif event.key == pygame.K_SPACE and can_launch:
                    press_start_time = pygame.time.get_ticks()
                    is_pressing = True

            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE and is_pressing and can_launch:
                (ball_vel_x, ball_vel_y, last_power_ratio, equacao_texto,
                 Pi_pixel, V_pixel, Pf_pixel,
                 Pi_plano, V_plano, Pf_plano,
                 coeficientes, impacto_calculado) = calcular_lancamento(
                    press_start_time, max_press_duration, max_power, baggete_rect, trail
                )
                is_pressing = False
                press_start_time = None
                can_launch = False

        if not can_launch:
            ball_vel_y += gravity
            baggete_pos_x += ball_vel_x
            baggete_pos_y += ball_vel_y
            baggete_rect.center = (int(baggete_pos_x), int(baggete_pos_y))
            if 0 <= baggete_rect.centerx <= LARGURA_TELA and 0 <= baggete_rect.centery <= ALTURA_TELA:
                trail.append(baggete_rect.center)

            if baggete_rect.bottom >= Y_CHÃO:
                baggete_pos_y = Y_CHÃO
                if not impacto_calculado and len(trail) >= 3:
                    (Pi_pixel, V_pixel, Pf_pixel,
                     Pi_plano, V_plano, Pf_plano,
                     coeficientes, equacao_texto) = calcular_raizes_e_equação(trail, Y_CHÃO, ORIGEM_PIXEL, ESCALA_X, ESCALA_Y)
                    
                    if V_pixel and V_pixel[1] < 0:
                        Pi_pixel = V_pixel = Pf_pixel = None
                        Pi_plano = V_plano = Pf_plano = None
                    
                baggete_pos_x, baggete_pos_y = baggete_pos_inicial
                baggete_rect.midbottom = baggete_pos_inicial
                ball_vel_x = 0
                ball_vel_y = 0
                can_launch = True
                trail = []

        if ball_vel_x != 0 or ball_vel_y != 0:
            baggete_frame_timer += dt * 2
            if baggete_frame_timer >= frame_duration:
                baggete_frame_timer = 0
                baggete_frame_index = (baggete_frame_index + 1) % len(baggete_frames)
        else:
            baggete_frame_index = 0

        current_baggete = baggete_frames[baggete_frame_index]
        baggete_mask = pygame.mask.from_surface(current_baggete)

        # Atualiza ângulo do canhão
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - cannon_rect.centerx
        dy = mouse_y - cannon_rect.centery
        cannon_angle = -math.degrees(math.atan2(dy, dx)) - 90
        cannon_surface_rotated = pygame.transform.rotate(cannon_surface, cannon_angle)
        cannon_rect = cannon_surface_rotated.get_rect(midbottom=(base_rect.midbottom[0]+20, base_rect.midbottom[1] - 40))

        # Atualiza e rotaciona a baggete antes do lançamento
        if can_launch:
            current_baggete = pygame.transform.rotate(current_baggete, cannon_angle)
            baggete_rect = current_baggete.get_rect(center=cannon_rect.center)
            baggete_pos_x = baggete_rect.centerx
            baggete_pos_y = baggete_rect.centery

        # Colisões
        offset = (hobbes_rect.left - baggete_rect.left, hobbes_rect.top - baggete_rect.top)
        if baggete_mask.overlap(hobbes_mask, offset):

            (baggete_pos_x, baggete_pos_y,
             ball_vel_x, ball_vel_y,
             can_launch, equacao_texto, impacto_calculado,
             trail,
             Pi_pixel, V_pixel, Pf_pixel,
             Pi_plano, V_plano, Pf_plano,
             coeficientes) = resetar_baggete(baggete_rect, baggete_pos_inicial)
            pygame.display.flip()
            resultado, fase_atual, dados_fase = gerenciar_proxima_fase(
                fase_atual, fases, screen, fonte, clock, iniciar_fase, tela_sucesso_fase, tela_fim_de_jogo
            )
            if resultado == "sair":
                running = False
            elif resultado == "menu":
                return
            elif resultado in ("reiniciar", "continuar") and dados_fase:
                (obstaculos, baggete_pos_inicial, baggete_rect, descartes_rect,
                 hobbes_rect, baggete_pos_x, baggete_pos_y,
                 ball_vel_x, ball_vel_y, base_rect, cannon_rect, plataforma_rec, plataforma_hitbox) = dados_fase

        for obs in obstaculos:
            if baggete_rect.colliderect(obs["rect"]):

                offset = (obs["rect"].left - baggete_rect.left, obs["rect"].top - baggete_rect.top)
                obst_mask = pygame.mask.from_surface(obs["surface"])

                if baggete_mask.overlap(obst_mask, offset):
                    (baggete_pos_x, baggete_pos_y,
                     ball_vel_x, ball_vel_y,
                     can_launch, equacao_texto, impacto_calculado,
                     trail,
                     Pi_pixel, V_pixel, Pf_pixel,
                     Pi_plano, V_plano, Pf_plano,
                     coeficientes) = resetar_baggete(baggete_rect, baggete_pos_inicial)
                    
                # Colisão com a parte inferior da plataforma
        if plataforma_hitbox and baggete_rect.colliderect(plataforma_hitbox):
            (baggete_pos_x, baggete_pos_y,
             ball_vel_x, ball_vel_y,
             can_launch, equacao_texto, impacto_calculado,
             trail,
             Pi_pixel, V_pixel, Pf_pixel,
             Pi_plano, V_plano, Pf_plano,
             coeficientes) = resetar_baggete(baggete_rect, baggete_pos_inicial)

        if (baggete_rect.right < 0 or baggete_rect.left > LARGURA_TELA or
                baggete_rect.bottom < 0 or baggete_rect.top > ALTURA_TELA):
            (baggete_pos_x, baggete_pos_y,
             ball_vel_x, ball_vel_y,
             can_launch, equacao_texto, impacto_calculado,
             trail,
             Pi_pixel, V_pixel, Pf_pixel,
             Pi_plano, V_plano, Pf_plano,
             coeficientes) = resetar_baggete(baggete_rect, baggete_pos_inicial)

        # DESENHO
        screen.blit(plane_surface_phaseMode, (0, 0))
        screen.blit(current_baggete, baggete_rect)
        screen.blit(cannon_surface_rotated, cannon_rect)
        screen.blit(base_surface, base_rect)
        screen.blit(descartes_surface, descartes_rect)
        screen.blit(hobbes_surface, hobbes_rect)
        if plataforma_rec:
            screen.blit(flying_surface,plataforma_rec)
        
        for obs in obstaculos:
            screen.blit(obs["surface"], obs["rect"])

        btn_pause = desenhar_botao_pause(screen)

        if coeficientes and Pi_plano and Pf_plano:
            desenhar_parabola(screen, coeficientes, Pi_plano, Pf_plano, ORIGEM_PIXEL, ESCALA_X, ESCALA_Y)

        if Pi_pixel and V_pixel and Pf_pixel:
            desenhar_pontos(screen, Pi_pixel, V_pixel, Pf_pixel)
            desenhar_legenda_pontos(screen, fonte, Pi_plano, V_plano, Pf_plano, Pi_pixel, V_pixel, Pf_pixel)

        desenhar_barra_forca(screen, is_pressing, press_start_time, last_power_ratio)
        pygame.display.flip()
