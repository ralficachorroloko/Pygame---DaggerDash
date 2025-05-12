from os import path
from Classes.Player import *
from Classes.Sala import *
from Classes.Parede import *
from Classes.Espada import *
from Classes.Kamikaze import *
from Classes.Dungeon import *   
import pygame
from config import *
from math import *


def tela_inicio(tela):

    pygame.mixer.init()
    pygame.mixer.music.load(path.join('8bitmusic.mp3'))
    pygame.mixer.music.play(-1)  

    clock = pygame.time.Clock()
    timer = 0
    mostrar_quadrado = True

    inicial = pygame.image.load(path.join("img" ,'inicio.png')).convert()
    inicial = pygame.transform.scale(inicial, (WIDTH, HEIGHT))
    inicial_rect = inicial.get_rect()

    running = True
    state = INICIO  # Estado inicial

    while running:

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = QUIT
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print("Pressionou ENTER - Mudando para TESTES")
                    state = TESTES
                    running = False
                if event.key == pygame.K_2:
                    print("Pressionou 2 - Mudando para TESTES2")
                    state = TESTES2
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
            # Adiciona texto para mostrar as opções
            fonte = pygame.font.Font(None, 36)
            texto1 = fonte.render("Pressione ENTER para Teste 1", True, WHITE)
            texto2 = fonte.render("Pressione 2 para Teste 2", True, WHITE)
            tela.blit(texto1, (200, 420))
            tela.blit(texto2, (200, 460))

        pygame.display.flip()

    print("Retornando estado:", state)
    return state