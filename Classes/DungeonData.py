from Classes.Sala import Sala
from Classes.Kamikaze import Kamikaze

# Dicionário de salas disponíveis para randomização
SALAS_DISPONIVEIS = {
    "Sala_aberta": {
        "imagem": "Sala aberta.png",
        "nome": "Sala de Inimigos 1",
        "portas": {"esquerda": True, "direita": True},
        "inimigos": [
            # (x, y, velocidade, tamanho, alcance, imagem)
            (400, 300, 2, (32, 32), 200, "kamikaze.png"),
            (500, 400, 2, (32, 32), 200, "kamikaze.png"),
        ]
    },
    "sala_inimigos_2": {
        "nome": "Sala de Inimigos 2",
        "portas": {"esquerda": True, "direita": True},
        "inimigos": [
            (300, 200, 2, (32, 32), 200, "kamikaze.png"),
            (600, 500, 2, (32, 32), 200, "kamikaze.png"),
            (450, 350, 2, (32, 32), 200, "kamikaze.png"),
        ]
    },
    # Adicione mais variações de salas aqui
}

# Matrizes das dungeons (7 dungeons lineares)
DUNGEON_MATRIZES = {
    1: [
        ["sala_spawn", "Sala_aberta", "sala_boss"],
    ],
    2: [
        ["sala_spawn", "Sala_aberta", "sala_inimigos_2", "sala_boss"],
    ],
    3: [
        ["sala_spawn", "Sala_aberta", "sala_inimigos_2", "Sala_aberta", "sala_boss"],
    ],
    4: [
        ["sala_spawn", "sala_inimigos_2", "Sala_aberta", "sala_inimigos_2", "Sala_aberta", "sala_boss"],
    ],
    5: [
        ["sala_spawn", "Sala_aberta", "sala_inimigos_2", "Sala_aberta", "sala_inimigos_2", "Sala_aberta", "sala_boss"],
    ],
    6: [
        ["sala_spawn", "sala_inimigos_2", "Sala_aberta", "sala_inimigos_2", "Sala_aberta", "sala_inimigos_2", "Sala_aberta", "sala_boss"],
    ],
    7: [
        ["sala_spawn", "Sala_aberta", "sala_inimigos_2", "Sala_aberta", "sala_inimigos_2", "Sala_aberta", "sala_inimigos_2", "Sala_aberta", "sala_boss"],
    ],
}

# Função para criar uma sala a partir do dicionário
def criar_sala(tipo_sala):
    if tipo_sala == "sala_spawn":
        return Sala("Spawn", {"esquerda": True, "direita": True})
    elif tipo_sala == "sala_boss":
        return Sala("Boss", {"esquerda": True, "direita": True})
    elif tipo_sala in SALAS_DISPONIVEIS:
        dados = SALAS_DISPONIVEIS[tipo_sala]
        inimigos = []
        for inimigo_data in dados["inimigos"]:
            inimigos.append(Kamikaze(*inimigo_data))
        return Sala(dados['nome'], dados["portas"], inimigos=inimigos, imagem_sala=dados.get('imagem'))
    return None 