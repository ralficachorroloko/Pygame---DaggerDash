import pygame
import random
from os import path

from config import *

def init_screen(screen):
    clock = pygame.time.Clock()

    background = pygame.image.load(path.join('inicio.png')).convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    background_rect = background.get_rect()

    font = pygame.font.Font(None, 60)

        # Define botão fora do loop
        # Posição do botão "JOGAR" na parte inferior

    

    button_width = 200
    button_height = 80
    button_x = (WIDTH - button_width) // 2
    button_y = HEIGHT - button_height - 40  # 40 px acima da base

    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    # Texto centralizado no botão
    text = font.render("JOGAR", True, WHITE)
    text_rect = text.get_rect(center=button_rect.center)
    titulo = font.render("Date com Mentao", True, WHITE)
    titulo_rect = titulo.get_rect(center=(WIDTH // 2, 40))

    running = True
    while running:

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = QUIT
                running = False
            if event.type == pygame.KEYUP:
                state = QUIT
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                if button_rect.collidepoint(event.pos):
                    state = MAPA
                    running = False

        screen.fill(BLACK)
        screen.blit(background, background_rect)

        # Desenha botão por cima do fundo
        pygame.draw.rect(screen, RED, button_rect, border_radius=12)
        screen.blit(text, text_rect)
        screen.blit(titulo, titulo_rect)

        pygame.display.flip()

    return state