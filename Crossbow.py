import pygame
from os import path
from config import *
from math import *

class Crossbow:
    def __init__(self, player, mouse_pos):
        self.player = player
        self.cooldown = 0
        self.cooldown_max = 30
        
        dx = mouse_pos[0] - player.rect.centerx
        dy = mouse_pos[1] - player.rect.centery
        self.angulo = atan2(dy, dx)
        
        self.imagem_base = pygame.image.load(path.join("img", "itens", "crossbow.png")).convert_alpha()
        self.imagem_base = pygame.transform.scale(self.imagem_base, (50, 50))
        
        self.largura_base = 50
        self.altura_base = 50
        
        self.atualizar_imagem()
        
    def atualizar_imagem(self):
        if -pi/4 <= self.angulo < pi/4:  # Direita
            self.imagem = pygame.transform.rotate(self.imagem_base, 0)
            self.rect = pygame.Rect(
                self.player.rect.right,
                self.player.rect.centery - self.largura_base/2,
                self.altura_base,
                self.largura_base
            )
        elif pi/4 <= self.angulo < 3*pi/4:  # Baixo
            self.imagem = pygame.transform.rotate(self.imagem_base, -90)
            self.rect = pygame.Rect(
                self.player.rect.centerx - self.largura_base/2,
                self.player.rect.bottom,
                self.largura_base,
                self.altura_base
            )
        elif 3*pi/4 <= self.angulo < 4*pi/4:  # Esquerda
            self.imagem = pygame.transform.rotate(self.imagem_base, 180)
            self.rect = pygame.Rect(
                self.player.rect.left - self.altura_base,
                self.player.rect.centery - self.largura_base/2,
                self.altura_base,
                self.largura_base
            )
        else:  # Cima
            self.imagem = pygame.transform.rotate(self.imagem_base, 90)
            self.rect = pygame.Rect(
                self.player.rect.centerx - self.largura_base/2,
                self.player.rect.top - self.altura_base,
                self.largura_base,
                self.altura_base
            )

    def atualizar(self):
        if self.cooldown > 0:
            self.cooldown -= 1
        self.atualizar_imagem()

    def pode_atirar(self):
        return self.cooldown == 0 and self.player.tem_arco
    
    def atirar(self):
        if self.pode_atirar():
            self.cooldown = self.cooldown_max
            self.player.estado = "bow"
            self.player.shoot_timer = self.player.shoot_duracao
            return True
        return False
    
    def desenhar(self, tela):
        if self.player.tem_arco:
            tela.blit(self.imagem, self.rect)
