import pygame
from os import path
from Classes.Parede import Parede
from Classes.Kamikaze import Kamikaze
from Classes.Esqueleto import Esqueleto
from config import HEIGHT, WIDTH

class Sala:
    def __init__(self, nome, portas, imagem_sala=None, paredes=None, inimigos=None, player_spawn=(400, 300)):
        self.nome = nome
        self.portas = portas
        self.paredes = []
        self.inimigos = []
        self.objetos = []  # Inicializa a lista de objetos
        self.player_spawn = player_spawn
        self.areas_portas = {}  # Áreas específicas para as portas
        
        # Carrega a imagem da sala se fornecida
        if imagem_sala:
            try:
                self.imagem = pygame.image.load(path.join("Mapas", imagem_sala)).convert()
                self.rect = self.imagem.get_rect()
            except:
                print(f"Erro ao carregar imagem da sala: {imagem_sala}")
                self.imagem = None
                self.rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        else:
            self.imagem = None
            self.rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        
        # Adiciona as paredes personalizadas se fornecidas
        if paredes:
            for parede in paredes:
                if len(parede) == 4:  # Verifica se a parede tem todos os parâmetros necessários
                    self.paredes.append(Parede(*parede))
        else:
            # Se não houver paredes personalizadas, cria as paredes padrão
            self._criar_paredes_padrao()
        
        # Adiciona inimigos personalizados se fornecidos
        if inimigos:
            self.inimigos = inimigos  # Agora recebe diretamente a lista de inimigos já criados
        
        # Configura as áreas das portas
        self._configurar_portas()
    
    def _configurar_portas(self):
        # Configura as áreas das portas baseado no dicionário de portas
        for nome_porta, dados_porta in self.portas.items():
            self.areas_portas[nome_porta] = pygame.Rect(
                dados_porta["x"],
                dados_porta["y"],
                dados_porta["largura"],
                dados_porta["altura"]
            )
    
    def _criar_paredes_padrao(self):
        # Define as alturas das paredes (em pixels, onde cada bloco é 32x32)
        if self.nome == "Spawn":
            # No Spawn: parede superior 3 blocos (96px), outras 2 blocos (64px)
            self.paredes.append(Parede(0, 0, WIDTH, 64))  # Parede superior
            self.paredes.append(Parede(0, HEIGHT-64, WIDTH, 64))  # Parede inferior 
            self.paredes.append(Parede(0, 0, 64, HEIGHT))  # Parede esquerda 
            self.paredes.append(Parede(WIDTH-64, 0, 64, HEIGHT))  # Parede direita 
        else:
            # Nas outras salas: parede superior 2 blocos (64px), outras 1 blocos (32px)
            self.paredes.append(Parede(0, 0, WIDTH, 64))  # Parede superior 
            self.paredes.append(Parede(0, HEIGHT-32, WIDTH, 32))  # Parede inferior 
            self.paredes.append(Parede(0, 0, 32, HEIGHT))  # Parede esquerda 
            self.paredes.append(Parede(WIDTH-24, 0, 48, HEIGHT))  # Parede direita 
    
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
        
        # Desenha os inimigos
        for inimigo in self.inimigos:
            inimigo.desenhar(tela)
            
        # Desenha os objetos da sala
        for objeto in self.objetos:
            objeto.desenhar(tela)
    
    def atualizar(self, player):
        if not player:  # Verifica se o player é válido
            return
            
        # Atualiza todos os inimigos na sala
        for inimigo in self.inimigos[:]:  # Usa uma cópia da lista para evitar problemas durante a iteração
            inimigo.atualizar(player, self.paredes)
            
            # Verifica colisão com o jogador
            if inimigo.rect.colliderect(player.rect):
                player.levar_dano()  # Jogador leva dano
                if isinstance(inimigo, Kamikaze):  # Se for um kamikaze, ele é removido após causar dano
                    self.inimigos.remove(inimigo)
            
            # Verifica colisão das flechas do esqueleto com o jogador
            if isinstance(inimigo, Esqueleto):
                for flecha in inimigo.flechas[:]:
                    if flecha.rect.colliderect(player.rect):
                        player.levar_dano()
                        inimigo.flechas.remove(flecha)
        
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
