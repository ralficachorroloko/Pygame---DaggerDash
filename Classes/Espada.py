import pygame
from os import path
from config import *
from math import *

class Espada:
    def __init__(self, player, mouse_pos, imagem):
        self.player = player  # Guarda referência ao jogador
        self.duracao = 10
        
        # Calcula o ângulo entre o jogador e o mouse
        dx = mouse_pos[0] - player.rect.centerx
        dy = mouse_pos[1] - player.rect.centery
        angulo = atan2(dy, dx)
        
        # Guarda a direção do ataque
        self.direcao = angulo
        
        # Define a área de ataque baseada no ângulo
        if -pi/4 <= angulo < pi/4:  # Direita (ângulo entre -45 e 45 graus)
            self.rect = pygame.Rect(player.rect.right, player.rect.y - 15, 30, player.rect.height + 30)
        elif pi/4 <= angulo < 3*pi/4:  # Baixo (ângulo entre 45 e 135 graus)
            self.rect = pygame.Rect(player.rect.x - 15, player.rect.bottom, player.rect.width + 30, 30)
        elif 3*pi/4 <= angulo < 5*pi/4:  # Esquerda (ângulo entre 135 e 225 graus)
            self.rect = pygame.Rect(player.rect.x - 30, player.rect.y - 15, 30, player.rect.height + 30)
        else:  # Cima (ângulo entre 225 e 315 graus)
            self.rect = pygame.Rect(player.rect.x - 15, player.rect.y - 30, player.rect.width + 30, 30)

        # Carrega a imagem da espada
        self.imagem = pygame.image.load(path.join("img", "player", imagem)).convert_alpha()
        self.imagem = pygame.transform.scale(self.imagem, (30, 30))

    def atualizar(self):
        self.duracao -= 1
        
        # Atualiza a posição da espada baseada na posição do jogador
        if -pi/4 <= self.direcao < pi/4:  # Direita
            self.rect.left = self.player.rect.right
            self.rect.centery = self.player.rect.centery
        elif pi/4 <= self.direcao < 3*pi/4:  # Baixo
            self.rect.top = self.player.rect.bottom
            self.rect.centerx = self.player.rect.centerx
        elif 3*pi/4 <= self.direcao < 5*pi/4:  # Esquerda
            self.rect.right = self.player.rect.left
            self.rect.centery = self.player.rect.centery
        else:  # Cima
            self.rect.bottom = self.player.rect.top
            self.rect.centerx = self.player.rect.centerx

    def esta_ativo(self):
        return self.duracao > 0
    
    def desenhar(self, tela):
        pygame.draw.rect(tela, (255, 255, 0), self.rect)  # Desenha um retângulo amarelo

        