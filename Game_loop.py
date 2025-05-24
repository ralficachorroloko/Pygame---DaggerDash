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
    # Inicializa a dungeon com a matriz da primeira dungeon
    from Classes.DungeonData import DUNGEON_MATRIZES, criar_sala
    dungeon = Dungeon(dungeon_num=1)
    
    # Cria e adiciona as salas da primeira dungeon
    for i, tipo_sala in enumerate(DUNGEON_MATRIZES[1][0]):
        sala = criar_sala(tipo_sala)
        if sala:
            dungeon.adicionar_sala(sala, i, 0)
    
    jogador = dungeon.player
    espada = None
    shoots = []
    municao_atual = 4
    recarregando = False
    tempo_recarga = 0

    # Inicializa a música do jogo
    pygame.mixer.music.stop()  # Para a música anterior
    pygame.mixer.music.load(path.join('sons/track.mp3'))
    pygame.mixer.music.play(-1)  # -1 para loop infinito

    clock = pygame.time.Clock()
    running = True
    state = JOGO

    # Coração de vida
    vida_img = pygame.image.load(path.join("img", "player", "vida.png")).convert_alpha()
    vida_img = pygame.transform.scale(vida_img, (32, 32))

    # Imagem da flecha para mostrar munição
    flecha_img = pygame.image.load(path.join("img", "esqueleto", "flecha arqueiro.png")).convert_alpha()
    flecha_img = pygame.transform.scale(flecha_img, (20, 20))  # Flecha menor para o indicador

    # Variáveis para o sistema de munição e recarga
    FPS = 60  # Frames por segundo
    TEMPO_RECARGA = 3 * FPS  # 3 segundos em frames

    while running:
        clock.tick(FPS)

        # Verifica se o jogador perdeu todas as vidas
        if jogador.vidas <= 0:
            return GAME_OVER

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return QUIT
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not espada:  # Botão esquerdo do mouse
                    espada = Espada(jogador, pygame.mouse.get_pos(), "idle.png")
                elif event.button == 3 and jogador.tem_arco and not recarregando and municao_atual > 0:  # Botão direito do mouse
                    shoots.append(Shoot(jogador, pygame.mouse.get_pos(), "bow.png"))
                    municao_atual -= 1
                    jogador.estado = "bow"
                    jogador.shoot_timer = jogador.shoot_duracao

                    # Se acabou a munição, inicia a recarga
                    if municao_atual <= 0:
                        recarregando = True
                        tempo_recarga = TEMPO_RECARGA

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
            resultado = dungeon.passagem_porta(dx, dy)
            if resultado == VITORIA:
                return VITORIA

        # Sistema de munição e recarga
        if recarregando:
            tempo_recarga -= 1
            if tempo_recarga <= 0:
                recarregando = False
                municao_atual = 4

        # Atualiza e remove tiros se passaram do alcance
        for shoot in shoots[:]:
            if shoot.atualizar():  # True se passou do alcance
                shoots.remove(shoot)
            else:
                # Verifica colisão com inimigos na sala atual
                sala_atual = dungeon.sala_atual()
                if sala_atual:
                    for inimigo in sala_atual.inimigos[:]:
                        if shoot.get_rect().colliderect(inimigo.rect):
                            # Calcula a direção da flecha para o knockback
                            dx = shoot.flecha.dx
                            dy = shoot.flecha.dy
                            morreu, item = inimigo.receber_dano(100, (dx, dy))  # Passa a direção da flecha
                            if morreu:
                                sala_atual.inimigos.remove(inimigo)
                                if item:
                                    sala_atual.objetos.append(item)
                                    item.posicionar(inimigo.rect.centerx, inimigo.rect.centery)
                            shoots.remove(shoot)
                            break

        # Atualiza a sala atual
        sala_atual = dungeon.sala_atual()
        if sala_atual:
            sala_atual.atualizar(jogador)

        jogador.atualizar()

        # Verifica colisão da espada com inimigos
        if espada and espada.esta_ativo():
            espada.atualizar()
            
            # Verifica colisão com inimigos na sala atual
            sala_atual = dungeon.sala_atual()
            if sala_atual:
                for inimigo in sala_atual.inimigos[:]:
                    if espada.rect.colliderect(inimigo.rect):
                        if isinstance(inimigo, Kamikaze):
                            sala_atual.inimigos.remove(inimigo)
                        elif isinstance(inimigo, Esqueleto):
                            morreu, item = inimigo.receber_dano(100)  # Dano suficiente para matar
                            if morreu:
                                sala_atual.inimigos.remove(inimigo)
                                if item:
                                    sala_atual.objetos.append(item)
                                    item.posicionar(inimigo.rect.centerx, inimigo.rect.centery)
        else:
            espada = None

        # Desenha tudo
        tela.fill((0, 0, 0))
        dungeon.desenhar(tela)
        if espada:
            espada.desenhar(tela)
        for shoot in shoots:
            shoot.desenhar(tela)

        # Desenha as vidas
        for i in range(jogador.vidas):
            tela.blit(vida_img, (WIDTH - 40 * (i + 1), 10))

        # Desenha as flechas de munição no canto inferior direito
        for i in range(municao_atual):
            tela.blit(flecha_img, (WIDTH - 30 * (i + 1), HEIGHT - 30))

        pygame.display.flip()

    return state

