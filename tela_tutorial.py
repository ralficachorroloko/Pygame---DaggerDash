from os import path
import pygame
from config import *

def tela_tutorial(tela):
    """Função que gerencia a tela de Tutorial.
    
    Mostra a tela de Tutorial e aguarda o jogador pressionar ENTER para continuar
    para o jogo ou ESC para sair.
    
    Args:
        tela (pygame.Surface): Superfície onde a tela de Tutorial será renderizada
        
    Returns:
        int: Estado do jogo após sair da tela de Tutorial (JOGO ou QUIT)
    """
    clock = pygame.time.Clock()
    timer = 0
    mostrar_quadrado = True

    # Carrega a imagem de fundo do tutorial
    tutorial_img = pygame.image.load(path.join("img", "Tutorial.png")).convert_alpha()
    # Redimensiona a imagem para cobrir toda a tela
    tutorial_img = pygame.transform.scale(tutorial_img, (WIDTH, HEIGHT))
    tutorial_rect = tutorial_img.get_rect()
    tutorial_rect.topleft = (0, 0)  # Posiciona a imagem no canto superior esquerdo

    running = True
    state = TUTORIAL  # Estado inicial

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = QUIT
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Tecla Enter
                    state = JOGO  # Vai para o jogo
                    running = False
                elif event.key == pygame.K_ESCAPE:  # Tecla ESC
                    state = QUIT
                    running = False

        # Preenche a tela com preto antes de desenhar a imagem
        tela.fill(BLACK)
        
        # Desenha a imagem do tutorial
        tela.blit(tutorial_img, tutorial_rect)

        # Pisca o retângulo
        timer += clock.get_time()
        if timer >= 500:
            mostrar_quadrado = not mostrar_quadrado
            timer = 0

        if mostrar_quadrado:
            pygame.draw.rect(tela, BLACK, (25, 485, 1000, 150))

        pygame.display.flip()

    return state 