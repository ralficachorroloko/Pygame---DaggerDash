import pygame
from os import path
from config import *
from math import *
from Classes.Esqueleto import Flecha

class Shoot:
    """Classe que representa o tiro com arco do jogador.
    
    Gerencia o comportamento do tiro com arco, incluindo:
    - Criação e direção da flecha
    - Movimento e alcance
    - Colisão com inimigos
    """
    
    def __init__(self, player, mouse_pos, imagem):
        """Inicializa um novo tiro com arco.
        
        Args:
            player (Player): Referência ao jogador
            mouse_pos (tuple): Posição do mouse (x, y)
            imagem (str): Nome do arquivo da imagem da flecha
        """
        # Calcula direção entre player e mouse
        dx = mouse_pos[0] - player.rect.centerx
        dy = mouse_pos[1] - player.rect.centery
        angulo = atan2(dy, dx)

        # Normaliza a direção
        modulo = sqrt(dx**2 + dy**2)
        dx /= modulo
        dy /= modulo

        # Cria uma flecha como projétil
        self.flecha = Flecha(
            x=player.rect.centerx,
            y=player.rect.centery,
            dx=dx,
            dy=dy,
            velocidade=12,
            alcance=400
        )

    def atualizar(self):
        """Atualiza o estado do tiro.
        
        Returns:
            bool: True se a flecha atingiu seu alcance máximo, False caso contrário
        """
        # Retorna True se a flecha passou do alcance
        return self.flecha.atualizar()

    def desenhar(self, tela):
        """Desenha a flecha na tela.
        
        Args:
            tela (pygame.Surface): Superfície onde a flecha será desenhada
        """
        self.flecha.pinta(tela)

    def get_rect(self):
        """Retorna o retângulo de colisão da flecha.
        
        Returns:
            pygame.Rect: Retângulo de colisão da flecha
        """
        return self.flecha.rect