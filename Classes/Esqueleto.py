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
        self.velocidade = 2  # Mais lento que o player
        self.velocidade_retorno = 1  # Velocidade ao voltar para o spawn
        self.voltando_spawn = False
        
        # Atributos para órbita
        self.raio_orbita = 30  # Raio da órbita ao redor do spawn
        self.angulo_orbita = 0  # Ângulo atual na órbita
        self.velocidade_orbita = 0.02  # Velocidade de rotação na órbita
        
        # Atributos para movimento
        self.direcao_x = 1  # Começa movendo para direita
        self.direcao_y = 0
        self.tempo_mudanca_direcao = 0
        self.intervalo_mudanca = 120  # Muda direção a cada 2 segundos (60 FPS)
        self.distancia_fuga = 70  # Distância mínima que tenta manter do player

    def atualizar_orbita(self):
        # Atualiza o ângulo da órbita
        self.angulo_orbita += self.velocidade_orbita
        
        # Calcula a nova posição na órbita
        self.rect.centerx = self.pos_inicial_x + cos(self.angulo_orbita) * self.raio_orbita
        self.rect.centery = self.pos_inicial_y + sin(self.angulo_orbita) * self.raio_orbita

    def verificar_distancia_spawn(self):
        dx = self.pos_inicial_x - self.rect.centerx
        dy = self.pos_inicial_y - self.rect.centery
        return hypot(dx, dy)

    def detectar_player(self, player):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distancia = hypot(dx, dy)
        
        self.player_detectado = distancia <= self.alcance_visao
        
        # Se o player estiver muito perto, foge
        if distancia < self.distancia_fuga:
            self.direcao_x = -dx / distancia
            self.direcao_y = -dy / distancia
            self.voltando_spawn = False
        # Se o player estiver muito longe, volta para o spawn
        elif distancia > self.alcance_visao * 1.5:  # 50% além do alcance de visão
            self.voltando_spawn = True
            dx = self.pos_inicial_x - self.rect.centerx
            dy = self.pos_inicial_y - self.rect.centery
            distancia = hypot(dx, dy)
            if distancia > 0:
                self.direcao_x = dx / distancia
                self.direcao_y = dy / distancia
        elif self.player_detectado:
            self.imagem_atual = self.imagem_atirando
            self.voltando_spawn = False
        else:
            self.imagem_atual = self.imagem_standby
            self.voltando_spawn = False
        
        return distancia

    def verificar_colisao_paredes(self, paredes):
        # Guarda a posição anterior
        pos_anterior_x = self.rect.centerx
        pos_anterior_y = self.rect.centery
        
        # Se estiver voltando ao spawn ou fugindo, verifica colisão
        if self.voltando_spawn or self.player_detectado:
            # Tenta mover
            self.rect.centerx += self.direcao_x * (self.velocidade_retorno if self.voltando_spawn else self.velocidade)
            self.rect.centery += self.direcao_y * (self.velocidade_retorno if self.voltando_spawn else self.velocidade)
            
            # Verifica colisão com cada parede
            for parede in paredes:
                if self.rect.colliderect(pygame.Rect(parede)):
                    # Se colidiu, volta para a posição anterior
                    self.rect.centerx = pos_anterior_x
                    self.rect.centery = pos_anterior_y
                    # Se estiver voltando ao spawn, tenta outro caminho
                    if self.voltando_spawn:
                        self.voltando_spawn = False
                        self.atualizar_orbita()
                    break

    def atirar(self, player):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        
        distancia = hypot(dx, dy)
        if distancia > 0:
            dx = dx / distancia
            dy = dy / distancia
            flecha = Flecha(self.rect.centerx,self.rect.centery,dx,dy,self.velocidade_flecha,self.alcance_flecha)
            self.flechas.append(flecha)

    def atualizar(self, player, paredes):
        self.detectar_player(player)
        
        # Se não estiver detectando o player e não estiver voltando ao spawn
        if not self.player_detectado and not self.voltando_spawn:
            # Verifica se está muito longe do spawn
            if self.verificar_distancia_spawn() > self.raio_orbita * 2:
                # Se estiver muito longe, volta ao spawn
                self.voltando_spawn = True
                dx = self.pos_inicial_x - self.rect.centerx
                dy = self.pos_inicial_y - self.rect.centery
                distancia = hypot(dx, dy)
                if distancia > 0:
                    self.direcao_x = dx / distancia
                    self.direcao_y = dy / distancia
            else:
                # Se estiver próximo do spawn, orbita
                self.atualizar_orbita()
        else:
            # Atualiza movimento com colisão
            self.verificar_colisao_paredes(paredes)
        
        # Atualiza tiro
        if self.player_detectado:
            self.tempo_ultimo_tiro += 1
            if self.tempo_ultimo_tiro >= self.tempo_cd:
                self.atirar(player)
                self.tempo_ultimo_tiro = 0
                
        # Atualiza flechas
        flechas_para_remover = []
        for flecha in self.flechas:
            if flecha.atualizar():
                flechas_para_remover.append(flecha)
        for flecha in flechas_para_remover:
            self.flechas.remove(flecha)

    def receber_dano(self, dano):
        self.vida -= dano
        return self.vida <= 0

    def desenhar(self, tela):
        tela.blit(self.imagem_atual, self.rect)
        for flecha in self.flechas:
            flecha.pinta(tela)
