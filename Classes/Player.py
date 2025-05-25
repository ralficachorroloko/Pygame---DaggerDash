from os import path
import pygame
from itens import Inventario

class Player:
    def __init__(self, x, y, imagem_idle, velocidade, tamanho):
        # Carrega as imagens de idle, walk e bow
        idle_img = pygame.image.load(path.join("img", "player", imagem_idle)).convert_alpha()
        self.idle_imagem = pygame.transform.scale(idle_img, tamanho)

        walk_img = pygame.image.load(path.join("img", "player", "walk.png")).convert_alpha()
        self.walk_imagem = pygame.transform.scale(walk_img, tamanho)

        bow_img = pygame.image.load(path.join("img", "player", "bow.png")).convert_alpha()
        self.bow_imagem = pygame.transform.scale(bow_img, tamanho)

        self.imagem_original = self.idle_imagem
        self.rect = self.imagem_original.get_rect(topleft=(x, y))
        self.estado = "idle"

        # Atributos base do jogador
        self.velocidade = velocidade 
        self.velocidade_original = velocidade
        self.dano = 1
        self.defesa = 0
        self.velocidade_ataque = 1.0
        self.vida_maxima = 5
        self.vida = 5

        self.direcao = None
        self.espelhado = False

        # Controle de animação
        self.anim_frame = 0
        self.anim_intervalo = 10  # Frames entre as trocas

        self.shoot_timer = 0
        self.shoot_duracao = 10  # quantos frames ele fica na pose de tiro

        # Dash
        self.dash_ativo = False
        self.dash_frames = 0
        self.dash_duracao = 8
        self.dash_cooldown = 0
        self.dash_cooldown_max = 120
        self.dash_direcao = [0, 0]

        self.tem_arco = True

        #SISTEMA DE VIDAS
        self.vidas = 5           # Quantidade de vidas
        self.invencivel = False  # Evita dano múltiplo em um frame
        self.inv_frames = 0      # Tempo de invencibilidade
        self.inv_max = 60        # Duração da invencibilidade 
        self.flash_dano = 0      # Contador para o efeito de flash vermelho

        # Sistema de Inventário
        self.inventario = Inventario()
        self.inventario.set_jogador(self)  # Passa a referência do jogador para o inventário

    def equipar_item(self, item):
        if item in self.inventario.itens and not item.equipado:
            item.equipado = True
            self.inventario.itens_equipados.append(item)
            # Aplica os efeitos do item
            if hasattr(item, 'aplicar_efeitos'):
                item.aplicar_efeitos(self)
            return True
        return False

    def desequipar_item(self, item):
        if self.inventario.desequipar_item(item):
            # Remove os efeitos do item
            if hasattr(item, 'remover_efeitos'):
                item.remover_efeitos(self)
            return True
        return False

    def adicionar_item(self, item):
        # Adiciona o item ao inventário (os efeitos serão aplicados pelo inventário)
        return self.inventario.adicionar_item(item)

    def remover_item(self, item):
        if self.inventario.remover_item(item):
            # Remove os efeitos do item
            if hasattr(item, 'remover_efeitos'):
                item.remover_efeitos(self)
            return True
        return False

    def obter_itens_equipados(self):
        return self.inventario.obter_itens_equipados()

    def obter_itens_inventario(self):
        return self.inventario.obter_itens_inventario()

    def desenhar(self, tela):
        if self.estado == "bow":
            imagem_base = self.bow_imagem
        elif self.estado == "walk":
            imagem_base = self.walk_imagem
        else:
            imagem_base = self.idle_imagem

        if self.espelhado:
            imagem_a_usar = pygame.transform.flip(imagem_base, True, False)
        else:
            imagem_a_usar = imagem_base

        if self.dash_ativo:
            imagem_a_usar = imagem_a_usar.copy()
            imagem_a_usar.set_alpha(128)

        # Efeito de flash vermelho quando toma dano
        if self.flash_dano > 0:
            imagem_a_usar = imagem_a_usar.copy()
            imagem_a_usar.fill((255, 0, 0, 128), special_flags=pygame.BLEND_RGBA_MULT)

        tela.blit(imagem_a_usar, self.rect)

    def mover(self, dx, dy):
        if self.estado != "bow":  # <-- Protege contra sobrescrever "bow"
            if dx != 0 or dy != 0:
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
            # Normaliza o movimento para evitar problemas com diagonais
            if dx != 0 and dy != 0:
                dx = dx * 0.7071  # 1/sqrt(2)
                dy = dy * 0.7071
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

        if self.invencivel:
            self.inv_frames -= 1
            if self.inv_frames <= 0:
                self.invencivel = False

        # Atualiza o efeito de flash vermelho
        if self.flash_dano > 0:
            self.flash_dano -= 1

        if self.estado == "bow":
            self.shoot_timer -= 1
            if self.shoot_timer <= 0:
                self.estado = "idle"

    def levar_dano(self):
        if not self.invencivel:
            self.vidas -= 1
            self.invencivel = True
            self.inv_frames = self.inv_max
            self.flash_dano = 5  # Inicia o efeito de flash vermelho
