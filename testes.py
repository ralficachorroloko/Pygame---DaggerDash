import pygame
import random
from os import path
from classes import *
from config import *

def tela_teste(tela):
    jogador = Player(400, 300, "idle.png", 10, (50, 50))
    parede = Parede(300, 400, 100, 300)

    paredes_mapa = [parede]

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
            pos_anterior = jogador.rect.topleft
            jogador.mover(0, -1)
        if keys[pygame.K_DOWN]:
            pos_anterior = jogador.rect.topleft
            jogador.mover(0, 1)
        if keys[pygame.K_LEFT]:
            pos_anterior = jogador.rect.topleft
            jogador.mover(-1, 0)
        if keys[pygame.K_RIGHT]:
            pos_anterior = jogador.rect.topleft
            jogador.mover(1, 0)

        for parede in paredes_mapa:
            if jogador.rect.colliderect(parede.rect):
                jogador.rect.topleft = pos_anterior

        tela.fill(BLACK)
        jogador.desenhar(tela)
        parede.desenhar(tela, True)

        pygame.display.flip()