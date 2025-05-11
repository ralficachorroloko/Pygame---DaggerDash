import pygame
from os import path
from config import *
from math import *

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

class Kamikaze:
    def __init__(self, x, y, velocidade, tamanho, alcance, imagem):
        img = pygame.image.load(path.join("img", "player", imagem)).convert_alpha()
        self.imagem = pygame.transform.scale(img, tamanho)
        self.rect = pygame.Rect(x, y, tamanho[0], tamanho[1])
        self.velocidade = velocidade
        self.alcance = alcance
        self.direcao = 1
        self.limite_esquerdo = x - 50
        self.limite_direito = x + 50
        self.em_patrulha = False

    def atualizar(self, player):
        alcance = self.alcance
        velocidade = self.velocidade
        player_x = player.rect.x
        player_y = player.rect.y
        inimigo_x, inimigo_y = self.rect.x, self.rect.y
        distancia = hypot(player_x - inimigo_x, player_y - inimigo_y)

        #PERSEGUICAO

        if distancia <= alcance:
            self.em_patrulha = False
            velocidade += 3
            dx = player_x - inimigo_x
            dy = player_y - inimigo_y
            distancia = hypot(dx, dy)
            dx /= distancia
            dy /= distancia
            self.rect.x += dx * velocidade
            self.rect.y += dy * velocidade

        #WANDER

        else:
            if not self.em_patrulha:
                self.limite_esquerdo = self.rect.x - 50
                self.limite_direito = self.rect.x + 50
                self.em_patrulha = True  

            self.rect.x += self.direcao * self.velocidade

            if self.rect.left <= self.limite_esquerdo or self.rect.right >= self.limite_direito:
                self.direcao *= -1

    def desenhar(self, tela):
        tela.blit(self.imagem, self.rect)

        

        