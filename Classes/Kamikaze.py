from os import path
from Classes.Player import Player   
import pygame
from config import *
from math import *

class Kamikaze:
    TAMANHO_PADRAO = (32, 32)
    ALCANCE_PADRAO = 200

    def __init__(self, x, y, velocidade):
        # Carrega duas imagens alternadas
        img1 = pygame.image.load(path.join("img", "kamikazze", "kami1.png")).convert_alpha()
        img2 = pygame.image.load(path.join("img", "kamikazze", "kami2.png")).convert_alpha()
        self.imagens = [
            pygame.transform.scale(img1, self.TAMANHO_PADRAO),
            pygame.transform.scale(img2, self.TAMANHO_PADRAO)
        ]

        self.img_atual = 0
        self.rect = pygame.Rect(x, y, *self.TAMANHO_PADRAO)
        self.velocidade = velocidade
        self.alcance = self.ALCANCE_PADRAO
        self.direcao = 1
        self.limite_esquerdo = x - 50
        self.limite_direito = x + 50
        self.em_patrulha = False

        self.anim_frame = 0
        self.anim_intervalo = 30

    def _colidiu_com_parede(self, paredes):
        for parede in paredes:
            if self.rect.colliderect(parede.rect):
                return True
        return False

    def atualizar(self, player, paredes):
        player_x, player_y = player.rect.center
        inimigo_x, inimigo_y = self.rect.center
        distancia = hypot(player_x - inimigo_x, player_y - inimigo_y)

        perseguindo = distancia <= self.alcance and distancia > 0

        velocidade = self.velocidade + 3 if perseguindo else self.velocidade
        dx = dy = 0

        if perseguindo:
            self.anim_intervalo = 8
            self.em_patrulha = False
            dir_x = player_x - inimigo_x
            dir_y = player_y - inimigo_y
            if distancia > 0:
                dx = (dir_x / distancia) * velocidade
                dy = (dir_y / distancia) * velocidade
        else:
            self.anim_intervalo = 20
            if not self.em_patrulha:
                self.limite_esquerdo = self.rect.x - 50
                self.limite_direito = self.rect.x + 50
                self.em_patrulha = True

            dx = self.direcao * self.velocidade
            dy = 0

            self.rect.x += dx
            if self._colidiu_com_parede(paredes):
                self.rect.x -= dx
                self.direcao *= -1  # Inverte a direção ao colidir

        # Movimento e verificação de colisão
        if dx != 0 or dy != 0:
            self.rect.x += dx
            if self._colidiu_com_parede(paredes):
                self.rect.x -= dx

            self.rect.y += dy
            if self._colidiu_com_parede(paredes):
                self.rect.y -= dy

        # Atualiza animação
        self.anim_frame += 1
        if self.anim_frame >= self.anim_intervalo:
            self.img_atual = (self.img_atual + 1) % 2
            self.anim_frame = 0

    def desenhar(self, tela):
        tela.blit(self.imagens[self.img_atual], self.rect)
