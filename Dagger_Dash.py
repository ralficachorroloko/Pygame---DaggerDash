# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
import random
from config import *
from tela_inicial import *


pygame.init()
pygame.mixer.init()

# ----- Gera tela principal
tela = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dagger Dash')

state = INICIO

while state != QUIT:
    if state == INICIO:
        state = tela_inicio(tela)
    
# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados 