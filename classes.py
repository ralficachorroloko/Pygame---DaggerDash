import pygame
import os
from config import *

class Player:
    def __init__(self, x, y, largura, altura, cor, velocidade):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.cor = cor
        self.velocidade = velocidade

    def desenhar_player(self, tela):
        pygame.draw.rect(tela, self.cor, (self.x, self.y, self.largura, self.altura))

    def mover(self, dx, dy):
        dx *= self.velocidade
        dy *= self.velocidade
        self.x += dx
        self.y += dy
        self.x = max(0, min(self.x, WIDTH - self.largura))
        self.y = max(0, min(self.y, HEIGHT - self.altura))
        