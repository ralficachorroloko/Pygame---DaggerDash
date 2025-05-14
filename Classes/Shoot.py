import pygame
from os import path
from config import *
from math import *

class Shoot:
    def __init__(self, player, mouse_pos, imagem):
        self.velocidade = 10  # Velocidade do projétil

        # Calcula o ângulo entre o jogador e o mouse
        dx = mouse_pos[0] - player.rect.centerx
        dy = mouse_pos[1] - player.rect.centery
        angulo = atan2(dy, dx)

        # Salva a direção como componentes normalizados
        self.dx = cos(angulo)
        self.dy = sin(angulo)

        # Define a posição inicial do projétil na frente do player
        self.rect = pygame.Rect(player.rect.centerx, player.rect.centery, 10, 10)

        # Carrega a imagem do projétil
        self.imagem = pygame.image.load(path.join("img", "player", imagem)).convert_alpha()
        self.imagem = pygame.transform.scale(self.imagem, (10, 10))

    def atualizar(self):
        # Move o projétil na direção calculada
        self.rect.x += self.dx * self.velocidade
        self.rect.y += self.dy * self.velocidade

    def desenhar(self, tela):
        tela.blit(self.imagem, self.rect)