# ===== Inicialização =====
# ----- Importa e inicia pacotes
from os import path
from Classes.Player import *
from Classes.Sala import *
from Classes.Parede import *
from Classes.Espada import *
from Classes.Kamikaze import *  
from Classes.Dungeon import *   
import pygame
from math import *
import random
from config import *
from tela_inicial import *
from testes import tela_teste
from testes2 import tela_teste2


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
    if state == TESTES:
        print("Entrando no teste 1")
        state = tela_teste(tela)
    if state == TESTES2:
        print("Entrando no teste 2")
        state = tela_teste2(tela)
    
# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados 