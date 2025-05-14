from os import path
import pygame

class Player:
    def __init__(self, x, y, imagem, velocidade, tamanho):
        img = pygame.image.load(path.join("img", "player", imagem)).convert_alpha()
        self.imagem = pygame.transform.scale(img, tamanho)
        self.imagem_original = self.imagem.copy()  # Guarda a imagem original
        self.rect = self.imagem.get_rect(topleft=(x, y))

        self.velocidade = velocidade 
        self.velocidade_original = velocidade  # Guarda a velocidade original

        self.direcao = None
        
        self.dash_ativo = False
        self.dash_frames = 0
        self.dash_duracao = 8  # Número de frames que o dash vai durar
        self.dash_cooldown = 0  # Contador para o cooldown
        self.dash_cooldown_max = 120  # 2 segundos (60 frames por segundo * 2)
        self.dash_direcao = [0, 0]  # Direção do dash [dx, dy]

        self.tem_arco = False

    def desenhar(self, tela):
        if self.dash_ativo:
            # Cria uma cópia da imagem com transparência
            imagem_dash = self.imagem_original.copy()
            imagem_dash.set_alpha(128)  # Define a transparência (0-255)
            tela.blit(imagem_dash, self.rect)
        else:
            tela.blit(self.imagem, self.rect)

    def mover(self, dx, dy):
        if self.dash_ativo:
            # Durante o dash, usa a direção armazenada
            self.rect.x += self.dash_direcao[0] * self.velocidade
            self.rect.y += self.dash_direcao[1] * self.velocidade
        else:
            # Movimento normal
            self.rect.x += dx * self.velocidade
            self.rect.y += dy * self.velocidade

    def teleportar_para(self, x, y):
        self.rect.topleft = (x, y)
    
    def dash(self):
        if not self.dash_ativo and self.dash_cooldown <= 0:  # Só ativa se não estiver ativo e cooldown acabou
            # Armazena a direção atual do movimento
            if self.direcao == "w":
                self.dash_direcao = [0, -1]
            elif self.direcao == "s":
                self.dash_direcao = [0, 1]
            elif self.direcao == "a":
                self.dash_direcao = [-1, 0]
            elif self.direcao == "d":
                self.dash_direcao = [1, 0]
            else:
                # Se não houver direção definida, não ativa o dash
                return
                
            self.dash_ativo = True
            self.velocidade = self.velocidade_original * 3
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

