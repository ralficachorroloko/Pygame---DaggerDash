
import pygame
from os import path
from config import *
from math import *

class Espada:
    def __init__(self, player, duracao, direcao, imagem):
        self.rect = player.rect
        self.duracao = duracao
        if direcao == "w":
            # Golpe acima
            self.rect = pygame.Rect(player.rect.x, player.rect.y - 20, player.rect.width, 20)
        elif direcao == "s":
            # Golpe abaixo
            self.rect = pygame.Rect(player.rect.x, player.rect.bottom, player.rect.width, 20)
        elif direcao == "a":
            # Golpe à esquerda
            self.rect = pygame.Rect(player.rect.x - 20, player.rect.y, 20, player.rect.height)
        elif direcao == "d":
            # Golpe à direita
            self.rect = pygame.Rect(player.rect.right, player.rect.y, 20, player.rect.height)

        self.imagem = pygame.image.load(path.join("img", "player", imagem)).convert_alpha()
        

    def atualizar(self):
        self.duracao -= 1

    def esta_ativo(self):
        return self.duracao > 0
    
    def desenhar(self, tela):
        pygame.draw.rect(tela, (255, 255, 0), self.rect)

        