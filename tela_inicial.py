import pygame
import random
from os import path

from config import *



def tela_inicio(tela):
    clock = pygame.time.Clock()
    timer = 0
    mostrar_quadrado = True

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print("Pressionou ENTER")
                    state = QUIT
                    running = False

        tela.fill(BLACK)
        tela.blit(inicial, inicial_rect)

        #pisca "pressione enter para jogar"
        timer += clock.get_time()
        if timer >= 500:
            mostrar_quadrado = not mostrar_quadrado
            timer = 0

        if mostrar_quadrado == True:
            pygame.draw.rect(tela, BLACK, (160, 400, 500, 150))

        pygame.display.flip()

    return state