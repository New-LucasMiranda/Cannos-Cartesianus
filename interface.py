import pygame
from assets import next_surface, button_surface, end_surface, pause_surface

def aplicar_hover_mascara(screen, surface, rect):
    hover_img = surface.copy()
    for x in range(hover_img.get_width()):
        for y in range(hover_img.get_height()):
            r, g, b, a = hover_img.get_at((x, y))
            if a > 0:
                r = min(r + 30, 255)
                g = min(g + 30, 255)
                b = min(b + 30, 255)
                hover_img.set_at((x, y), (r, g, b, a))
    screen.blit(hover_img, rect.topleft)

def desenha_botao(screen, fonte, texto, rect, imagem_base, cor_texto=(0, 0, 0)):
    mouse_pos = pygame.mouse.get_pos()
    if rect.collidepoint(mouse_pos):
        aplicar_hover_mascara(screen, imagem_base, rect)
    else:
        screen.blit(imagem_base, rect.topleft)
    texto_render = fonte.render(texto, True, cor_texto)
    screen.blit(texto_render, texto_render.get_rect(center=rect.center))

def tela_pausa(screen, fonte, clock):

    largura, altura = screen.get_size()

    # Tamanho e posição do pop-up
    popup_w, popup_h = 400, 250
    popup_x = (largura - popup_w) // 2
    popup_y = (altura - popup_h) // 2
    popup_rect = pygame.Rect(popup_x, popup_y, popup_w, popup_h)

    # Carrega e redimensiona a imagem de fundo do pop-up
    fundo_popup = pygame.transform.scale(pause_surface, (popup_w, popup_h))

    # Configuração dos botões
    botao_w, botao_h = 300, 50
    espacamento = 20

    btn_continuar = pygame.Rect(popup_x + (popup_w - botao_w) // 2, popup_y + 90, botao_w, botao_h)
    btn_menu = pygame.Rect(popup_x + (popup_w - botao_w) // 2, btn_continuar.bottom + espacamento, botao_w, botao_h)

    # Redimensiona imagem de botão
    button_img = pygame.transform.scale(button_surface, (botao_w, botao_h))

    while True:

        screen.blit(fundo_popup, popup_rect.topleft)  # Fundo do pop-up

        desenha_botao(screen, fonte, "Continuar (C)", btn_continuar, button_img)
        desenha_botao(screen, fonte, "Voltar ao Menu (M)", btn_menu, button_img)

        # Título
        texto_pausa = fonte.render("PAUSADO", True, (0, 0, 0))
        screen.blit(texto_pausa, texto_pausa.get_rect(center=(popup_rect.centerx, popup_rect.top + 50)))

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "menu"

            elif event.type == pygame.KEYDOWN:
                tecla = pygame.key.name(event.key).lower()
                if tecla == 'c':
                    return "continuar"
                elif tecla == 'm' or tecla == 'escape':
                    return "menu"

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_continuar.collidepoint(event.pos):
                    return "continuar"
                elif btn_menu.collidepoint(event.pos):
                    return "menu"


def desenhar_botao_pause(screen):
    largura, altura = screen.get_size()
    btn_tam = 50
    margem = 10
    btn_pause = pygame.Rect(largura - btn_tam - margem, margem, btn_tam, btn_tam)

    # Desenhar botão (cinza com hover simples)
    mouse_pos = pygame.mouse.get_pos()
    cor = (120, 120, 120) if btn_pause.collidepoint(mouse_pos) else (70, 70, 70)
    pygame.draw.rect(screen, cor, btn_pause, border_radius=8)

    # Desenhar ícone de pausa (duas barras)
    barra_largura = 10
    espacamento = 10
    barra_altura = 30
    x1 = btn_pause.x + 10
    x2 = x1 + barra_largura + espacamento
    y = btn_pause.y + (btn_tam - barra_altura)//2

    pygame.draw.rect(screen, (255, 255, 255), (x1, y, barra_largura, barra_altura))
    pygame.draw.rect(screen, (255, 255, 255), (x2, y, barra_largura, barra_altura))

    return btn_pause

def tela_sucesso_fase(screen, fonte, clock, numero_fase):
    largura, altura = screen.get_size()

    # Dimensões do pop-up
    popup_w, popup_h = 500, 300
    popup_rect = pygame.Rect((largura - popup_w) // 2, (altura - popup_h) // 2, popup_w, popup_h)

    # Carrega e redimensiona o fundo do pop-up
    fundo_popup = pygame.transform.scale(next_surface, (popup_w, popup_h))

    # Configuração dos botões
    botao_largura = popup_w - 50
    botao_altura = 50
    espacamento = 15

    btn_proxima = pygame.Rect(popup_rect.left + 20, popup_rect.top + 114, botao_largura, botao_altura)
    btn_reiniciar = pygame.Rect(popup_rect.left + 20, btn_proxima.bottom + espacamento, botao_largura, botao_altura)
    btn_menu = pygame.Rect(popup_rect.left + 20, btn_reiniciar.bottom + espacamento, botao_largura, botao_altura)

    # Redimensiona imagem do botão
    button_img = pygame.transform.scale(button_surface, (botao_largura, botao_altura))

    while True:
        screen.blit(fundo_popup, popup_rect.topleft)

        # Sobreposição vermelha translúcida no pop-up
        verde_surface = pygame.Surface((popup_w, popup_h), pygame.SRCALPHA)
        verde_surface.fill((57, 255, 40, 100))
        screen.blit(verde_surface, popup_rect.topleft)

        # Título
        titulo = fonte.render(f"Fase {numero_fase} concluída!", True, (0, 0, 0))
        screen.blit(titulo, (660,popup_rect.top + 40))

        desenha_botao(screen, fonte, "Próxima fase (Enter)", btn_proxima, button_img, (255, 255, 255))
        desenha_botao(screen, fonte, "Reiniciar fase (R)", btn_reiniciar, button_img, (255, 255, 255))
        desenha_botao(screen, fonte, "Voltar ao Menu (M)", btn_menu, button_img, (255, 255, 255))

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "menu"

            elif event.type == pygame.KEYDOWN:
                tecla = pygame.key.name(event.key).lower()
                if tecla == 'return':
                    return "proxima"
                elif tecla == 'r':
                    return "reiniciar"
                elif tecla == 'm' or tecla == 'escape':
                    return "menu"

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_proxima.collidepoint(event.pos):
                    return "proxima"
                elif btn_reiniciar.collidepoint(event.pos):
                    return "reiniciar"
                elif btn_menu.collidepoint(event.pos):
                    return "menu"


def tela_fim_de_jogo(screen, fonte, clock):
    largura, altura = screen.get_size()

    # Dimensões e posição do pop-up
    popup_w, popup_h = 500, 300
    popup_x = (largura - popup_w) // 2
    popup_y = (altura - popup_h) // 2
    popup_rect = pygame.Rect(popup_x, popup_y, popup_w, popup_h)

    # Fundo do pop-up
    fundo_popup = pygame.transform.scale(end_surface, (popup_w, popup_h))

    # Configuração dos botões
    botao_altura = 50
    botao_largura = popup_w - 40
    espaco_entre = 15

    btn_reiniciar = pygame.Rect(popup_x + 20, popup_y + 138, botao_largura, botao_altura)
    btn_menu = pygame.Rect(popup_x + 20, btn_reiniciar.bottom + espaco_entre, botao_largura, botao_altura)

    # Redimensiona imagem do botão
    button_img = pygame.transform.scale(button_surface, (botao_largura, botao_altura))

    while True:
        # Fundo do pop-up
        screen.blit(fundo_popup, popup_rect.topleft)

        # Sobreposição vermelha translúcida no pop-up
        vermelho_surface = pygame.Surface((popup_w, popup_h), pygame.SRCALPHA)
        vermelho_surface.fill((255, 100, 100, 100))
        screen.blit(vermelho_surface, popup_rect.topleft)

        # Título
        fim = fonte.render("Fim de jogo!", True, (0, 0, 0))
        screen.blit(fim, (730,popup_rect.top + 40))

        desenha_botao(screen, fonte, "Reiniciar jogo (R)", btn_reiniciar, button_img, (255, 255, 255))
        desenha_botao(screen, fonte, "Voltar ao Menu (M)", btn_menu, button_img, (255, 255, 255))

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "menu"

            elif event.type == pygame.KEYDOWN:
                tecla = pygame.key.name(event.key).lower()
                if tecla == 'r':
                    return "reiniciar"
                elif tecla == 'm' or tecla == 'escape':
                    return "menu"

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_reiniciar.collidepoint(event.pos):
                    return "reiniciar"
                elif btn_menu.collidepoint(event.pos):
                    return "menu"


def gerenciar_proxima_fase(fase_atual, fases, screen, fonte, clock, iniciar_fase, tela_sucesso_fase, tela_fim_de_jogo):
    if fase_atual < len(fases) - 1:
        resposta = tela_sucesso_fase(screen, fonte, clock, fase_atual + 1)
        if resposta == "sair":
            return "sair", fase_atual, None
        elif resposta == "menu":
            return "menu", fase_atual, None
        elif resposta == "reiniciar":
            return "reiniciar", fase_atual, iniciar_fase(fase_atual)
        elif resposta == "proxima":
            fase_atual += 1
            return "continuar", fase_atual, iniciar_fase(fase_atual)
    else:
        resposta_fim = tela_fim_de_jogo(screen, fonte, clock)
        if resposta_fim == "sair":
            return "sair", fase_atual, None
        elif resposta_fim == "menu":
            return "menu", fase_atual, None
        elif resposta_fim == "reiniciar":
            fase_atual = 0
            return "reiniciar", fase_atual, iniciar_fase(fase_atual)
    
    return "continuar", fase_atual, None
