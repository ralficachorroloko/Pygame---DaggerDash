from os import path
from Classes.Player import *
from Classes.Sala import *
from Classes.Parede import *
from Classes.Espada import *
from Classes.Kamikaze import *
from Classes.Dungeon import *
from Classes.Shoot import *
from Classes.DungeonData import *
import pygame
from config import *
from math import *

def tela_jogo(tela):
    dungeon = Dungeon(dungeon_num=1)

    for i, tipo_sala in enumerate(DUNGEON_MATRIZES[1][0]):
        sala = criar_sala(tipo_sala)
        if sala:
            dungeon.adicionar_sala(sala, i, 0)

    pygame.mixer.init()
    pygame.mixer.music.load(path.join('sons/8bitmusic.mp3'))
    pygame.mixer.music.play(-1)  

    clock = pygame.time.Clock()
    espada = None
    jogador = dungeon.player
    shoots = []
    jogador.tem_arco = True
    cooldown_shoot = 0
    running = True

    # Coração de vida
    vida_img = pygame.image.load(path.join("img", "player", "vida.png")).convert_alpha()
    vida_img = pygame.transform.scale(vida_img, (32, 32))

    while running:
        clock.tick(FPS)

        # Verifica se o jogador perdeu todas as vidas
        if jogador.vidas <= 0:
            return GAME_OVER

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return QUIT
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not espada:
                    espada = Espada(jogador, pygame.mouse.get_pos(), "idle.png")

        # Movimento
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_w]:
            dy = -1
            jogador.direcao = "w"
        if keys[pygame.K_s]:
            dy = 1
            jogador.direcao = "s"
        if keys[pygame.K_a]:
            dx = -1
            jogador.direcao = "a"
        if keys[pygame.K_d]:
            dx = 1
            jogador.direcao = "d"
        if keys[pygame.K_LSHIFT]:
            jogador.dash()

        if dx != 0 or dy != 0:
            dungeon.passagem_porta(dx, dy)

        # Disparo com botão direito
        if pygame.mouse.get_pressed()[2] and jogador.tem_arco and cooldown_shoot == 0:
            shoots.append(Shoot(jogador, pygame.mouse.get_pos(), "bow.png"))  # Pode trocar imagem depois
            cooldown_shoot = 15

            jogador.estado = "bow"
            jogador.shoot_timer = jogador.shoot_duracao

        if cooldown_shoot > 0:
            cooldown_shoot -= 1

        # Atualiza e remove tiros se passaram do alcance
        for shoot in shoots[:]:
            if shoot.atualizar():  # True se passou do alcance
                shoots.remove(shoot)

        dungeon.atualizar()
        jogador.atualizar()

        # Desenha tudo
        tela.fill((0, 0, 0))
        dungeon.desenhar(tela)

        if espada and espada.esta_ativo():
            espada.desenhar(tela)
            espada.atualizar()
        else:
            espada = None

        for shoot in shoots:
            shoot.desenhar(tela)

        # Desenha as vidas do jogador
        for i in range(jogador.vidas):           
            tela.blit(vida_img, (WIDTH - 40 * (i + 1), 10))

        pygame.display.flip()

    return QUIT

