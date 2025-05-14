import pygame
from os import path
from Classes.Parede import Parede
from Classes.Kamikaze import Kamikaze
from config import HEIGHT, WIDTH
from Classes.TileManager import TileManager

class Sala:
    def __init__(self, nome, portas, paredes=None, inimigos=None, player_spawn=(400, 300)):
        self.nome = nome
        self.portas = portas
        self.paredes = []
        self.inimigos = []
        self.player_spawn = player_spawn
        self.areas_portas = {}  # Áreas específicas para as portas
        
        # Novos atributos para o sistema de tiles
        self.tile_manager = TileManager()
        self.tile_map = []  # Matriz que armazena os tiles da sala
        
        # Inicializa o mapa de tiles
        self._inicializar_tile_map()
        
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
    
    def _inicializar_tile_map(self):
        # Calcula quantos tiles cabem na largura e altura da sala
        num_tiles_x = WIDTH // self.tile_manager.tile_size
        num_tiles_y = HEIGHT // self.tile_manager.tile_size
        
        # Cria uma matriz preenchida com tiles de chão
        self.tile_map = [[None for _ in range(num_tiles_x)] for _ in range(num_tiles_y)]
        
        # Preenche o centro da sala com tiles de chão
        for y in range(1, num_tiles_y-1):
            for x in range(1, num_tiles_x-1):
                self.tile_map[y][x] = self.tile_manager.get_tile_chao('centro')
        
        # Preenche as bordas com tiles de borda
        for x in range(num_tiles_x):
            self.tile_map[0][x] = self.tile_manager.get_tile_chao('borda')
            self.tile_map[-1][x] = self.tile_manager.get_tile_chao('borda')
        for y in range(num_tiles_y):
            self.tile_map[y][0] = self.tile_manager.get_tile_chao('borda')
            self.tile_map[y][-1] = self.tile_manager.get_tile_chao('borda')
    
    def _criar_paredes_padrao(self):
        # Adiciona paredes ao redor da sala
        self.paredes.append(Parede(0, 0, WIDTH, 16))  # Parede superior
        self.paredes.append(Parede(0, HEIGHT-16, WIDTH, 16))  # Parede inferior
        self.paredes.append(Parede(0, 0, 16, HEIGHT))  # Parede esquerda
        self.paredes.append(Parede(WIDTH-16, 0, 16, HEIGHT))  # Parede direita
        
        # Define áreas das portas e atualiza o mapa de tiles
        if self.portas.get("cima"):
            self.areas_portas["cima"] = pygame.Rect(280, 0, 80, 16)
            self._atualizar_tiles_porta("cima")
        else:
            self.paredes.append(Parede(280, 0, 80, 16))
            
        if self.portas.get("baixo"):
            self.areas_portas["baixo"] = pygame.Rect(280, HEIGHT-16, 80, 16)
            self._atualizar_tiles_porta("baixo")
        else:
            self.paredes.append(Parede(280, HEIGHT-16, 80, 16))
            
        if self.portas.get("esquerda"):
            self.areas_portas["esquerda"] = pygame.Rect(0, 280, 16, 80)
            self._atualizar_tiles_porta("esquerda")
        else:
            self.paredes.append(Parede(0, 280, 16, 80))
            
        if self.portas.get("direita"):
            self.areas_portas["direita"] = pygame.Rect(WIDTH-16, 280, 16, 80)
            self._atualizar_tiles_porta("direita")
        else:
            self.paredes.append(Parede(WIDTH-16, 280, 16, 80))
    
    def _atualizar_tiles_porta(self, direcao):
        tile_size = self.tile_manager.tile_size
        
        if direcao == "cima":
            start_x = 280 // tile_size
            end_x = (280 + 80) // tile_size
            for x in range(start_x, end_x):
                self.tile_map[0][x] = self.tile_manager.get_tile_parede("cima")
                
        elif direcao == "baixo":
            start_x = 280 // tile_size
            end_x = (280 + 80) // tile_size
            for x in range(start_x, end_x):
                self.tile_map[-1][x] = self.tile_manager.get_tile_parede("baixo")
                
        elif direcao == "esquerda":
            start_y = 280 // tile_size
            end_y = (280 + 80) // tile_size
            for y in range(start_y, end_y):
                self.tile_map[y][0] = self.tile_manager.get_tile_parede("esquerda")
                
        elif direcao == "direita":
            start_y = 280 // tile_size
            end_y = (280 + 80) // tile_size
            for y in range(start_y, end_y):
                self.tile_map[y][-1] = self.tile_manager.get_tile_parede("direita")
    
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
            
        # Desenha o background com tiles
        tile_size = self.tile_manager.tile_size
        for y, row in enumerate(self.tile_map):
            for x, tile in enumerate(row):
                if tile:  # Só desenha se houver um tile
                    tela.blit(tile, (x * tile_size, y * tile_size))
        
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
    
    def verificar_colisao(self, player, pos_anterior):
        if not player or not pos_anterior:  # Verifica se os parâmetros são válidos
            return False
            
        # Verifica colisão com todas as paredes da sala
        for parede in self.paredes:
            if player.rect.colliderect(parede.rect):
                player.rect.topleft = pos_anterior
                return True
        return False
