import pygame
import random
from os import path

from config import *

def tela_inicio(tela):
    clock = pygame.time.Clock()

    inicial = pygame.image.load(path.join('inicio.png')).convert()
    inicial = pygame.transform.scale(inicial, (WIDTH, HEIGHT))
    inicial_rect = inicial.get_rect()

    running = True
    while running:

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = QUIT
                running = False

        tela.fill(BLACK)
        tela.blit(inicial, inicial_rect)

        pygame.display.flip()

    return state