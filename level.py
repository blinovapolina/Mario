import pygame
from tiles import Tile
from settings import *
from player import Player


class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.setup_level(level_data)

        self.world_delta = 0

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for index_row, row in enumerate(layout):
            for index_col, cell in enumerate(row):
                if cell == 'X':
                    tile = Tile((index_col * tile_size, index_row * tile_size), tile_size)
                    self.tiles.add(tile)
                if cell == 'P':
                    player = Player((index_col * tile_size, index_row * tile_size))
                    self.player.add(player)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x == -1:
            self.world_delta = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x == 1:
            self.world_delta = -8
            player.speed = 0
        else:
            self.world_delta = 0
            player.speed = 8

    def run(self):
        self.tiles.update(self.world_delta)
        self.tiles.draw(self.display_surface)

        self.player.update()
        self.player.draw(self.display_surface)
        self.scroll_x()
