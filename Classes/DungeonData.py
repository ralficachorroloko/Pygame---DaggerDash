from Classes.Sala import Sala
from Classes.Kamikaze import Kamikaze

# Dicionário de salas disponíveis para randomização
SALAS_DISPONIVEIS = {
    "Spawn": {
        "nome": "Spawn",
        "imagem": "Spawn.png",
        "portas": {
            "centro": {
                "x": 384,  # (WIDTH - largura) // 2
                "y": 280,
                "largura": 32,
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
    "Sala_aberta": {
        "imagem": "Sala aberta.png",
        "nome": "Sala de Inimigos 1",
        "portas": {
            "esquerda": {
                "x": 0,
                "y": 280,
                "largura": 16,
                "altura": 80
            },
            "direita": {
                "x": 784,
                "y": 280,
                "largura": 16,
                "altura": 80
            }
        },
        "paredes": [
            (0, 0, 800, 64),      # Parede superior
            (0, 536, 800, 32),    # Parede inferior
            (0, 0, 32, 600),      # Parede esquerda
            (768, 0, 32, 600)     # Parede direita
        ],
        "inimigos": [
            (400, 300, 2, (32, 32), 200, "kamikaze.png"),
            (500, 400, 2, (32, 32), 200, "kamikaze.png"),
        ]
    },
}

# Matrizes das dungeons (7 dungeons lineares)
DUNGEON_MATRIZES = {
    1: [
        ["Spawn"],
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