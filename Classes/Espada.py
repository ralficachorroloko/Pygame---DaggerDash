import pygame
from os import path
from config import *
from math import *

class Espada:
    """Classe que representa o ataque com espada do jogador.
    
    Gerencia o comportamento do ataque com espada, incluindo:
    - Animação e rotação
    - Duração do ataque
    - Colisão com inimigos
    """
    
    def __init__(self, player, mouse_pos, imagem):
        """Inicializa um novo ataque com espada.
        
        Args:
            player (Player): Referência ao jogador
            mouse_pos (tuple): Posição do mouse (x, y)
            imagem (str): Nome do arquivo da imagem da espada
        """
        self.player = player
        self.duracao = 10
        
        # Calcula o ângulo entre o jogador e o mouse
        dx = mouse_pos[0] - player.rect.centerx
        dy = mouse_pos[1] - player.rect.centery
        self.angulo = atan2(dy, dx)
        
        # Carrega e prepara a imagem base
        self.imagem_base = pygame.image.load(path.join("img", "itens", "slash.png")).convert_alpha()
        self.imagem_base = pygame.transform.scale(self.imagem_base, (50, 100))
        
        # Define as dimensões base
        self.largura_base = 100
        self.altura_base = 50
        
        # Prepara a imagem e o retângulo inicial
        self.atualizar_imagem()
        
    def atualizar_imagem(self):
        """Atualiza a rotação e posição da espada baseada na direção do ataque."""
        # Determina a direção e ajusta a imagem e o retângulo
        if -pi/4 <= self.angulo < pi/4:  # Direita
            self.imagem = pygame.transform.rotate(self.imagem_base, 180)
            self.rect = pygame.Rect(
                self.player.rect.right,
                self.player.rect.centery - self.largura_base/2,
                self.altura_base,
                self.largura_base
            )
        elif pi/4 <= self.angulo < 3*pi/4:  # Baixo
            self.imagem = pygame.transform.rotate(self.imagem_base, 90)
            self.rect = pygame.Rect(
                self.player.rect.centerx - self.largura_base/2,
                self.player.rect.bottom,
                self.largura_base,
                self.altura_base
            )
        elif 3*pi/4 <= self.angulo < 4*pi/4:  # Esquerda
            self.imagem = pygame.transform.rotate(self.imagem_base, 0)
            self.rect = pygame.Rect(
                self.player.rect.left - self.altura_base,
                self.player.rect.centery - self.largura_base/2,
                self.altura_base,
                self.largura_base
            )
        else:  # Cima
            self.imagem = pygame.transform.rotate(self.imagem_base, -90)
            self.rect = pygame.Rect(
                self.player.rect.centerx - self.largura_base/2,
                self.player.rect.top - self.altura_base,
                self.largura_base,
                self.altura_base
            )

    def atualizar(self):
        """Atualiza o estado do ataque com espada.
        
        Returns:
            bool: True se o ataque ainda está ativo, False caso contrário
        """
        self.duracao -= 1
        self.atualizar_imagem()
        return self.duracao > 0

    def esta_ativo(self):
        """Verifica se o ataque com espada ainda está ativo.
        
        Returns:
            bool: True se o ataque está ativo, False caso contrário
        """
        return self.duracao > 0
    
    def desenhar(self, tela):
        """Desenha a espada na tela.
        
        Args:
            tela (pygame.Surface): Superfície onde a espada será desenhada
        """
        tela.blit(self.imagem, self.rect)

        