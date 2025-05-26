# ===== Inicialização =====
# ----- Importa e inicia pacotes
"""
Arquivo principal do jogo Dagger Dash.

Este arquivo contém o loop principal do jogo que gerencia as diferentes telas
e estados do jogo (tela inicial, gameplay, game over, vitória).
"""

from os import path
from Classes.Player import Player   
from Classes.Sala import Sala
from Classes.Parede import Parede
from Classes.Espada import Espada
from Classes.Kamikaze import Kamikaze  
from Classes.Dungeon import Dungeon   
import pygame
from math import *
import random
from config import *

from tela_inicial import *
from Game_loop import tela_jogo
from Classes.Esqueleto import *
from game_over import tela_game_over
from tela_vitoria import tela_vitoria


pygame.init()
pygame.mixer.init()

# ----- Gera tela principal
tela = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dagger Dash')

state = INICIO
print("Estado inicial:", state)

while state != QUIT:
    print("Estado atual:", state)
    if state == INICIO:
        print("Entrando na tela inicial")
        state = tela_inicio(tela)
    elif state == JOGO:
        print("Entrando no jogo")
        state = tela_jogo(tela)
    elif state == GAME_OVER:
        print("Entrando na tela de Game Over")
        state = tela_game_over(tela)
    elif state == VITORIA:
        print("Entrando na tela de Vitória")
        state = tela_vitoria(tela)
    
# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados 