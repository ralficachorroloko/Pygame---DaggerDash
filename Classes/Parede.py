import pygame
from config import *
from math import *

class Parede:
    def __init__(self, x, y, largura, altura):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.rect = pygame.Rect(x, y, largura, altura)
    
    def desenhar(self, tela, mostrar_hitbox=False):
 #       pygame.draw.rect(tela, (128, 128, 128), self.rect)  # Desenha a parede em cinza
        if mostrar_hitbox:
            pygame.draw.rect(tela, (255, 0, 0), self.rect, 2)  # Desenha a hitbox em vermelho