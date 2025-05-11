import pygame
import random
from os import path
from classes import *
from config import *

def tela_teste(tela):
    jogador = Player(400, 300, "idle.png", 10, (50, 50))
    parede = Parede(300, 400, 100, 300)

    pygame.mixer.init()
    pygame.mixer.music.load(path.join('8bitmusic.mp3'))
    pygame.mixer.music.play(-1)  

    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = QUIT
                return state
            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            jogador.mover(0, -1)
        if keys[pygame.K_DOWN]:
            jogador.mover(0, 1)
        if keys[pygame.K_LEFT]:
            jogador.mover(-1, 0)

        if keys[pygame.K_RIGHT]:
            jogador.mover(1, 0)

        tela.fill(BLACK)
        jogador.desenhar(tela)
        parede.desenhar(tela, True)

        pygame.display.flip()