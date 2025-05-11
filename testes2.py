import pygame
import random
from os import path
from classes import *
from config import *

def tela_teste2(tela):
    # Criando a dungeon
    dungeon = Dungeon()
    
    # Criando as salas
    sala_inicial = Sala(
        "START",
        {"direita": True, "baixo": True},
        inimigos=[(400, 300, 1, (25, 25), 200, "idle.png")]
    )
    
    sala_direita = Sala(
        "R1",
        {"esquerda": True, "baixo": True},
        inimigos=[(200, 200, 1, (25, 25), 200, "idle.png")]
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
    pygame.mixer.music.load(path.join('8bitmusic.mp3'))
    pygame.mixer.music.play(-1)  

    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = QUIT
                return state
            
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_UP]:
            dy = -1
        if keys[pygame.K_DOWN]:
            dy = 1
        if keys[pygame.K_LEFT]:
            dx = -1
        if keys[pygame.K_RIGHT]:
            dx = 1
            
        if dx != 0 or dy != 0:
            dungeon.mover_jogador(dx, dy)

        # Update game state
        dungeon.atualizar()
        
        # Draw everything
        dungeon.desenhar(tela)
        
        pygame.display.flip() 