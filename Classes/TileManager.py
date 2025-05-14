import pygame
import os
import random

class TileManager:
    def __init__(self):
        self.tile_size = 16  # Tamanho dos tiles ajustado para 16x16 pixels
        self.tiles = {
            'chao': {
                'centro': [],
                'borda': []
            },
            'paredes': {
                'cima': [],
                'baixo': [],
                'esquerda': [],
                'direita': [],
                'canto': {
                    'superior_esquerdo': [],
                    'superior_direito': [],
                    'inferior_esquerdo': [],
                    'inferior_direito': []
                }
            }
        }
        self._carregar_tiles()
    
    def _carregar_tiles(self):
        # Carrega tiles do chão
        chao_path = os.path.join('tiles_exportados', 'chão')
        for tile_file in os.listdir(chao_path):
            if tile_file.endswith('.png'):
                tile_path = os.path.join(chao_path, tile_file)
                tile_img = pygame.image.load(tile_path).convert_alpha()
                # Redimensiona o tile para 16x16
                tile_img = pygame.transform.scale(tile_img, (self.tile_size, self.tile_size))
                # Classifica os tiles do chão em centro ou borda
                if 'borda' in tile_file.lower():
                    self.tiles['chao']['borda'].append(tile_img)
                else:
                    self.tiles['chao']['centro'].append(tile_img)
        
        # Carrega tiles das paredes
        paredes_path = os.path.join('tiles_exportados', 'paredes')
        for direcao in ['cima', 'baixo', 'esquerda', 'direita']:
            dir_path = os.path.join(paredes_path, direcao)
            if os.path.exists(dir_path):
                for tile_file in os.listdir(dir_path):
                    if tile_file.endswith('.png'):
                        tile_path = os.path.join(dir_path, tile_file)
                        tile_img = pygame.image.load(tile_path).convert_alpha()
                        # Redimensiona o tile para 16x16
                        tile_img = pygame.transform.scale(tile_img, (self.tile_size, self.tile_size))
                        self.tiles['paredes'][direcao].append(tile_img)
    
    def get_tile_chao(self, tipo='centro'):
        """Retorna um tile de chão do tipo especificado (centro ou borda)"""
        if tipo == 'centro' and self.tiles['chao']['centro']:
            return random.choice(self.tiles['chao']['centro'])
        elif tipo == 'borda' and self.tiles['chao']['borda']:
            return random.choice(self.tiles['chao']['borda'])
        # Fallback para o tipo disponível se o solicitado não existir
        return random.choice(self.tiles['chao']['centro'] or self.tiles['chao']['borda'])
    
    def get_tile_parede(self, direcao):
        """Retorna um tile de parede para a direção especificada"""
        if direcao in self.tiles['paredes'] and self.tiles['paredes'][direcao]:
            return random.choice(self.tiles['paredes'][direcao])
        return None