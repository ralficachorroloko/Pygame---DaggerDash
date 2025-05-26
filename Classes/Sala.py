import pygame
from os import path
from Classes.Parede import Parede
from Classes.Kamikaze import Kamikaze
from Classes.Esqueleto import Esqueleto
from config import HEIGHT, WIDTH

class Sala:
    """Classe que representa uma sala na dungeon.
    
    Gerencia os elementos de uma sala, incluindo:
    - Paredes e colisões
    - Inimigos
    - Itens e objetos
    - Portas e transições
    """
    
    def __init__(self, nome, portas, imagem_sala=None, paredes=None, inimigos=None, player_spawn=(400, 300)):
        """Inicializa uma nova sala.
        
        Args:
            nome (str): Nome identificador da sala
            portas (dict): Dicionário de portas da sala
            imagem_sala (str, optional): Caminho para a imagem da sala. Defaults to None.
            paredes (list, optional): Lista de paredes da sala. Defaults to None.
            inimigos (list, optional): Lista de inimigos da sala. Defaults to None.
            player_spawn (tuple, optional): Posição inicial do jogador (x, y). Defaults to (400, 300).
        """
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
                # Verifica se a imagem foi carregada corretamente
                if self.imagem.get_width() == 0 or self.imagem.get_height() == 0:
                    print(f"Erro: Imagem da sala {imagem_sala} tem dimensões inválidas")
                    self.imagem = None
                    self.rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
            except Exception as e:
                print(f"Erro ao carregar imagem da sala {imagem_sala}: {str(e)}")
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
    
    def verificar_porta(self, rect):
        """Verifica se o jogador entrou em uma porta.
        
        Args:
            rect (pygame.Rect): Retângulo do jogador
            
        Returns:
            str: Direção da porta ("esquerda", "direita", "cima", "baixo", "centro") ou None
        """
        if not rect:  # Verifica se o rect é válido
            return None
            
        for direcao, area in self.areas_portas.items():
            # Cria uma área de detecção maior ao redor da porta
            area_deteccao = pygame.Rect(
                area.x - 10,  # Estende 10 pixels para a esquerda
                area.y,      # Mantém a mesma altura
                area.width + 20,  # Estende 10 pixels para cada lado
                area.height
            )
            
            if rect.colliderect(area_deteccao):
                return direcao
        return None
    
    def desenhar(self, tela):
        """Desenha todos os elementos da sala.
        
        Args:
            tela (pygame.Surface): Superfície onde a sala será desenhada
        """
        if not tela:  # Verifica se a tela é válida
            return
            
        # Desenha um fundo padrão caso a imagem não exista
        if not self.imagem:
            tela.fill((50, 50, 50))  # Cinza escuro como fundo padrão
        else:
            # Desenha a imagem da sala
            tela.blit(self.imagem, (0, 0))
        
        # Desenha as paredes
        for parede in self.paredes:
            parede.desenhar(tela)
        
        # Desenha os inimigos
        for inimigo in self.inimigos:
            inimigo.desenhar(tela)
            
        # Desenha os objetos da sala que têm o método desenhar
        for objeto in self.objetos:
            if hasattr(objeto, 'desenhar'):
                objeto.desenhar(tela)
            elif hasattr(objeto, 'pinta'):  # Alguns objetos usam 'pinta' em vez de 'desenhar'
                objeto.pinta(tela)
    
    def atualizar(self, player):
        """Atualiza o estado de todos os elementos da sala.
        
        Args:
            player (Player): Referência ao jogador para interações
        """
        if not player:  # Verifica se o player é válido
            return

        # Atualiza todos os inimigos
        for inimigo in self.inimigos[:]:  # Usa uma cópia da lista para evitar problemas durante a iteração
            inimigo.atualizar(player, self.paredes)
            
            # Verifica colisão com o jogador
            if inimigo.rect.colliderect(player.rect):
                player.levar_dano()  # Jogador leva dano
                if isinstance(inimigo, Kamikaze):  # Se for um kamikaze, ele é removido após causar dano
                    morreu, item = inimigo.receber_dano(100)
                    if morreu:
                        self.inimigos.remove(inimigo)
                        if item:
                            self.objetos.append(item)
                            item.posicionar(inimigo.rect.centerx, inimigo.rect.centery)
            elif isinstance(inimigo, Esqueleto):
                for flecha in inimigo.flechas[:]:
                    if flecha.rect.colliderect(player.rect):
                        player.levar_dano()
                        inimigo.flechas.remove(flecha)
        
        # Verifica colisão com itens no chão
        for item in self.objetos[:]:  # Usa uma cópia da lista para evitar problemas durante a iteração
            if hasattr(item, 'rect') and player.rect.colliderect(item.rect):
                # Adiciona o item ao inventário
                if player.adicionar_item(item):
                    # Se o item foi adicionado com sucesso, remove-o do chão
                    self.objetos.remove(item)
        
        # Atualiza todos os objetos da sala que têm o método atualizar
        for objeto in self.objetos:
            if hasattr(objeto, 'atualizar'):
                objeto.atualizar()
    
    def verificar_colisao(self, player, pos_anterior):
        """Verifica colisões do jogador com as paredes da sala.
        
        Args:
            player (Player): Jogador para verificar colisão
            pos_anterior (tuple): Posição anterior do jogador (x, y)
            
        Returns:
            bool: True se houve colisão, False caso contrário
        """
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
