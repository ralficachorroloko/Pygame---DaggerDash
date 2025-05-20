from Classes.Sala import Sala
from Classes.Kamikaze import Kamikaze
from Classes.Esqueleto import Esqueleto


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
SALAS_FIXAS = {
    "Spawn": {
        "nome": "Spawn",
        "imagem": "Spawn.png",
        "portas": {
            "centro": {
                "x": 610,
                "y": 288 - 32,
                "largura": 96,
                "altura": 80+32+16
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
    'Começo andar':{
        "nome": "Começo andar",
        "imagem": "Começo andar.png",
        "portas": {
                "direita": {
                "x": 784-20,
                "y": 280-64,
                "largura": 35,
                "altura": 96+32+16
            }
        },
        "paredes": [            
            (0, 0, 800, 64),      # Parede superior
            (0, 544, 800, 32),    # Parede inferior
            (0, 0, 32, 600),      # Parede esquerda
            (768, 0, 32, 600)     # Parede direita
        ]
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
}

SALAS_RANDOMIZADAS = {
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
        "inimigos": [
            (Esqueleto, 400, 300),  # Esqueleto no centro
            (Esqueleto, 600, 400),   # Esqueleto no canto inferior direito
            (Kamikaze, 500, 450, 3)
        ]
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

            (322, 33*8, 62*3, 29*4),

        ],
    }, 
        'Sala_estranha':{
        "imagem": "Sala estranha.png",
        "nome": "Sala_estranha",
        "portas": Default_portas,
        "paredes": [
            (0, 0, 800, 64),      # Parede superior
            (0, 544, 800, 32),    # Parede inferior
            (0, 0, 32, 600),      # Parede esquerda
            (768, 0, 32, 600),     # Parede direita

            (32*6, 32*5,31*15,63),
            (32*6, 32*11,31*15,63),

            (32*6, 32*7,31*4,31),
            (32*17, 32*7,31*4,31),

            (32*6, 32*10,31*4,31),
            (32*17, 32*10,31*4,31),
            
            
        ],
    }
}
# Matrizes das dungeons (7 dungeons lineares)
DUNGEON_MATRIZES = {
    1: [
        ["Spawn"],
    ],
    2: [
        ["Começo andar", "Sala_aberta", "sala_random", "Transição_andar"],
    ],
    3: [
        ["Começo andar", "sala_random", "sala_random", "Transição_andar"],
    ],
    4: [
        ["Começo andar", "sala_random", "sala_random", "Transição_andar"],
    ],
    5: [
        ["Começo andar", "sala_random", "sala_random", "Transição_andar"],
    ],
    6: [
        ["Começo andar", "sala_random", "sala_random", "Transição_andar"],
    ],
    7: [
        ["Começo andar", "sala_random", "sala_random", "Transição_andar"],
    ],
}

# Função para criar uma sala a partir do dicionário
def criar_sala(tipo_sala):
    if tipo_sala == 'sala_random':
        # Escolhe aleatoriamente uma sala do dicionário SALAS_RANDOMIZADAS
        import random
        tipo_sala = random.choice(list(SALAS_RANDOMIZADAS.keys()))
        dados = SALAS_RANDOMIZADAS[tipo_sala]
    elif tipo_sala in SALAS_FIXAS:
        dados = SALAS_FIXAS[tipo_sala]
    elif tipo_sala in SALAS_RANDOMIZADAS:
        dados = SALAS_RANDOMIZADAS[tipo_sala]
    else:
        return None

    inimigos = []
    if "inimigos" in dados:
        for inimigo_data in dados["inimigos"]:
            tipo_inimigo = inimigo_data[0]
            if tipo_inimigo == Kamikaze:
                inimigos.append(Kamikaze(*inimigo_data[1:]))
            elif tipo_inimigo == Esqueleto:
                inimigos.append(Esqueleto(*inimigo_data[1:]))
    
    # Cria a sala com as configurações personalizadas
    return Sala(
        dados['nome'], 
        dados["portas"], 
        inimigos=inimigos, 
        imagem_sala=dados.get('imagem'),
        paredes=dados.get('paredes', [])  # Lista de paredes personalizadas
    ) 