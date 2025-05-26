from os import path
import pygame
from config import *

def tela_vitoria(tela):
    """Função que gerencia a tela de Vitória.
    
    Mostra a tela de vitória e aguarda o jogador pressionar ENTER para voltar
    à tela inicial.
    
    Args:
        tela (pygame.Surface): Superfície onde a tela de vitória será renderizada
        
    Returns:
        int: Estado do jogo após sair da tela de vitória (INICIO)
    """
    pygame.mixer.init()
    pygame.mixer.music.load(path.join('sons/8bitmusic.mp3'))
    pygame.mixer.music.play(-1)

    clock = pygame.time.Clock()

    # Carrega a imagem de vitória
    vitoria_img = pygame.image.load(path.join("img", "Imagem final.png")).convert()
    vitoria_img = pygame.transform.scale(vitoria_img, (WIDTH, HEIGHT))
    vitoria_rect = vitoria_img.get_rect()

    running = True
    state = VITORIA

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = QUIT
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    state = INICIO
                    running = False

        tela.fill(BLACK)
        tela.blit(vitoria_img, vitoria_rect)
        pygame.display.flip()

    return state 