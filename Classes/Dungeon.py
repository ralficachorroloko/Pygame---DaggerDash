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
    
    def passagem_porta(self, dx, dy):
        sala_atual = self.sala_atual()
        if not sala_atual:
            return

        # Guarda a posição anterior do jogador
        pos_anterior = self.player.rect.topleft

        # Move o jogador
        self.player.mover(dx, dy)

        # Verifica colisão com paredes
        if sala_atual.verificar_colisao(self.player, pos_anterior):
            return

        # Verifica se o jogador entrou em uma porta
        direcao = sala_atual.verificar_porta(self.player.rect)
        if direcao:
            # Calcula a nova posição baseada na direção
            if direcao == "esquerda":
                self.pos_x -= 1
                self.ultima_direcao = "direita"
            elif direcao == "direita":
                self.pos_x += 1
                self.ultima_direcao = "esquerda"
            elif direcao == "cima":
                self.pos_y -= 1
                self.ultima_direcao = "baixo"
            elif direcao == "baixo":
                self.pos_y += 1
                self.ultima_direcao = "cima"
            elif direcao == "centro":
                # Se for a porta central da sala de transição ou spawn, avança para a próxima dungeon
                if sala_atual.nome == "Transição de andar" or sala_atual.nome == "Spawn":
                    self.dungeon_num += 1
                    if self.dungeon_num <= 7:  # Verifica se ainda há dungeons disponíveis
                        # Limpa a matriz atual
                        self.matriz = []
                        self.pos_x = 0
                        self.pos_y = 0
                        # Carrega a nova matriz da próxima dungeon
                        from Classes.DungeonData import DUNGEON_MATRIZES
                        nova_matriz = DUNGEON_MATRIZES[self.dungeon_num]
                        # Cria as salas da nova dungeon
                        for i, tipo_sala in enumerate(nova_matriz[0]):
                            from Classes.DungeonData import criar_sala
                            sala = criar_sala(tipo_sala)
                            if sala:
                                self.adicionar_sala(sala, i, 0)
                        return
                self.completa = True

            # Teleporta o jogador para a posição correta na nova sala
            nova_sala = self.sala_atual()
            if nova_sala:
                if self.ultima_direcao == "esquerda":
                    self.player.teleportar_para(50, nova_sala.player_spawn[1])
                elif self.ultima_direcao == "direita":
                    self.player.teleportar_para(WIDTH - 100, nova_sala.player_spawn[1])
                elif self.ultima_direcao == "cima":
                    self.player.teleportar_para(nova_sala.player_spawn[0], 50)
                elif self.ultima_direcao == "baixo":
                    self.player.teleportar_para(nova_sala.player_spawn[0], HEIGHT - 100)
    
    def desenhar(self, tela):
        sala_atual = self.sala_atual()
        if sala_atual:
            sala_atual.desenhar(tela)
            self.player.desenhar(tela)
                
            # Desenha o nome da sala atual e número da dungeon
            fonte = pygame.font.Font(None, 36)
            texto = fonte.render(f"Dungeon {self.dungeon_num} - Sala: {sala_atual.nome}", True, WHITE)
            tela.blit(texto, (10, 10))
    
    def atualizar(self):
        if self.player:
            self.sala_atual().atualizar(self.player)
    