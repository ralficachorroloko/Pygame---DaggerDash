from os import path
import pygame
from config import *

def tela_game_over(tela):
    """Função que gerencia a tela de Game Over.
    
    Mostra a tela de Game Over e aguarda o jogador pressionar ENTER para voltar
    à tela inicial ou ESC para sair.
    
    Args:
        tela (pygame.Surface): Superfície onde a tela de Game Over será renderizada
        
    Returns:
        int: Estado do jogo após sair da tela de Game Over (INICIO ou QUIT)
    """
    pygame.mixer.init()
    pygame.mixer.music.load(path.join('sons/gameover.mp3'))
    pygame.mixer.music.play()  

    clock = pygame.time.Clock()
    timer = 0
    mostrar_quadrado = True

    # Carrega a imagem de fundo do game over
    game_over_img = pygame.image.load(path.join("img", "game_over.png")).convert_alpha()
    # Redimensiona a imagem para cobrir toda a tela
    game_over_img = pygame.transform.scale(game_over_img, (WIDTH, HEIGHT))
    game_over_rect = game_over_img.get_rect()
    game_over_rect.topleft = (0, 0)  # Posiciona a imagem no canto superior esquerdo

    running = True
    state = GAME_OVER  # Estado inicial

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = QUIT
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Tecla Enter
                    state = INICIO  # Volta para a tela inicial
                    running = False

        # Preenche a tela com preto antes de desenhar a imagem
        tela.fill(BLACK)
        
        # Desenha a imagem de game over
        tela.blit(game_over_img, game_over_rect)

        # Pisca "pressione enter para reiniciar"
        timer += clock.get_time()
        if timer >= 500:
            mostrar_quadrado = not mostrar_quadrado
            timer = 0

        if mostrar_quadrado:
            pygame.draw.rect(tela, BLACK, (25, 400, 1000, 150))

        pygame.display.flip()

    return state 