import pygame
from os import path
from Classes.Player import Player
from Classes.Sala import Sala
from config import HEIGHT, WIDTH, WHITE

class Dungeon:
    def __init__(self, matriz=None, dungeon_num=1):
        self.matriz = matriz if matriz else []
        self.pos_x = 0
        self.pos_y = 0
        self.player = None
        self.ultima_direcao = None  # Armazena a direção da última transição
        self.dungeon_num = dungeon_num  # Número da dungeon atual (1-7)
        self.completa = False  # Indica se a dungeon foi completada
    
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
            self.player = Player(sala.player_spawn[0], sala.player_spawn[1], "idle.png", 5, (32, 32))
    
    def sala_atual(self):
        if 0 <= self.pos_y < len(self.matriz) and 0 <= self.pos_x < len(self.matriz[self.pos_y]):
            return self.matriz[self.pos_y][self.pos_x]
        return None
    
    def mudar_sala(self, direcao):
        # Determina a direção de transição da sala na matriz
        dx = 0
        if direcao == "esquerda":
            dx = -1
        elif direcao == "direita":
            dx = 1

        # calcula as coordenadas da sala de destino na matriz
        novo_x = self.pos_x + dx

        # Verifica se a sala de destino existe e não é None
        if 0 <= novo_x < len(self.matriz[self.pos_y]):
            if self.matriz[self.pos_y][novo_x] is not None:
                # Atualiza as coordenadas da sala atual
                self.pos_x = novo_x
                self.ultima_direcao = direcao

                # Teleporta o jogador para a porta correspondente na nova sala
                if self.player:
                    sala = self.sala_atual()
                    if sala:
                        # Define a posição do jogador baseada na direção oposta da transição
                        if direcao == "esquerda":
                            self.player.teleportar_para(WIDTH-100, 320)  # Mais longe da porta direita
                        elif direcao == "direita":
                            self.player.teleportar_para(100, 320)  # Mais longe da porta esquerda
                return True  # Retorna True se a transição foi bem sucedida
        return False  # Retorna False se a transição falhou
    
    def atualizar(self):
        if self.player:
            self.sala_atual().atualizar(self.player)
    
    def desenhar(self, tela):
        sala = self.sala_atual()
        if sala:
            sala.desenhar(tela)
            if self.player:
                self.player.desenhar(tela)
                
            # Desenha o nome da sala atual e número da dungeon
            fonte = pygame.font.Font(None, 36)
            texto = fonte.render(f"Dungeon {self.dungeon_num} - Sala: {sala.nome}", True, WHITE)
            tela.blit(texto, (10, 10))
    
    def passagem_porta(self, dx, dy):
        if self.player:
            pos_anterior = self.player.rect.topleft
            self.player.mover(dx, dy)
            
            # Transição de sala
            sala_atual = self.sala_atual()
            if sala_atual:
                direcao_porta = sala_atual.verificar_porta(self.player.rect)
                if direcao_porta:
                    if self.mudar_sala(direcao_porta):
                        return
            
            # Verifica colisão com paredes
            if self.sala_atual().verificar_colisao(self.player, pos_anterior):
                return
            