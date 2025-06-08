from assets import base_surface, cannon_surface, baggete_frames

def construir_conjunto_canhao(base_midbottom):
    """
    Monta base, canhão e baguete a partir da posição da base (midbottom).
    """
    base_rect = base_surface.get_rect(midbottom=base_midbottom)
    
    # Ajuste do canhão relativo à base
    cannon_offset_x = 20
    cannon_offset_y = 40
    cannon_rect = cannon_surface.get_rect(midbottom=(
        base_rect.midbottom[0] + cannon_offset_x,
        base_rect.midbottom[1] - cannon_offset_y
    ))
    
    # A baguete inicia centralizada na boca do canhão
    baggete_surface = baggete_frames[0]
    baggete_rect = baggete_surface.get_rect(center=cannon_rect.center)

    return base_rect, cannon_rect, baggete_rect
# Vamos criar funções específicas para corrigir o Y de cada elemento visual, com base na diferença entre o visual e o real.
def gerar_funcoes_correcao_y():
    correcao = {
        "base": 31,
        "hobbes": 608 - 599,
        "descartes": 608 - 599,
        "ground": 606 - 599,
        "wood": 604.5 - 599,
    }

    # Funções geradas dinamicamente
    def corrigir_y_base(y): return y + correcao["base"]
    def corrigir_y_hobbes(y): return y + correcao["hobbes"]
    def corrigir_y_descartes(y): return y + correcao["descartes"]
    def corrigir_y_obstaculo_ground(y): return y + correcao["ground"]
    def corrigir_y_obstaculo_wood(y): return y + correcao["wood"]

    return {
        "corrigir_y_base": corrigir_y_base,
        "corrigir_y_hobbes": corrigir_y_hobbes,
        "corrigir_y_descartes": corrigir_y_descartes,
        "corrigir_y_obstaculo_ground": corrigir_y_obstaculo_ground,
        "corrigir_y_obstaculo_wood": corrigir_y_obstaculo_wood,
    }

# Executa para gerar e exibir as funções
funcoes_correcao = gerar_funcoes_correcao_y()
list(funcoes_correcao.keys())

def resetar_baggete(ball_rectangle, ball_start_pos):
    ball_pos_x, ball_pos_y = ball_start_pos
    ball_rectangle.midbottom = ball_start_pos
    ball_velocity_x = 0
    ball_velocity_y = 0
    can_launch = True
    equacao_texto = "Função indefinida"
    impacto_calculado = False
    trail = []

    Pi_pixel = V_pixel = Pf_pixel = None
    Pi_plano = V_plano = Pf_plano = None
    coeficientes = None

    return (
        ball_pos_x, ball_pos_y,
        ball_velocity_x, ball_velocity_y,
        can_launch, equacao_texto, impacto_calculado,
        trail,
        Pi_pixel, V_pixel, Pf_pixel,
        Pi_plano, V_plano, Pf_plano,
        coeficientes
    )