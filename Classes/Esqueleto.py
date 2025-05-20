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
        
        # Guarda a posição inicial
        self.pos_inicial_x = x
        self.pos_inicial_y = y
        
        self.rect = pygame.Rect(x, y, self.tamanho[0], self.tamanho[1])
        
        self.vida = 100
        self.velocidade_flecha = 7
        self.alcance_flecha = 400
        self.alcance_visao = 300  
        self.tempo_cd = 60  
        self.tempo_ultimo_tiro = 0
        self.flechas = []  
        self.player_norange = False
        
        # Atributos para movimento
        self.velocidade = 2  # Velocidade ao fugir do player
        self.velocidade_patrulha = 1.5  # Velocidade durante a patrulha
        
        # Atributos para comportamento
        self.distancia_fuga = 200  # Distância mínima que tenta manter do player
        self.estado_movimento = "patrulhando"  # Estados: "patrulhando", "fugindo"
        self.estado_ataque = "parado"  # Estados: "parado", "atacando"
        
        # Atributos para patrulha
        self.direcao_patrulha = 1  # 1 para direita, -1 para esquerda
        self.distancia_patrulha = 100  # Distância que percorre em cada direção
        self.pos_inicial_patrulha_x = x  # Posição inicial da patrulha

        # Sistema de knockback e contador de flechas
        self.knockback = [0, 0]  # [dx, dy] do knockback
        self.knockback_forca = 5  # Força do knockback
        self.knockback_duracao = 10  # Frames que o knockback dura
        self.knockback_timer = 0
        self.flechas_acertadas = 0  # Contador de flechas que acertaram

    def receber_dano(self, dano, direcao=None):
        self.flechas_acertadas += 1
        
        # Aplica knockback se uma direção foi fornecida
        if direcao:
            self.knockback = [direcao[0] * self.knockback_forca, direcao[1] * self.knockback_forca]
            self.knockback_timer = self.knockback_duracao
        
        # Retorna True se morreu (2 flechas acertadas)
        return self.flechas_acertadas >= 2

    def atualizar_patrulha(self, paredes):
        # Guarda a posição anterior
        pos_anterior_x = self.rect.centerx
        pos_anterior_y = self.rect.centery
        
        # Aplica knockback se ativo
        if self.knockback_timer > 0:
            self.rect.centerx += self.knockback[0]
            self.rect.centery += self.knockback[1]
            self.knockback_timer -= 1
            
            # Verifica colisão com paredes durante knockback
            if self.verificar_colisao_paredes(paredes):
                self.rect.centerx = pos_anterior_x
                self.rect.centery = pos_anterior_y
                self.knockback_timer = 0
            return

        # Move na direção atual da patrulha
        self.rect.centerx += self.direcao_patrulha * self.velocidade_patrulha
        
        # Verifica colisão
        if self.verificar_colisao_paredes(paredes):
            self.rect.centerx = pos_anterior_x
            self.direcao_patrulha *= -1
            self.pos_inicial_patrulha_x = self.rect.centerx
        # Verifica se precisa mudar de direção
        elif abs(self.rect.centerx - self.pos_inicial_patrulha_x) >= self.distancia_patrulha:
            self.direcao_patrulha *= -1
            self.pos_inicial_patrulha_x = self.rect.centerx

    def verificar_distancia_player(self, player):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        return hypot(dx, dy)

    def mover_em_direcao(self, alvo_x, alvo_y, velocidade, paredes):
        # Guarda a posição anterior
        pos_anterior_x = self.rect.centerx
        pos_anterior_y = self.rect.centery
        
        # Aplica knockback se ativo
        if self.knockback_timer > 0:
            self.rect.centerx += self.knockback[0]
            self.rect.centery += self.knockback[1]
            self.knockback_timer -= 1
            
            # Verifica colisão com paredes durante knockback
            if self.verificar_colisao_paredes(paredes):
                self.rect.centerx = pos_anterior_x
                self.rect.centery = pos_anterior_y
                self.knockback_timer = 0
            return

        # Calcula o movimento
        dx = alvo_x - self.rect.centerx
        dy = alvo_y - self.rect.centery
        distancia = hypot(dx, dy)
        
        if distancia > 0:
            # Tenta mover no eixo X
            self.rect.centerx += (dx / distancia) * velocidade
            if self.verificar_colisao_paredes(paredes):
                self.rect.centerx = pos_anterior_x
            
            # Tenta mover no eixo Y
            self.rect.centery += (dy / distancia) * velocidade
            if self.verificar_colisao_paredes(paredes):
                self.rect.centery = pos_anterior_y

    def detectar_player(self, player):
        distancia_player = self.verificar_distancia_player(player)
        
        # Atualiza estado de movimento baseado na distância do player
        if distancia_player < self.distancia_fuga:
            self.estado_movimento = "fugindo"
        else:
            self.estado_movimento = "patrulhando"
        
        # Atualiza estado de ataque
        if distancia_player <= self.alcance_visao:
            self.estado_ataque = "atacando"
            self.imagem_atual = self.imagem_atirando
        else:
            self.estado_ataque = "parado"
            self.imagem_atual = self.imagem_standby
        
        return distancia_player

    def verificar_colisao_paredes(self, paredes):
        # Guarda a posição anterior
        pos_anterior_x = self.rect.centerx
        pos_anterior_y = self.rect.centery
        
        # Verifica colisão com cada parede
        for parede in paredes:
            parede_rect = pygame.Rect(parede)
            if self.rect.colliderect(parede_rect):
                # Se colidiu, volta para a posição anterior
                self.rect.centerx = pos_anterior_x
                self.rect.centery = pos_anterior_y
                # Se estiver patrulhando, muda de direção
                if self.estado_movimento == "patrulhando":
                    self.direcao_patrulha *= -1
                return True
        return False

    def atirar(self, player):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        
        distancia = hypot(dx, dy)
        if distancia > 0:
            dx = dx / distancia
            dy = dy / distancia
            
            self.flechas.append(Flecha(
                self.rect.centerx,
                self.rect.centery,
                dx,
                dy,
                self.velocidade_flecha,
                self.alcance_flecha
            ))

    def atualizar(self, player, paredes):
        # Atualiza o estado baseado na distância do player
        distancia_player = self.detectar_player(player)
        
        # Atualiza as flechas
        for flecha in self.flechas[:]:
            if flecha.atualizar():
                self.flechas.remove(flecha)
        
        # Atualiza o movimento
        if self.estado_movimento == "patrulhando":
            self.atualizar_patrulha(paredes)
        elif self.estado_movimento == "fugindo":
            # Move na direção oposta ao player
            alvo_x = self.rect.centerx + (self.rect.centerx - player.rect.centerx)
            alvo_y = self.rect.centery + (self.rect.centery - player.rect.centery)
            self.mover_em_direcao(alvo_x, alvo_y, self.velocidade, paredes)
        
        # Atualiza o ataque
        if self.estado_ataque == "atacando":
            self.tempo_ultimo_tiro += 1
            if self.tempo_ultimo_tiro >= self.tempo_cd:
                self.atirar(player)
                self.tempo_ultimo_tiro = 0

    def desenhar(self, tela):
        # Desenha o esqueleto
        tela.blit(self.imagem_atual, self.rect)
        
        # Desenha as flechas
        for flecha in self.flechas:
            flecha.pinta(tela)
