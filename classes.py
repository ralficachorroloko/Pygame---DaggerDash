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

class Sala:
    def __init__(self, nome, portas):
        #              'R1'  dicionario com {cima:True, baixo: False} etc..
        self.nome = nome
        self.portas = portas

    def desenhar(self, tela):
        # Limpa a tela com cor da sala
        tela.fill((30, 30, 30))  # fundo cinza escuro


        # Desenha portas
        if self.portas.get("cima"):
            pygame.draw.rect(tela, (200, 200, 200), (280, 0, 80, 20))  # topo
        if self.portas.get("baixo"):
            pygame.draw.rect(tela, (200, 200, 200), (280, 580, 80, 20))  # baixo
        if self.portas.get("esquerda"):
            pygame.draw.rect(tela, (200, 200, 200), (0, 280, 20, 80))  # esquerda
        if self.portas.get("direita"):
            pygame.draw.rect(tela, (200, 200, 200), (580, 280, 20, 80))  # direita

class Dungeon:
    def __init__(self):
        self.matriz = self.criar_dungeon()
        self.pos_x = 1
        self.pos_y = 1

    def criar_dungeon(self):
        # Cria uma matriz 3x3 de salas, com conexões (portas) definidas
        return [
            [None, Sala("R1", {"baixo": True}), None],
            [Sala("R2", {"direita": True}), Sala("START", {"esquerda": True, "direita": True, "baixo": True}), Sala("R3", {"esquerda": True})],
            [None, Sala("R4", {"cima": True, "direita": True}), Sala("EXIT", {"esquerda": True})]
        ]

    def sala_atual(self):
        return self.matriz[self.pos_y][self.pos_x]

    def mudar_sala(self, direcao):
        dx, dy = 0, 0
        if direcao == "cima":
            dy = -1
        elif direcao == "baixo":
            dy = 1
        elif direcao == "esquerda":
            dx = -1
        elif direcao == "direita":
            dx = 1

        novo_x = self.pos_x + dx
        novo_y = self.pos_y + dy

        if 0 <= novo_y < len(self.matriz) and 0 <= novo_x < len(self.matriz[0]):
            if self.matriz[novo_y][novo_x] is not None:
                self.pos_x = novo_x
                self.pos_y = novo_y
                print(f"Entrou na sala: {self.sala_atual().nome}")


        