from os import path
import pygame

class Player:
    def __init__(self, x, y, imagem_idle, velocidade, tamanho):
        # Carrega as imagens de idle e walk
        idle_img = pygame.image.load(path.join("img", "player", imagem_idle)).convert_alpha()
        self.idle_imagem = pygame.transform.scale(idle_img, tamanho)

        walk_img = pygame.image.load(path.join("img", "player", "walk.png")).convert_alpha()
        self.walk_imagem = pygame.transform.scale(walk_img, tamanho)

        self.imagem_original = self.idle_imagem
        self.rect = self.imagem_original.get_rect(topleft=(x, y))
        self.estado = "idle"

        self.velocidade = velocidade 
        self.velocidade_original = velocidade
        self.direcao = None
        self.espelhado = False

        # Controle de animação
        self.anim_frame = 0
        self.anim_intervalo = 10  # Frames entre as trocas

        # Dash
        self.dash_ativo = False
        self.dash_frames = 0
        self.dash_duracao = 8
        self.dash_cooldown = 0
        self.dash_cooldown_max = 120
        self.dash_direcao = [0, 0]

        self.tem_arco = False

    def desenhar(self, tela):
        imagem_base = self.walk_imagem if self.estado == "walk" else self.idle_imagem
        if self.espelhado:
            imagem_a_usar = pygame.transform.flip(imagem_base, True, False)
        else:
            imagem_a_usar = imagem_base

        if self.dash_ativo:
            imagem_a_usar = imagem_a_usar.copy()
            imagem_a_usar.set_alpha(128)

        tela.blit(imagem_a_usar, self.rect)

    def mover(self, dx, dy):
        if dx != 0 or dy != 0:
            # Alterna entre walk e idle a cada intervalo
            self.anim_frame += 1
            if self.anim_frame >= self.anim_intervalo:
                self.estado = "walk" if self.estado == "idle" else "idle"
                self.anim_frame = 0
        else:
            self.estado = "idle"
            self.anim_frame = 0

        # Atualiza espelhamento
        if dx > 0:
            self.espelhado = False
        elif dx < 0:
            self.espelhado = True

        # Movimento
        if self.dash_ativo:
            self.rect.x += self.dash_direcao[0] * self.velocidade
            self.rect.y += self.dash_direcao[1] * self.velocidade
        else:
            self.rect.x += dx * self.velocidade
            self.rect.y += dy * self.velocidade

    def teleportar_para(self, x, y):
        self.rect.topleft = (x, y)
    
    def dash(self):
        if not self.dash_ativo and self.dash_cooldown <= 0:
            if self.direcao == "w":
                self.dash_direcao = [0, -1]
            elif self.direcao == "s":
                self.dash_direcao = [0, 1]
            elif self.direcao == "a":
                self.dash_direcao = [-1, 0]
            elif self.direcao == "d":
                self.dash_direcao = [1, 0]
            else:
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
                self.dash_cooldown = self.dash_cooldown_max
        
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1

