import pygame
from tiles import Tile
from settings import *


class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.setup_level(level_data)

        self.world_delta = 0

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        for index_row, row in enumerate(layout):
            for index_col, cell in enumerate(row):
                if cell == 'X':
                    tile = Tile((index_col * tile_size, index_row * tile_size), tile_size)
                    self.tiles.add(tile)

    def run(self):
        self.tiles.update(self.world_delta)
        self.tiles.draw(self.display_surface)
