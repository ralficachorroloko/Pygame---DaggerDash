import pygame
from os import path
from Classes.Player import Player
from Classes.Sala import Sala
from config import HEIGHT, WIDTH, WHITE, VITORIA

class Dungeon:
    """Classe que representa uma dungeon no jogo.
    
    Gerencia a estrutura da dungeon, incluindo:
    - Matriz de salas
    - Posição do jogador
    - Transições entre salas
    - Progressão entre dungeons
    """
    
    def __init__(self, matriz=None, dungeon_num=1):
        """Inicializa uma nova dungeon.
        
        Args:
            matriz (list, optional): Matriz de salas da dungeon. Defaults to None.
            dungeon_num (int, optional): Número da dungeon atual. Defaults to 1.
        """
        self.matriz = matriz if matriz else []
        self.pos_x = 0
        self.pos_y = 0
        self.player = None
        self.ultima_direcao = None  # Armazena a direção da última transição
        self.dungeon_num = dungeon_num  # Número da dungeon atual (1-7)
        self.completa = False  # Indica se a dungeon foi completada
    
    def adicionar_sala(self, sala, x, y):
        """Adiciona uma sala à matriz da dungeon.
        
        Args:
            sala (Sala): Objeto sala a ser adicionado
            x (int): Posição x na matriz
            y (int): Posição y na matriz
        """
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
        """Retorna a sala atual onde o jogador está.
        
        Returns:
            Sala: Objeto da sala atual ou None se posição inválida
        """
        if 0 <= self.pos_y < len(self.matriz) and 0 <= self.pos_x < len(self.matriz[self.pos_y]):
            return self.matriz[self.pos_y][self.pos_x]
        return None
    
    def passagem_porta(self, dx, dy):
        """Gerencia a passagem do jogador entre salas.
        
        Args:
            dx (int): Direção horizontal do movimento
            dy (int): Direção vertical do movimento
            
        Returns:
            int: Estado VITORIA se completou a dungeon, None caso contrário
        """
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
            # Se estiver na sala final e entrar pela porta direita, ativa a tela de vitória
            if sala_atual.nome == "Final" and direcao == "direita":
                return VITORIA
                
            # Calcula a nova posição baseada na direção
            nova_pos_x = self.pos_x
            nova_pos_y = self.pos_y
            
            if direcao == "esquerda":
                nova_pos_x -= 1
                self.ultima_direcao = "direita"
            elif direcao == "direita":
                nova_pos_x += 1
                self.ultima_direcao = "esquerda"
            elif direcao == "cima":
                nova_pos_y -= 1
                self.ultima_direcao = "baixo"
            elif direcao == "baixo":
                nova_pos_y += 1
                self.ultima_direcao = "cima"
            elif direcao == "centro":
                # Se for a porta central da sala de transição, spawn ou sala besta, avança para a próxima dungeon
                if sala_atual.nome in ["Transição de andar", "Spawn", "Sala_besta"]:
                    self.dungeon_num += 1
                    if self.dungeon_num <= 7:  # Verifica se ainda há dungeons disponíveis
                        # Limpa a matriz atual
                        self.matriz = []
                        self.pos_x = 0
                        self.pos_y = 0
                        # Carrega a nova matriz da próxima dungeon
                        from Classes.DungeonData import DUNGEON_MATRIZES, criar_sala
                        nova_matriz = DUNGEON_MATRIZES[self.dungeon_num]
                        # Cria as salas da nova dungeon
                        for i, tipo_sala in enumerate(nova_matriz[0]):
                            sala = criar_sala(tipo_sala)
                            if sala:
                                self.adicionar_sala(sala, i, 0)
                        return
                    self.completa = True
                    return

            # Verifica se a nova posição está dentro dos limites da matriz
            if 0 <= nova_pos_y < len(self.matriz) and 0 <= nova_pos_x < len(self.matriz[nova_pos_y]):
                # Se a próxima sala for None, avança para a próxima dungeon
                if self.matriz[nova_pos_y][nova_pos_x] is None:
                    self.dungeon_num += 1
                    if self.dungeon_num <= 7:  # Verifica se ainda há dungeons disponíveis
                        # Limpa a matriz atual
                        self.matriz = []
                        self.pos_x = 0
                        self.pos_y = 0
                        # Carrega a nova matriz da próxima dungeon
                        from Classes.DungeonData import DUNGEON_MATRIZES, criar_sala
                        nova_matriz = DUNGEON_MATRIZES[self.dungeon_num]
                        # Cria as salas da nova dungeon
                        for i, tipo_sala in enumerate(nova_matriz[0]):
                            sala = criar_sala(tipo_sala)
                            if sala:
                                self.adicionar_sala(sala, i, 0)
                        return
                    self.completa = True
                    return

                # Atualiza as posições
                self.pos_x = nova_pos_x
                self.pos_y = nova_pos_y

                # Teleporta o jogador para a posição correta na nova sala
                nova_sala = self.sala_atual()
                if nova_sala:
                    # Posiciona o jogador na nova sala
                    if self.ultima_direcao == "esquerda":
                        self.player.teleportar_para(50, nova_sala.player_spawn[1])
                    elif self.ultima_direcao == "direita":
                        self.player.teleportar_para(WIDTH - 100, nova_sala.player_spawn[1])
                    elif self.ultima_direcao == "cima":
                        self.player.teleportar_para(nova_sala.player_spawn[0], 50)
                    elif self.ultima_direcao == "baixo":
                        self.player.teleportar_para(nova_sala.player_spawn[0], HEIGHT - 100)
                else:
                    # Volta o jogador para a posição anterior
                    self.player.rect.topleft = pos_anterior
                    # Restaura as posições anteriores
                    self.pos_x = nova_pos_x + (1 if direcao == "esquerda" else -1 if direcao == "direita" else 0)
                    self.pos_y = nova_pos_y + (1 if direcao == "cima" else -1 if direcao == "baixo" else 0)
            else:
                # Volta o jogador para a posição anterior
                self.player.rect.topleft = pos_anterior
    
    def desenhar(self, tela):
        """Desenha a sala atual e o jogador.
        
        Args:
            tela (pygame.Surface): Superfície onde a dungeon será desenhada
        """
        sala_atual = self.sala_atual()
        if sala_atual:
            sala_atual.desenhar(tela)
            self.player.desenhar(tela)
    
    def atualizar(self):
        """Atualiza o estado da sala atual."""
        if self.player:
            self.sala_atual().atualizar(self.player)
    