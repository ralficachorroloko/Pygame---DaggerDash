from enum import Enum
import random
from os import path
import pygame

class Raridade(Enum):
    COMUM = {"chance": 0.60, "multiplicador": 1.0, "cor": "branco"}
    INCOMUM = {"chance": 0.25, "multiplicador": 1.5, "cor": "verde"}
    RARO = {"chance": 0.10, "multiplicador": 2.0, "cor": "azul"}
    ÉPICO = {"chance": 0.05, "multiplicador": 2.5, "cor": "roxo"}
    LENDÁRIO = {"chance": 0.00, "multiplicador": 3.0, "cor": "laranja"}

class Item:
    def __init__(self, nome, descricao, raridade="COMUM", atributos_base=None, imagem_nome=None):
        self.nome = nome
        self.descricao = descricao
        self.raridade = Raridade[raridade]
        self.equipado = False
        self.atributos_base = atributos_base or {}
        self.atributos = self.calcular_atributos()
        
        if imagem_nome:
            self.imagem = pygame.image.load(path.join("img", "itens", imagem_nome)).convert_alpha()
            self.tamanho = (30, 30)
            self.imagem = pygame.transform.scale(self.imagem, self.tamanho)
            self.rect = None
    
    def posicionar(self, x, y):
        if hasattr(self, 'imagem'):
            self.rect = pygame.Rect(x, y, self.tamanho[0], self.tamanho[1])
            self.rect.centerx = x
            self.rect.centery = y
    
    def pinta(self, tela):
        if hasattr(self, 'imagem') and self.rect:
            tela.blit(self.imagem, self.rect)

    def calcular_atributos(self):
        multiplicador = self.raridade.value["multiplicador"]
        atributos_calculados = {}
        for chave, valor in self.atributos_base.items():
            atributos_calculados[chave] = valor * multiplicador
        return atributos_calculados

    def obter_nome_colorido(self):
        return f"{self.raridade.value['cor']}: {self.nome}"

    def aplicar_efeitos(self, jogador):
        if not self.equipado:
            for atributo, valor in self.atributos.items():
                valor_atual = getattr(jogador, atributo, 0)
                setattr(jogador, atributo, valor_atual + valor)
            self.equipado = True

    def remover_efeitos(self, jogador):
        if self.equipado:
            for atributo, valor in self.atributos.items():
                valor_atual = getattr(jogador, atributo, 0)
                setattr(jogador, atributo, valor_atual - valor)
            self.equipado = False

def rolar_raridade():
    rolagem = random.random()
    acumulado = 0
    for raridade in Raridade:
        acumulado += raridade.value["chance"]
        if rolagem <= acumulado:
            return raridade.name
    return Raridade.COMUM.name

class Inventario:
    def __init__(self):
        self.itens = []
        self.itens_equipados = []

    def adicionar_item(self, item):
        self.itens.append(item)
        self.equipar_item(item)
        return True

    def remover_item(self, item):
        if item in self.itens:
            if item.equipado:
                self.desequipar_item(item)
            self.itens.remove(item)
            return True
        return False

    def equipar_item(self, item):

        if item in self.itens and not item.equipado:
            item.equipado = True
            self.itens_equipados.append(item)
            return True
        return False

    def desequipar_item(self, item):
        if item in self.itens_equipados:
            item.equipado = False
            self.itens_equipados.remove(item)
            return True
        return False

    def obter_itens_equipados(self):
                return self.itens_equipados

    def obter_itens_inventario(self):
        return self.itens

    def possui_item(self, nome_item):
        for item in self.itens:
            if item.nome == nome_item:
                return True
        return False

class Halter(Item):
    def __init__(self, raridade="COMUM"):
        super().__init__(
            nome="Halter",
            descricao="Um halter que aumenta o dano",
            raridade=raridade,
            atributos_base={"dano": 5},
            imagem_nome="Halter.png"
        )

class BotasVelozes(Item):
    def __init__(self, raridade="COMUM"):
        super().__init__(
            nome="Botas Velozes",
            descricao="Botas mágicas que aumentam a velocidade de movimento",
            raridade=raridade,
            atributos_base={"velocidade": 2},
            imagem_nome="Botas da velocidade.png"
        )

class Adrenalina(Item):
    def __init__(self, raridade="COMUM"):
        super().__init__(
            nome="Seringa de Adrenalina",
            descricao="Seringa de adrenalina que aumenta a velocidade de ataque",
            raridade=raridade,
            atributos_base={"velocidade_ataque": 0.3},
            imagem_nome="seringa.png"
        )

class AmuletoDeVida(Item):
    def __init__(self, raridade="COMUM"):
        super().__init__(
            nome="Amuleto de Vida",
            descricao="Um amuleto mágico que aumenta os pontos de vida",
            raridade=raridade,
            atributos_base={
                "vida_maxima": 20,
                "vida": 20
            },
            imagem_nome="amuleto de vida.png"
        )

    def aplicar_efeitos(self, jogador):
        if not self.equipado:
            # Primeiro aplica o aumento da vida máxima
            vida_maxima_atual = getattr(jogador, "vida_maxima", 0)
            vida_maxima_nova = vida_maxima_atual + self.atributos["vida_maxima"]
            setattr(jogador, "vida_maxima", vida_maxima_nova)
            
            # Se a vida atual for menor que a máxima, recupera a vida
            vida_atual = getattr(jogador, "vida", 0)
            if vida_atual < vida_maxima_nova:
                setattr(jogador, "vida", vida_maxima_nova)
            
            self.equipado = True

    def remover_efeitos(self, jogador):
        if self.equipado:
            # Remove o aumento da vida máxima
            vida_maxima_atual = getattr(jogador, "vida_maxima", 0)
            vida_maxima_nova = vida_maxima_atual - self.atributos["vida_maxima"]
            setattr(jogador, "vida_maxima", vida_maxima_nova)
            
            # Se a vida atual for maior que a nova vida máxima, ajusta para a máxima
            vida_atual = getattr(jogador, "vida", 0)
            if vida_atual > vida_maxima_nova:
                setattr(jogador, "vida", vida_maxima_nova)
            
            self.equipado = False

def criar_item_aleatorio():
    # Lista de itens disponíveis (sem o amuleto de defesa)
    itens_disponiveis = [
        AmuletoDeVida,  # Comum (60%)
        BotasVelozes,   # Incomum (25%)
        Halter,         # Raro (10%)
        Adrenalina      # Épico (5%)
    ]
    
    # Escolhe o item baseado na raridade
    raridade = rolar_raridade()
    
    # Mapeia a raridade para o item correspondente
    if raridade == "COMUM":
        return AmuletoDeVida(raridade)
    elif raridade == "INCOMUM":
        return BotasVelozes(raridade)
    elif raridade == "RARO":
        return Halter(raridade)
    elif raridade == "ÉPICO":
        return Adrenalina(raridade)
    
    # Fallback para comum se algo der errado
    return AmuletoDeVida("COMUM")
