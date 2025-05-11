import pygame
from os import path
from config import *

class Player:
    def __init__(self, x, y, imagem, velocidade, tamanho):
        img = pygame.image.load(path.join("img", "player", imagem)).convert_alpha()
        self.imagem = pygame.transform.scale(img, tamanho)
        self.rect = self.imagem.get_rect(topleft=(x, y))
        self.velocidade = velocidade 

    def desenhar(self, tela):
        tela.blit(self.imagem, self.rect)

    def mover(self, dx, dy):
        self.rect.x += dx * self.velocidade
        self.rect.y += dy * self.velocidade
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))

class Parede:
    def __init__(self, x, y, largura, altura):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.rect = pygame.Rect(x, y, largura, altura)
    
    def desenhar(self, tela, mostrar_hitbox=False):
        if mostrar_hitbox == True:
            pygame.draw.rect(tela, (255, 0, 0), self.rect)

        