
import pygame
from os import path
from config import *
from math import *


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
