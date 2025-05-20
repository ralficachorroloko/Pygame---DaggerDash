import pygame
from os import path
from config import *
from math import *
from Classes.Esqueleto import Flecha

class Shoot:
    def __init__(self, player, mouse_pos, imagem):
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
        # Retorna True se a flecha passou do alcance
        return self.flecha.atualizar()

    def desenhar(self, tela):
        self.flecha.pinta(tela)

    def get_rect(self):
        return self.flecha.rect