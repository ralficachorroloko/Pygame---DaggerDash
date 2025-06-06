from os import path
import pygame
from math import *

# Dados gerais do jogo.
WIDTH = 800 # Largura da tela
HEIGHT = 576 # Altura da tela
FPS = 60 # Frames por segundo

# Define algumas variáveis com as cores básicas
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Estados para controle do fluxo da aplicação
INICIO = 0
MAPA = 1
QUIT = 2

VITORIA = 3  #  estado para vitória
JOGO = 4  #  estado para o jogo
DUNGEON = 5  #  estado para fluxo de Dungeon
GAME_OVER = 6  #  estado para a tela de game over
TUTORIAL = 7  #  estado para a tela de tutorial