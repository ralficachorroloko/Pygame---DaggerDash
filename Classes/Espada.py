import pygame
from os import path
from config import *
from math import *

class Espada:
    def __init__(self, player, mouse_pos, imagem):
        self.rect = player.rect
        self.duracao = 10
        
        # Calcula o ângulo entre o jogador e o mouse
        dx = mouse_pos[0] - player.rect.centerx
        dy = mouse_pos[1] - player.rect.centery
        angulo = atan2(dy, dx)
        
        # Define a área de ataque baseada no ângulo
        if -pi/4 <= angulo < pi/4:  # Direita (ângulo entre -45 e 45 graus)
            self.rect = pygame.Rect(player.rect.right, player.rect.y - 15, 30, player.rect.height + 30)
        elif pi/4 <= angulo < 3*pi/4:  # Baixo (ângulo entre 45 e 135 graus)
            self.rect = pygame.Rect(player.rect.x - 15, player.rect.bottom, player.rect.width + 30, 30)
        elif 3*pi/4 <= angulo < 5*pi/4:  # Esquerda (ângulo entre 135 e 225 graus)
            self.rect = pygame.Rect(player.rect.x - 30, player.rect.y - 15, 30, player.rect.height + 30)
        else:  # Cima (ângulo entre 225 e 315 graus)
            self.rect = pygame.Rect(player.rect.x - 15, player.rect.y - 30, player.rect.width + 30, 30)

        self.imagem = pygame.image.load(path.join("img", "player", imagem)).convert_alpha()
        

    def atualizar(self):
        self.duracao -= 1

    def esta_ativo(self):
        return self.duracao > 0
    
    def desenhar(self, tela):
        pygame.draw.rect(tela, (255, 255, 0), self.rect)

        