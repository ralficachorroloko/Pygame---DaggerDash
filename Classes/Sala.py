import pygame
from os import path
from Classes.Parede import Parede
from Classes.Kamikaze import Kamikaze
from config import HEIGHT, WIDTH, LARGURA, ALTURA

class Sala:
    def __init__(self, nome, portas, imagem_sala=None, paredes=None, inimigos=None, player_spawn=(400, 300)):
        self.nome = nome
        self.portas = portas
        self.paredes = []
        self.inimigos = []
        self.player_spawn = player_spawn
        self.areas_portas = {}  # Áreas específicas para as portas
        
        # Carrega a imagem da sala se fornecida
        if imagem_sala:
            self.imagem = pygame.image.load(path.join("img", "salas", imagem_sala)).convert()
            self.rect = self.imagem.get_rect()
        else:
            self.imagem = None
            self.rect = pygame.Rect(0, 0, LARGURA, ALTURA)
        
        # Adiciona as paredes padrão da sala
        self._criar_paredes_padrao()
        
        # Adiciona paredes personalizadas se fornecidas
        if paredes:
            for parede in paredes:
                if len(parede) == 4:  # Verifica se a parede tem todos os parâmetros necessários
                    self.paredes.append(Parede(*parede))
        
        # Adiciona inimigos personalizados se fornecidos
        if inimigos:
            for inimigo in inimigos:
                if len(inimigo) == 6:  # Verifica se o inimigo tem todos os parâmetros necessários
                    self.inimigos.append(Kamikaze(*inimigo))
    
    def _criar_paredes_padrao(self):
        # Adiciona paredes ao redor da sala
        self.paredes.append(Parede(0, 0, WIDTH, 16))  # Parede superior
        self.paredes.append(Parede(0, HEIGHT-16, WIDTH, 16))  # Parede inferior
        self.paredes.append(Parede(0, 0, 16, HEIGHT))  # Parede esquerda
        self.paredes.append(Parede(WIDTH-16, 0, 16, HEIGHT))  # Parede direita
        
        # Define áreas das portas
        if self.portas.get("cima"):
            self.areas_portas["cima"] = pygame.Rect(280, 0, 80, 16)
        else:
            self.paredes.append(Parede(280, 0, 80, 16))
            
        if self.portas.get("baixo"):
            self.areas_portas["baixo"] = pygame.Rect(280, HEIGHT-16, 80, 16)
        else:
            self.paredes.append(Parede(280, HEIGHT-16, 80, 16))
            
        if self.portas.get("esquerda"):
            self.areas_portas["esquerda"] = pygame.Rect(0, 280, 16, 80)
        else:
            self.paredes.append(Parede(0, 280, 16, 80))
            
        if self.portas.get("direita"):
            self.areas_portas["direita"] = pygame.Rect(WIDTH-16, 280, 16, 80)
        else:
            self.paredes.append(Parede(WIDTH-16, 280, 16, 80))
    
    def verificar_porta(self, player_rect):
        if not player_rect:  # Verifica se o rect é válido
            return None
            
        for direcao, area in self.areas_portas.items():
            if player_rect.colliderect(area):
                return direcao
        return None
    
    def desenhar(self, tela):
        if not tela:  # Verifica se a tela é válida
            return
            
        # Desenha a imagem da sala se existir
        if self.imagem:
            tela.blit(self.imagem, (0, 0))
        
        # Desenha as paredes
        for parede in self.paredes:
            parede.desenhar(tela)
        
        # Desenha as portas
        for area in self.areas_portas.values():
            pygame.draw.rect(tela, (200, 200, 200), area)
        
        # Desenha os inimigos
        for inimigo in self.inimigos:
            inimigo.desenhar(tela)
    
    def atualizar(self, player):
        if not player:  # Verifica se o player é válido
            return
            
        # Update all enemies in the room
        for inimigo in self.inimigos[:]:  # Usa uma cópia da lista para evitar problemas durante a iteração
            inimigo.atualizar(player)
            if inimigo.rect.colliderect(player.rect):
                self.inimigos.remove(inimigo)
        
        # Atualiza todos os objetos da sala
        for objeto in self.objetos:
            objeto.atualizar()
    
    def verificar_colisao(self, player, pos_anterior):
        if not player or not pos_anterior:  # Verifica se os parâmetros são válidos
            return False
            
        # Verifica colisão com todas as paredes da sala
        for parede in self.paredes:
            if player.rect.colliderect(parede.rect):
                player.rect.topleft = pos_anterior
                return True
        return False

    def adicionar_objeto(self, objeto):
        self.objetos.append(objeto)
        
    def adicionar_porta(self, porta):
        self.portas.append(porta)
        
    def get_rect(self):
        return self.rect
