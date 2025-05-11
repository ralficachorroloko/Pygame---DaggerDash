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
        self.areas_portas = {}  # Áreas específicas para as portas
        
        # Adiciona as paredes padrão da sala
        self._criar_paredes_padrao()
        
        # Adiciona paredes personalizadas se fornecidas
        if paredes:
            for parede in paredes:
                self.paredes.append(Parede(*parede))
        
        # Adiciona inimigos personalizados se fornecidos
        if inimigos:
            for inimigo in inimigos:
                self.inimigos.append(Kamikaze(*inimigo))
    
    def _criar_paredes_padrao(self):
        # Adiciona paredes ao redor da sala
        self.paredes.append(Parede(0, 0, WIDTH, 20))  # Parede superior
        self.paredes.append(Parede(0, HEIGHT-20, WIDTH, 20))  # Parede inferior
        self.paredes.append(Parede(0, 0, 20, HEIGHT))  # Parede esquerda
        self.paredes.append(Parede(WIDTH-20, 0, 20, HEIGHT))  # Parede direita
        
        # Define áreas das portas
        if self.portas.get("cima"):
            self.areas_portas["cima"] = pygame.Rect(280, 0, 80, 20)
        else:
            self.paredes.append(Parede(280, 0, 80, 20))
            
        if self.portas.get("baixo"):
            self.areas_portas["baixo"] = pygame.Rect(280, HEIGHT-20, 80, 20)
        else:
            self.paredes.append(Parede(280, HEIGHT-20, 80, 20))
            
        if self.portas.get("esquerda"):
            self.areas_portas["esquerda"] = pygame.Rect(0, 280, 20, 80)
        else:
            self.paredes.append(Parede(0, 280, 20, 80))
            
        if self.portas.get("direita"):
            self.areas_portas["direita"] = pygame.Rect(WIDTH-20, 280, 20, 80)
        else:
            self.paredes.append(Parede(WIDTH-20, 280, 20, 80))
    
    def verificar_porta(self, player_rect):
        for direcao, area in self.areas_portas.items():
            if player_rect.colliderect(area):
                return direcao
        return None
    
    def desenhar(self, tela):
        # Draw room background
        tela.fill((30, 30, 30))  # Dark gray background
        
        # Draw walls
        for parede in self.paredes:
            parede.desenhar(tela)
        
        # Draw doors
        for area in self.areas_portas.values():
            pygame.draw.rect(tela, (200, 200, 200), area)
        
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
            
        # Desenha o nome da sala atual
        fonte = pygame.font.Font(None, 36)
        texto = fonte.render(f"Sala: {self.sala_atual().nome}", True, WHITE)
        tela.blit(texto, (10, 10))
    
    def mover_jogador(self, dx, dy):
        if self.player:
            pos_anterior = self.player.rect.topleft
            self.player.mover(dx, dy)
            
            # Check door transitions first
            sala_atual = self.sala_atual()
            if sala_atual:
                direcao_porta = sala_atual.verificar_porta(self.player.rect)
                if direcao_porta:
                    if self.mudar_sala(direcao_porta):
                        # Ajusta a posição do jogador após a transição
                        if direcao_porta == "cima":
                            self.player.rect.bottom = HEIGHT - 20
                        elif direcao_porta == "baixo":
                            self.player.rect.top = 20
                        elif direcao_porta == "esquerda":
                            self.player.rect.right = WIDTH - 20
                        elif direcao_porta == "direita":
                            self.player.rect.left = 20
                        return
            
            # Check wall collisions only if no door transition happened
            if self.sala_atual().verificar_colisao(self.player, pos_anterior):
                return


        