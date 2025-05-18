from os import path
import pygame
from math import *
from config import *

class Flecha:
    def __init__(self, x, y, dx, dy, velocidade, alcance):
        self.imagem_original = pygame.image.load(path.join("img", "esqueleto", "flecha arqueiro.png")).convert_alpha()
        self.tamanho_flecha = (45, 15)
        self.imagem_original = pygame.transform.scale(self.imagem_original, self.tamanho_flecha)
        self.rect = pygame.Rect(x, y, self.tamanho_flecha[0], self.tamanho_flecha[1])
        self.dx = dx
        self.dy = dy
        self.velocidade = velocidade
        self.distancia_percorrida = 0
        self.alcance = alcance
        
        self.angulo = degrees(atan2(dy, dx))
        self.atualizar_rotacao()
        
        self.rect.centerx = x
        self.rect.centery = y

    def atualizar_rotacao(self):
        self.imagem_rotacionada = pygame.transform.rotate(self.imagem_original, -self.angulo)
        nrect = self.imagem_rotacionada.get_rect()
        nrect.center = (self.rect.centerx, self.rect.centery)
        self.rect = nrect

    def atualizar(self):
        mx = self.dx * self.velocidade
        my = self.dy * self.velocidade
        self.rect.centerx += mx
        self.rect.centery += my
        self.distancia_percorrida += sqrt(mx**2 + my**2)
        return self.distancia_percorrida >= self.alcance

    def pinta(self, tela):
        tela.blit(self.imagem_rotacionada, self.rect)

class Esqueleto:
    def __init__(self, x, y):
        self.imagem_standby = pygame.image.load(path.join("img", "esqueleto", "Esqueleto stand by.png")).convert_alpha()
        self.imagem_atirando = pygame.image.load(path.join("img", "esqueleto", "Esqueleto atirando.png")).convert_alpha()
        
        self.tamanho = (50, 50)
        self.imagem_standby = pygame.transform.scale(self.imagem_standby, self.tamanho)
        self.imagem_atirando = pygame.transform.scale(self.imagem_atirando, self.tamanho)
        
        self.imagem_atual = self.imagem_standby
        
        self.rect = pygame.Rect(x, y, self.tamanho[0], self.tamanho[1])
        
        self.vida = 100
        self.velocidade_flecha = 7
        self.alcance_flecha = 400
        self.alcance_visao = 300  
        self.tempo_cd = 60  
        self.tempo_ultimo_tiro = 0
        self.flechas = []  
        self.player_norange = False

    def detectar_player(self, player):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distancia = hypot(dx, dy)
        
        self.player_detectado = distancia <= self.alcance_visao
        
        self.imagem_atual = self.imagem_atirando if self.player_detectado else self.imagem_standby
        
        return distancia

    def atirar(self, player):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        
        distancia = hypot(dx, dy)
        if distancia > 0:
            dx = dx / distancia
            dy = dy / distancia
            flecha = Flecha(self.rect.centerx,self.rect.centery,dx,dy,self.velocidade_flecha,self.alcance_flecha)
            self.flechas.append(flecha)

    def atualizar(self, player):
        self.detectar_player(player)
        if self.player_detectado:
            self.tempo_ultimo_tiro += 1
            if self.tempo_ultimo_tiro >= self.tempo_cd:
                self.atirar(player)
                self.tempo_ultimo_tiro = 0
        flechas_para_remover = []
        for flecha in self.flechas:
            if flecha.atualizar():
                flechas_para_remover.append(flecha)
        for flecha in flechas_para_remover:
            self.flechas.remove(flecha)

    def receber_dano(self, dano):
        self.vida -= dano
        return self.vida <= 0

    def pinta(self, tela):
        tela.blit(self.imagem_atual, self.rect)
        for flecha in self.flechas:
            flecha.pinta(tela)
