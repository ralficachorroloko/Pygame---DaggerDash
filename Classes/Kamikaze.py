from os import path
from Classes.Player import Player   
import pygame
from config import *
from math import *
from itens import criar_item_aleatorio, rolar_raridade
import random

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

        # Sistema de knockback e contador de flechas
        self.knockback = [0, 0]  # [dx, dy] do knockback
        self.knockback_forca = 5  # Força do knockback
        self.knockback_duracao = 10  # Frames que o knockback dura
        self.knockback_timer = 0  # Timer do knockback
        self.flechas_acertadas = 0  # Contador de flechas que acertaram

        self.drop_chance = 0.2  # 20% de chance de dropar um item (1 em 5)

    def receber_dano(self, dano, direcao=None):
        self.flechas_acertadas += 1
        
        # Aplica knockback se uma direção foi fornecida
        if direcao:
            self.knockback = [direcao[0] * self.knockback_forca, direcao[1] * self.knockback_forca]
            self.knockback_timer = self.knockback_duracao
        
        # Se morreu, tenta dropar um item
        if self.flechas_acertadas >= 2:
            if random.random() < self.drop_chance:
                return True, self.tentar_drop()
            return True, None
        return False, None

    def tentar_drop(self):
        # Se passou no teste de chance (10%), o drop é garantido
        raridade = rolar_raridade()
        return criar_item_aleatorio()

    def _colidiu_com_parede(self, paredes):
        for parede in paredes:
            if self.rect.colliderect(parede.rect):
                return True
        return False

    def atualizar(self, player, paredes):
        # Guarda a posição anterior
        pos_anterior_x = self.rect.centerx
        pos_anterior_y = self.rect.centery

        # Aplica knockback se ativo
        if self.knockback_timer > 0:
            self.rect.centerx += self.knockback[0]
            self.rect.centery += self.knockback[1]
            self.knockback_timer -= 1
            
            # Verifica colisão com paredes durante knockback
            if self._colidiu_com_parede(paredes):
                self.rect.centerx = pos_anterior_x
                self.rect.centery = pos_anterior_y
                self.knockback_timer = 0
            return

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
            self.anim_intervalo = 30
            if self.em_patrulha:
                dx = self.direcao * velocidade
                if self.rect.centerx <= self.limite_esquerdo:
                    self.direcao = 1
                elif self.rect.centerx >= self.limite_direito:
                    self.direcao = -1
            else:
                self.em_patrulha = True
                self.limite_esquerdo = self.rect.centerx - 50
                self.limite_direito = self.rect.centerx + 50

        # Atualiza animação
        self.anim_frame += 1
        if self.anim_frame >= self.anim_intervalo:
            self.anim_frame = 0
            self.img_atual = (self.img_atual + 1) % len(self.imagens)

        # Move o inimigo
        self.rect.centerx += dx
        self.rect.centery += dy

        # Verifica colisão com paredes
        if self._colidiu_com_parede(paredes):
            self.rect.centerx = pos_anterior_x
            self.rect.centery = pos_anterior_y
            if self.em_patrulha:
                self.direcao *= -1

    def desenhar(self, tela):
        tela.blit(self.imagens[self.img_atual], self.rect)
