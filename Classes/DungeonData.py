from Classes.Sala import Sala
from Classes.Kamikaze import Kamikaze


Default_portas = {
            "esquerda": {
                "x": 0,
                "y": 280-64,
                "largura": 40,
                "altura": 96+32+16
            },
            "direita": {
                "x": 784-20,
                "y": 280-64,
                "largura": 35,
                "altura": 96+32+16
            }
}

# Dicionário de salas disponíveis para randomização
SALAS_DISPONIVEIS = {
    "Spawn": {
        "nome": "Spawn",
        "imagem": "Spawn.png",
        "portas": {
            "centro": {
                "x": 624,
                "y": 28,
                "largura": 64,
                "altura": 80
            }
        },
        "imagem": "Spawn.png",
        "paredes": [
            (0, 0, 800, 64),      # Parede superior
            (0, 536, 800, 64),    # Parede inferior
            (0, 0, 64, 600),      # Parede esquerda
            (736, 0, 64, 600)     # Parede direita
        ]
    },
    'Transição_andar':{
        "nome": "Transição de andar",
        "imagem": "Transição de andar.png",
        "portas": {
            "centro": {
                "x": 610,
                "y": 288 - 64,
                "largura": 96,
                "altura": 80+32+16
            },
            "esquerda": {
                "x": 0,
                "y": 280-64,
                "largura": 40,
                "altura": 96+32+16
                }
        },
        "paredes": [
            (0, 0, 800, 64),      # Parede superior
            (0, 544, 800, 32),    # Parede inferior
            (0, 0, 32, 600),      # Parede esquerda
            (768, 0, 32, 600)     # Parede direita
        ],
    },       
    "Sala_aberta": {
        "imagem": "Sala aberta.png",
        "nome": "Sala_aberta",
        "portas": Default_portas,
        "paredes": [
            (0, 0, 800, 64),      # Parede superior
            (0, 544, 800, 32),    # Parede inferior
            (0, 0, 32, 600),      # Parede esquerda
            (768, 0, 32, 600)     # Parede direita
        ],
    },
    'Sala_esqueletos': {
        "imagem": "Corredor esqueletos.png",
        "nome": "Sala_esqueletos",
        "portas": Default_portas,
        "paredes": [
            (0, 0, 800, 64),      # Parede superior
            (0, 536, 800, 32),    # Parede inferior
            (0, 0, 32, 600),      # Parede esquerda
            (768, 0, 32, 600),     # Parede direita

            (0, 32*5, 800, 30),     # transversal superior
            (0, 32*12-16, 800, 30+16)     # transversal superior
        ],
    },
    'Sala_retangulos': {
        "imagem": "Sala retangulos.png",
        "nome": "Sala_retangulos",
        "portas": Default_portas,
        "paredes": [
            (0, 0, 800, 64),      # Parede superior
            (0, 544, 800, 32),    # Parede inferior
            (0, 0, 32, 600),      # Parede esquerda
            (768, 0, 32, 600),     # Parede direita

            (256-32, 96+64, 64, 288+32),     # Retangulo menor
            (512+32, 96+32, 64+32, 288+64+16),     # Retangulo maior
        ],
    },
    'Sala_Buracos': {
        "imagem": "sala buracos.png",
        "nome": "Sala_Buracos",
        "portas": Default_portas,
        "paredes": [
            (0, 0, 800, 64),      # Parede superior
            (0, 544, 800, 32),    # Parede inferior
            (0, 0, 32, 600),      # Parede esquerda
            (768, 0, 32, 600),     # Parede direita

            (32*7, 32*5, 64, 64), #buraco 1
            (32*13, 32*5, 64, 64), #buraco 2
            (32*19, 32*5, 64, 64), #buraco 3

            (32*7, 32*11, 64, 64), #buraco 4
            (32*13, 32*11, 64, 64), #buraco 5
            (32*19, 32*11, 64, 64), #buraco 6
            
        ],
    },
    'Sala_besta': {
        "imagem": "Sala Besta.png",
        "nome": "Sala_besta",
        "portas": {
            "centro": {
                "x": 610,
                "y": 288 - 64,
                "largura": 96,
                "altura": 80+32+16
            },
            "esquerda": {
                "x": 0,
                "y": 280-64,
                "largura": 40,
                "altura": 96+32+16
                },
        },
        "paredes": [
            (0, 0, 800, 64),      # Parede superior
            (0, 544, 800, 32),    # Parede inferior
            (0, 0, 32, 600),      # Parede esquerda
            (768, 0, 32, 600),     # Parede direita

            (64,32*6,32*14,32),
            (96, 32*11,32*14, 32)
        ],
    },
    'Sala_dinheiro': {
        "imagem": "Sala dinheiro.png",
        "nome": "Sala_dinheiro",
        "portas": Default_portas,
        "paredes": [
            (0, 0, 800, 64),      # Parede superior
            (0, 544, 800, 32),    # Parede inferior
            (0, 0, 32, 600),      # Parede esquerda
            (768, 0, 32, 600),     # Parede direita

            (32*6, 32*5, 94, 62),
            (32*17, 31*5, 96, 62),
            (32*6, 32*13, 96, 64),
            (32*17, 32*13, 96, 64),

            (318, 32*8, 63*3, 31*4),

        ],
    }
}
# Matrizes das dungeons (7 dungeons lineares)
DUNGEON_MATRIZES = {
    1: [
        ["Sala_aberta", "Sala_dinheiro", "Transição_andar"],
    ],
    2: [
        [],
    ],
    3: [
        [],
    ],
    4: [
        [],
    ],
    5: [
        [],
    ],
    6: [
        [],
    ],
    7: [
        [],
    ],
}

# Função para criar uma sala a partir do dicionário
def criar_sala(tipo_sala):
    if tipo_sala in SALAS_DISPONIVEIS:
        dados = SALAS_DISPONIVEIS[tipo_sala]
        inimigos = []
        if "inimigos" in dados:
            for inimigo_data in dados["inimigos"]:
                inimigos.append(Kamikaze(*inimigo_data))
        # Cria a sala com as configurações personalizadas
        return Sala(
            dados['nome'], 
            dados["portas"], 
            inimigos=inimigos, 
            imagem_sala=dados.get('imagem'),
            paredes=dados.get('paredes', [])  # Lista de paredes personalizadas
        )
    return None 