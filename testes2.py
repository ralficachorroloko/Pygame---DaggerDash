from os import path
from Classes.Player import *
from Classes.Sala import *
from Classes.Parede import *
from Classes.Espada import *
from Classes.Kamikaze import *
from Classes.Dungeon import *
from Classes.Shoot import *
import pygame
from config import *
from math import *

def tela_teste2(tela):
    # Criando a dungeon
    dungeon = Dungeon()
    
    # Criando as salas
    sala_inicial = Sala(
        "Spawn",
        {"direita": True, "baixo": True},
        imagem_sala='Spawn.png'  # Adicionando uma parede no meio da sala
    )
    
    sala_direita = Sala(
        "R1",
        {"esquerda": True, "baixo": True},
        inimigos=[(200, 200, 1, (25, 25), 200, "idle.png"),(400, 300, 1, (25, 25), 200, "idle.png")]
    )
    
    sala_baixo = Sala(
        "R2",
        {"cima": True, "direita": True},
        inimigos=[(300, 400, 1, (25, 25), 200, "idle.png")]
    )
    
    sala_diagonal = Sala(
        "R3",
        {"cima": True, "esquerda": True},
        inimigos=[(400, 300, 1, (25, 25), 200, "idle.png")]
    )
    
    # Adicionando as salas à dungeon
    dungeon.adicionar_sala(sala_inicial, 0, 0)    # Sala inicial
    dungeon.adicionar_sala(sala_direita, 1, 0)    # Sala à direita
    dungeon.adicionar_sala(sala_baixo, 0, 1)      # Sala abaixo
    dungeon.adicionar_sala(sala_diagonal, 1, 1)   # Sala diagonal

    pygame.mixer.init()
    pygame.mixer.music.load(path.join('sons/8bitmusic.mp3'))
    pygame.mixer.music.play(-1)  

    clock = pygame.time.Clock()
    espada = None  # Inicializa sem espada
    jogador = dungeon.player
    shoots = []  # Lista para armazenar os tiros
    jogador.tem_arco = True  # Remove esta linha se quiser desbloquear o arco depois
    cooldown_shoot = 0  # Controle de tempo entre tiros
    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = QUIT
                return state
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not espada:  # 1 é o botão esquerdo do mouse
                    espada = Espada(jogador, pygame.mouse.get_pos(), "idle.png")

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_w]:
            dy = -1
            jogador.direcao = "w"
        if keys[pygame.K_s]:
            dy = 1
            jogador.direcao = "s"
        if keys[pygame.K_a]:
            dx = -1
            jogador.direcao = "a"
        if keys[pygame.K_d]:
            dx = 1
            jogador.direcao = "d"
        if keys[pygame.K_LSHIFT]:
            jogador.dash()
            
        if dx != 0 or dy != 0:
            dungeon.passagem_porta(dx, dy)

        # --- Controle de Tiro com botão direito do mouse ---
        if pygame.mouse.get_pressed()[2] and jogador.tem_arco and cooldown_shoot == 0:
            shoots.append(Shoot(jogador, pygame.mouse.get_pos(), "idle.png"))  # Substitua pela imagem da flecha
            cooldown_shoot = 15  # Controle de intervalo entre os tiros

        if cooldown_shoot > 0:
            cooldown_shoot -= 1

        # Atualiza tiros existentes
        for shoot in shoots[:]:
            shoot.atualizar()
            # Remove se sair da tela
            if not tela.get_rect().colliderect(shoot.rect):
                shoots.remove(shoot)

        # Update game state
        dungeon.atualizar()
        jogador.atualizar()
        
        # Draw everything
        tela.fill((0, 0, 0))  # Limpa a tela com preto
        dungeon.desenhar(tela)  # Primeiro desenha a dungeon
        
        # Desenha a espada por último para ficar por cima
        if espada and espada.esta_ativo():
            espada.desenhar(tela)
            espada.atualizar()
        else:
            espada = None  # Destrói a espada se não estiver mais ativa

        # Desenha os tiros
        for shoot in shoots:
            shoot.desenhar(tela)
        
        pygame.display.flip()

