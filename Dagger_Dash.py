# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
import random
from config import *


pygame.init()
pygame.mixer.init()

# ----- Gera tela principal
tela = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dagger Dash')

# while state != QUIT:
#     if state == INIT:
#         state = init_screen(tela)
    
# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados 