from os import path
import pygame

class Player:
    def __init__(self, x, y, imagem, velocidade, tamanho):
        img = pygame.image.load(path.join("img", "player", imagem)).convert_alpha()
        self.imagem = pygame.transform.scale(img, tamanho)
        self.rect = self.imagem.get_rect(topleft=(x, y))
        self.velocidade = velocidade 
        
        self.velocidade_original = velocidade  # Guarda a velocidade original
        self.direcao = None
        self.dash_ativo = False
        self.dash_frames = 0
        self.dash_duracao = 10  # Número de frames que o dash vai durar
        self.dash_cooldown = 0  # Contador para o cooldown
        self.dash_cooldown_max = 180  # 3 segundos (60 frames por segundo * 3)

    def desenhar(self, tela):
        tela.blit(self.imagem, self.rect)

    def mover(self, dx, dy):
        self.rect.x += dx * self.velocidade
        self.rect.y += dy * self.velocidade

    def teleportar_para(self, x, y):
        self.rect.topleft = (x, y)
    
    def dash(self):
        if not self.dash_ativo and self.dash_cooldown <= 0:  # Só ativa se não estiver ativo e cooldown acabou
            self.dash_ativo = True
            self.velocidade = self.velocidade_original * 2
            self.dash_frames = 0

    def atualizar(self):
        if self.dash_ativo:
            self.dash_frames += 1
            if self.dash_frames >= self.dash_duracao:
                self.dash_ativo = False
                self.velocidade = self.velocidade_original
                self.dash_cooldown = self.dash_cooldown_max  # Inicia o cooldown
        
        if self.dash_cooldown > 0:  # Atualiza o cooldown
            self.dash_cooldown -= 1

