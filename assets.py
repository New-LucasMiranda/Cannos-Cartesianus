import pygame
#INTERFACES
plane_surface_freeMode = pygame.image.load('Graphics/Interfaçes/Plano de fundo (modo livre).png.jpg').convert()
plane_surface_phaseMode = pygame.image.load('Graphics/Interfaçes/Plano de fundo (modo fases).png.jpg').convert()
menu_surface = pygame.image.load('Graphics/Interfaçes/Fundo menu inicial 2_Prancheta 1.png').convert()
board_surface = pygame.image.load('Graphics/Interfaçes/quadro com giz 2_Prancheta 1.png').convert()
next_surface = pygame.image.load('Graphics/Interfaçes/tela de proxima fase_Prancheta 1.png').convert()
end_surface = pygame.image.load('Graphics/Interfaçes/Tela final_Prancheta 1.png').convert()
pause_surface = pygame.image.load('Graphics/Interfaçes/fundo menu Pausa (com fundo).png').convert()
button_surface = pygame.image.load('Graphics/Interfaçes/Baguete Menu_Prancheta 1.png').convert_alpha()
#PERSONAS
descartes_surface = pygame.image.load('Graphics/Personas/René Descartes_Prancheta 1.png').convert_alpha()
hobbes_surface = pygame.image.load('Graphics/Personas/Thomas Hobbes_Prancheta 1.png').convert_alpha()
#CENARY
groundShield_surface = pygame.image.load('Graphics/Cenary/Escudo proteção terrestre_Prancheta 1.png').convert_alpha()
baggete_surface = pygame.image.load('Graphics/Cenary/Escudo proteção terrestre_Prancheta 1.png').convert_alpha()
base_surface = pygame.image.load('Graphics/Cenary/Canhão Base_Prancheta 1.png').convert_alpha()
cannon_surface = pygame.image.load('Graphics/Cenary/Cannhao cano_Prancheta 1.png').convert_alpha()
wood_surface = pygame.image.load('Graphics/Cenary/Madeira cenrario_Prancheta 1.png').convert_alpha()
flying_surface = pygame.image.load('Graphics/Cenary/Plataforma aeria_Prancheta 1.png').convert_alpha()
#PROJECTILE
baggete_frames = [
    pygame.image.load(f'Graphics/Projectile/baggete {i+1}.png').convert_alpha()
    for i in range(8)
]

ball_start_pos = (599,599)
baggete_start_pos = (599,599)

arrow_surface = pygame.Surface((60, 10), pygame.SRCALPHA)
pygame.draw.polygon(arrow_surface, (0, 0, 255), [(0, 5), (50, 0), (60, 5), (50, 10)])
