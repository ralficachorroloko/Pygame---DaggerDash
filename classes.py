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
        if distancia <= alcance and distancia > 0:
            self.em_patrulha = False
            velocidade += 3
            dx = player_x - inimigo_x
            dy = player_y - inimigo_y
            distancia = hypot(dx, dy)
            if distancia > 0:
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
    def __init__(self, nome, portas, paredes=None, inimigos=None, player_spawn=(400, 300)):
        self.nome = nome
        self.portas = portas
        self.paredes = []
        self.inimigos = []
        self.player_spawn = player_spawn
        
        # Adiciona as paredes padrão da sala
        self._criar_paredes_padrao()
        
        # Adiciona paredes personalizadas se fornecidas
        if paredes:
            for parede in paredes:
                self.paredes.append(Parede(*parede))  # (x, y, largura, altura)
        
        # Adiciona inimigos personalizados se fornecidos
        if inimigos:
            for inimigo in inimigos:
                # inimigo deve ser uma tupla (x, y, velocidade, tamanho, alcance, imagem)
                self.inimigos.append(Kamikaze(*inimigo))
    
    def _criar_paredes_padrao(self):
        # Adiciona paredes ao redor da sala
        self.paredes.append(Parede(0, 0, WIDTH, 20))  # Parede superior
        self.paredes.append(Parede(0, HEIGHT-20, WIDTH, 20))  # Parede inferior
        self.paredes.append(Parede(0, 0, 20, HEIGHT))  # Parede esquerda
        self.paredes.append(Parede(WIDTH-20, 0, 20, HEIGHT))  # Parede direita
        
        # Adiciona paredes ao redor das portas
        if not self.portas.get("cima"):
            self.paredes.append(Parede(280, 0, 80, 20))
        if not self.portas.get("baixo"):
            self.paredes.append(Parede(280, HEIGHT-20, 80, 20))
        if not self.portas.get("esquerda"):
            self.paredes.append(Parede(0, 280, 20, 80))
        if not self.portas.get("direita"):
            self.paredes.append(Parede(WIDTH-20, 280, 20, 80))
    
    def adicionar_inimigo(self, inimigo):
        self.inimigos.append(inimigo)
    
    def desenhar(self, tela):
        # Draw room background
        tela.fill((30, 30, 30))  # Dark gray background
        
        # Draw walls
        for parede in self.paredes:
            parede.desenhar(tela)
        
        # Draw doors
        if self.portas.get("cima"):
            pygame.draw.rect(tela, (200, 200, 200), (280, 0, 80, 20))
        if self.portas.get("baixo"):
            pygame.draw.rect(tela, (200, 200, 200), (280, HEIGHT-20, 80, 20))
        if self.portas.get("esquerda"):
            pygame.draw.rect(tela, (200, 200, 200), (0, 280, 20, 80))
        if self.portas.get("direita"):
            pygame.draw.rect(tela, (200, 200, 200), (WIDTH-20, 280, 20, 80))
        
        # Draw enemies
        for inimigo in self.inimigos:
            inimigo.desenhar(tela)
    
    def atualizar(self, player):
        # Update all enemies in the room
        for inimigo in self.inimigos[:]:
            inimigo.atualizar(player)
            if inimigo.rect.colliderect(player.rect):
                self.inimigos.remove(inimigo)
    
    def verificar_colisao(self, player, pos_anterior):
        # Verifica colisão com todas as paredes da sala
        for parede in self.paredes:
            if player.rect.colliderect(parede.rect):
                player.rect.topleft = pos_anterior
                return True
        return False

class Dungeon:
    def __init__(self, matriz=None):
        self.matriz = matriz if matriz else []
        self.pos_x = 0
        self.pos_y = 0
        self.player = None
    
    def adicionar_sala(self, sala, x, y):
        # Garante que a matriz tem espaço suficiente
        while len(self.matriz) <= y:
            self.matriz.append([])
        while len(self.matriz[y]) <= x:
            self.matriz[y].append(None)
        
        self.matriz[y][x] = sala
        
        # Se for a primeira sala, define como posição inicial
        if self.player is None:
            self.pos_x = x
            self.pos_y = y
            self.player = Player(sala.player_spawn[0], sala.player_spawn[1], "idle.png", 10, (50, 50))
    
    def sala_atual(self):
        if 0 <= self.pos_y < len(self.matriz) and 0 <= self.pos_x < len(self.matriz[self.pos_y]):
            return self.matriz[self.pos_y][self.pos_x]
        return None
    
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

        if 0 <= novo_y < len(self.matriz) and 0 <= novo_x < len(self.matriz[novo_y]):
            if self.matriz[novo_y][novo_x] is not None:
                self.pos_x = novo_x
                self.pos_y = novo_y
                # Reset player position when changing rooms
                if self.player:
                    self.player.rect.topleft = self.sala_atual().player_spawn
                return True
        return False
    
    def atualizar(self):
        if self.player:
            self.sala_atual().atualizar(self.player)
    
    def desenhar(self, tela):
        self.sala_atual().desenhar(tela)
        if self.player:
            self.player.desenhar(tela)
    
    def mover_jogador(self, dx, dy):
        if self.player:
            pos_anterior = self.player.rect.topleft
            self.player.mover(dx, dy)
            
            # Check wall collisions
            if self.sala_atual().verificar_colisao(self.player, pos_anterior):
                return
            
            # Check door transitions
            if self.player.rect.top <= 0 and self.sala_atual().portas.get("cima"):
                self.mudar_sala("cima")
            elif self.player.rect.bottom >= HEIGHT and self.sala_atual().portas.get("baixo"):
                self.mudar_sala("baixo")
            elif self.player.rect.left <= 0 and self.sala_atual().portas.get("esquerda"):
                self.mudar_sala("esquerda")
            elif self.player.rect.right >= WIDTH and self.sala_atual().portas.get("direita"):
                self.mudar_sala("direita")


        