from os import path
from Classes.Player import Player   
from Classes.Sala import Sala
from Classes.Parede import Parede
from Classes.Espada import Espada
from Classes.Kamikaze import Kamikaze
from Classes.Dungeon import Dungeon   
import pygame
from config import *
from math import *


def tela_inicio(tela):
    """Função que gerencia a tela inicial do jogo.
    
    Mostra a tela de título e aguarda o jogador pressionar ENTER para começar
    ou ESC para sair.
    
    Args:
        tela (pygame.Surface): Superfície onde a tela inicial será renderizada
        
    Returns:
        int: Estado do jogo após sair da tela inicial (JOGO ou QUIT)
    """
    pygame.mixer.init()
    pygame.mixer.music.load(path.join('sons/8bitmusic.mp3'))
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
                    print("Pressionou enter - Mudando para jogo")   
                    pygame.mixer.music.stop()  # Para a música antes de mudar de tela
                    state = JOGO
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

        pygame.display.flip()

    print("Retornando estado:", state)
    return state