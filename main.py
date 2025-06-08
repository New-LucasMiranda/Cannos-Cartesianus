import pygame
from sys import exit
from settings import screen, clock
import modo_livre
import modo_fases
from assets import menu_surface, button_surface

def menu_inicial():
    largura, altura = screen.get_size()
    running = True

    # Dimensões dos botões atualizadas
    largura_btn = 300
    altura_btn = 180

  # Largura da tela dividida em 3 partes iguais (bandeira da França)
    faixa_largura = largura // 3

    # Dimensões dos botões
    largura_btn = 300
    altura_btn = 180

    # Alinhamento vertical do Modo Livre e Modo Fases (mesmo Y)
    y_alinhado = 300

    # Botão "Modo Livre" no centro da faixa azul
    x_modo1 = faixa_largura // 2 - largura_btn // 2

    # Botão "Modo Fases" no centro da faixa vermelha
    x_modo2 = 2 * faixa_largura + faixa_largura // 2 - largura_btn // 2

    # Botão "Sair" no centro da faixa branca, mas mais abaixo
    x_sair = largura // 2 - largura_btn // 2
    y_sair = 500


    # Redimensiona a imagem do botão para 300x180
    button_img = pygame.transform.scale(button_surface, (largura_btn, altura_btn))

    # Fonte maior para os textos dos botões
    fonte_botao = pygame.font.SysFont(None, 48)

    while running:

        screen.blit(menu_surface, (0, 0))

        # Bandeira da França opaca a partir de Y=272.5
        bandeira_y = 272.5
        bandeira_altura = altura - bandeira_y
        faixa_largura = largura // 3
        alpha = 120

        azul_surface = pygame.Surface((faixa_largura, bandeira_altura), pygame.SRCALPHA)
        branco_surface = pygame.Surface((faixa_largura, bandeira_altura), pygame.SRCALPHA)
        vermelho_surface = pygame.Surface((faixa_largura, bandeira_altura), pygame.SRCALPHA)

        azul_surface.fill((0, 85, 164, alpha))
        branco_surface.fill((255, 255, 255, alpha))
        vermelho_surface.fill((239, 65, 53, alpha))

        screen.blit(azul_surface, (0, bandeira_y))
        screen.blit(branco_surface, (faixa_largura, bandeira_y))
        screen.blit(vermelho_surface, (2 * faixa_largura, bandeira_y))

        mouse_pos = pygame.mouse.get_pos()

        # Define retângulos para detecção de clique e hover
        btn_modo1 = pygame.Rect((x_modo1, y_alinhado), (largura_btn, altura_btn))
        btn_modo2 = pygame.Rect((x_modo2, y_alinhado), (largura_btn, altura_btn))
        btn_sair = pygame.Rect((x_sair, y_sair), (largura_btn, altura_btn))

        # Checa hover para escurecer o botão um pouco
        def aplicar_hover_mascara(surface, rect):
            if rect.collidepoint(mouse_pos):
                # Cria uma cópia do botão original para manipular sem afetar o original
                hover_img = surface.copy()

                # Clareia cada pixel visível (com alpha > 0)
                for x in range(hover_img.get_width()):
                    for y in range(hover_img.get_height()):
                        r, g, b, a = hover_img.get_at((x, y))
                        if a > 0:  # Só clareia se o pixel for visível
                            r = min(r + 30, 255)
                            g = min(g + 30, 255)
                            b = min(b + 30, 255)
                            hover_img.set_at((x, y), (r, g, b, a))

            screen.blit(hover_img, rect.topleft)

        # Desenha os botões com a imagem redimensionada
        screen.blit(button_img, btn_modo1.topleft)
        screen.blit(button_img, btn_modo2.topleft)
        screen.blit(button_img, btn_sair.topleft)

        # Renderiza textos dos botões e centraliza

# Em vez de blit + aplicar_hover separados, use apenas isso:
        if btn_modo1.collidepoint(mouse_pos):
            aplicar_hover_mascara(button_img, btn_modo1)
        else:
            screen.blit(button_img, btn_modo1.topleft)

        if btn_modo2.collidepoint(mouse_pos):
            aplicar_hover_mascara(button_img, btn_modo2)
        else:
            screen.blit(button_img, btn_modo2.topleft)

        if btn_sair.collidepoint(mouse_pos):
            aplicar_hover_mascara(button_img, btn_sair)
        else:
            screen.blit(button_img, btn_sair.topleft)

        # Renderiza textos dos botões e centraliza

        texto_modo1 = fonte_botao.render("Modo Livre", True, (255, 255, 255))
        texto_modo2 = fonte_botao.render("Modo Fases", True, (255, 255, 255))
        texto_sair = fonte_botao.render("Sair", True, (255, 255, 255))

        screen.blit(texto_modo1, texto_modo1.get_rect(center=btn_modo1.center))
        screen.blit(texto_modo2, texto_modo2.get_rect(center=btn_modo2.center))
        screen.blit(texto_sair, texto_sair.get_rect(center=btn_sair.center))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_modo1.collidepoint(event.pos):
                    resultado = modo_livre.run_modo_livre()
                    if resultado == "menu":
                        continue
                elif btn_modo2.collidepoint(event.pos):
                    resultado = modo_fases.run_modo_fases()
                    if resultado == "menu":
                        continue
                elif btn_sair.collidepoint(event.pos):
                    running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    exit()


if __name__ == "__main__":
    menu_inicial()
