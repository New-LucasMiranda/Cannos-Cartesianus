from settings import Y_CHÃO
from game_utils import gerar_funcoes_correcao_y

funcoes_correcao = gerar_funcoes_correcao_y()

fases = [
     
              {
        "hobbes_pos": (1145, funcoes_correcao['corrigir_y_hobbes'](Y_CHÃO)),
        "base_pos": (175, funcoes_correcao['corrigir_y_base'](Y_CHÃO)),
        "descartes_pos": (55, funcoes_correcao['corrigir_y_descartes'](Y_CHÃO))
    },

    {
        "hobbes_pos": (1145, funcoes_correcao['corrigir_y_hobbes'](Y_CHÃO)),
        "base_pos": (175, funcoes_correcao['corrigir_y_base'](Y_CHÃO)),
        "descartes_pos": (55, funcoes_correcao['corrigir_y_descartes'](Y_CHÃO)),
        "obstaculos": [
            {"tipo": "ground", "pos": (435, funcoes_correcao['corrigir_y_obstaculo_ground'](Y_CHÃO))},
            {"tipo": "ground", "pos": (820, funcoes_correcao['corrigir_y_obstaculo_ground'](Y_CHÃO))}
        ],
    },

    {
        "hobbes_pos": (870, funcoes_correcao['corrigir_y_hobbes'](Y_CHÃO)),
        "base_pos": (400, funcoes_correcao['corrigir_y_base'](Y_CHÃO)),
        "descartes_pos": (275, funcoes_correcao['corrigir_y_descartes'](Y_CHÃO)),
        "obstaculos": [
            {"tipo": "wood", "pos": (545, funcoes_correcao['corrigir_y_obstaculo_wood'](Y_CHÃO)), "escala": (1.0, 2.5)},
            {"tipo": "wood", "pos": (710, funcoes_correcao['corrigir_y_obstaculo_wood'](Y_CHÃO)), "escala": (1.0, 2.5)}
        ],
    },

    {
        "hobbes_pos": (1030, funcoes_correcao['corrigir_y_hobbes'](200)),
        "base_pos": (380, funcoes_correcao['corrigir_y_base'](Y_CHÃO)),
        "descartes_pos": (310, funcoes_correcao['corrigir_y_descartes'](Y_CHÃO)),
        "plataforma": (1030, 225)
    },

     {
        "hobbes_pos": (1030, funcoes_correcao['corrigir_y_hobbes'](Y_CHÃO)),
        "base_pos": (345, funcoes_correcao['corrigir_y_base'](250)),
        "descartes_pos": (270, funcoes_correcao['corrigir_y_descartes'](250)),
        "plataforma": (330,275)
    },
     
     {
        "hobbes_pos": (1030, funcoes_correcao['corrigir_y_hobbes'](Y_CHÃO)),
        "base_pos": (315, funcoes_correcao['corrigir_y_base'](350)),
        "descartes_pos": (240, funcoes_correcao['corrigir_y_descartes'](350)),
        "plataforma": (300,375),
        "obstaculos": [  
            {"tipo": "wood", "pos": (710, funcoes_correcao['corrigir_y_obstaculo_wood'](Y_CHÃO)), "escala": (1.0, 2.5)},
            {"tipo": "wood", "pos": (545, funcoes_correcao['corrigir_y_obstaculo_wood'](200)), "escala": (1.0, 2.5),"rotacao": 180},
             {"tipo": "ground", "pos": (870, funcoes_correcao['corrigir_y_obstaculo_ground'](Y_CHÃO))}
        ],
    },

     {
        "hobbes_pos": (630, funcoes_correcao['corrigir_y_hobbes'](Y_CHÃO)),
        "base_pos": (400, funcoes_correcao['corrigir_y_base'](Y_CHÃO)),
        "descartes_pos": (275, funcoes_correcao['corrigir_y_descartes'](Y_CHÃO)),
        "obstaculos": [
            {"tipo": "wood", "pos": (545, funcoes_correcao['corrigir_y_obstaculo_wood'](Y_CHÃO)), "escala": (1.0, 2.5)},
            {"tipo": "wood", "pos": (710, funcoes_correcao['corrigir_y_obstaculo_wood'](Y_CHÃO)), "escala": (1.0, 2.5)},
            {"tipo": "wood", "pos": (545, funcoes_correcao['corrigir_y_obstaculo_wood'](200)), "escala": (1.0, 2.5),"rotacao": 180},
            {"tipo": "wood", "pos": (710, funcoes_correcao['corrigir_y_obstaculo_wood'](200)), "escala": (1.0, 2.5),"rotacao": 180}
        ],
    },
     
    {
        "hobbes_pos": (1000, funcoes_correcao['corrigir_y_hobbes'](Y_CHÃO)),
        "base_pos": (200, funcoes_correcao['corrigir_y_base'](Y_CHÃO)),
        "descartes_pos": (100, funcoes_correcao['corrigir_y_descartes'](Y_CHÃO)),
        "obstaculos": [
            {"tipo": "ground", "pos": (400, funcoes_correcao['corrigir_y_obstaculo_ground'](Y_CHÃO))},
            {"tipo": "wood", "pos": (900, funcoes_correcao['corrigir_y_obstaculo_wood'](170)), "escala": (1.0, 2.0),"rotacao": 180},
            {"tipo": "wood", "pos": (900, funcoes_correcao['corrigir_y_obstaculo_wood'](320)), "escala": (1.0, 2.0),"rotacao": 180},
            {"tipo": "wood", "pos": (900, funcoes_correcao['corrigir_y_obstaculo_wood'](470)), "escala": (1.0, 2.0),"rotacao": 180}
        ],
    },
]
