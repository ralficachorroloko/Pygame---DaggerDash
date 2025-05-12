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

def tela_teste(tela):
    # === Criação do jogador e inimigos ===
    jogador = Player(400, 300, "idle.png", 10, (50, 50))
    parede = Parede(300, 400, 100, 300)
    inimigo = Kamikaze(300, 100, 1, (25, 25), 200, "idle.png")

    paredes_mapa = [parede]
    inimigos = [inimigo]
    espada = None  # Inicializa sem espada

    # === Música de fundo ===
    pygame.mixer.init()
    pygame.mixer.music.load(path.join('8bitmusic.mp3'))
    pygame.mixer.music.play(-1)  

    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(FPS)

        # === Verifica eventos ===
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return QUIT

        # === Controle de movimento do jogador ===
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            jogador.direcao = "w"
            pos_anterior = jogador.rect.topleft
            jogador.mover(0, -1)
            for parede in paredes_mapa:
                if jogador.rect.colliderect(parede.rect):
                    jogador.rect.topleft = pos_anterior
        if keys[pygame.K_DOWN]:
            jogador.direcao = "s"
            pos_anterior = jogador.rect.topleft
            jogador.mover(0, 1)
            for parede in paredes_mapa:
                if jogador.rect.colliderect(parede.rect):
                    jogador.rect.topleft = pos_anterior
        if keys[pygame.K_LEFT]:
            jogador.direcao = "a"
            pos_anterior = jogador.rect.topleft
            jogador.mover(-1, 0)
            for parede in paredes_mapa:
                if jogador.rect.colliderect(parede.rect):
                    jogador.rect.topleft = pos_anterior
        if keys[pygame.K_RIGHT]:
            jogador.direcao = "d"
            pos_anterior = jogador.rect.topleft
            jogador.mover(1, 0)
            for parede in paredes_mapa:
                if jogador.rect.colliderect(parede.rect):
                    jogador.rect.topleft = pos_anterior

        # === Atualiza e desenha o jogador ===
        tela.fill(BLACK)
        jogador.desenhar(tela)

        # === Desenha as paredes ===
        parede.desenhar(tela, True)

        # === Atualiza e desenha os inimigos ===
        for kamikaze in inimigos[:]:
            kamikaze.atualizar(jogador)
            if kamikaze.rect.colliderect(jogador.rect):
                inimigos.remove(kamikaze)
            else:
                kamikaze.desenhar(tela)

        # === Criação da espada ao apertar espaço ===
        if keys[pygame.K_SPACE] and not espada:
            espada = Espada(jogador, 5, jogador.direcao, "idle.png")  # Substitua por sua imagem da espada

        # === Atualiza e desenha a espada se ela existir e estiver ativa ===
        if espada and espada.esta_ativo():
            espada.desenhar(tela)
            espada.atualizar()
        else:
            espada = None  # Destrói a espada se não estiver mais ativa

        # === Atualiza a tela ===
        pygame.display.flip()