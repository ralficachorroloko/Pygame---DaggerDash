import pygame
import random
from config import *
from tela_inicial import *
from classes import *

tela = pygame.display.set_mode((640, 640))
relogio = pygame.time.Clock()

dungeon = Dungeon()
rodando = True

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_w:
                dungeon.mudar_sala("cima")
            elif evento.key == pygame.K_s:
                dungeon.mudar_sala("baixo")
            elif evento.key == pygame.K_a:
                dungeon.mudar_sala("esquerda")
            elif evento.key == pygame.K_d:
                dungeon.mudar_sala("direita")

    dungeon.sala_atual().desenhar(tela)
    pygame.display.flip()
    relogio.tick(60)

pygame.quit()