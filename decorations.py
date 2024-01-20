import pygame
import random
from settings import *
from support import *
from tiles import AnimatedTile, StaticTile


class Sky:
    def __init__(self, horizon):
        self.top_sky = pygame.image.load('graphics/decoration/sky/sky_top.png').convert_alpha()
        self.mid_sky = pygame.image.load('graphics/decoration/sky/sky_middle.png').convert_alpha()
        self.bottom_sky = pygame.image.load('graphics/decoration/sky/sky_bottom.png').convert_alpha()

        self.horizon = horizon

        self.top_sky = pygame.transform.scale(self.top_sky, (screen_width, tile_size))
        self.mid_sky = pygame.transform.scale(self.mid_sky, (screen_width, tile_size))
        self.bottom_sky = pygame.transform.scale(self.bottom_sky, (screen_width, tile_size))

    def draw(self, surface):
        for row in range(vertical_tile_number):
            y = row * tile_size
            if row < self.horizon:
                surface.blit(self.top_sky, (0, y))
            elif row == self.horizon:
                surface.blit(self.mid_sky, (0, y))
            else:
                surface.blit(self.bottom_sky, (0, y))


class Water:
    def __init__(self, height, level_width):
        water_start = -screen_width
        water_width = 192
        tile_amount = int((level_width + screen_width) / water_width)
        self.water_sprites = pygame.sprite.Group()

        for tile in range(tile_amount):
            sprite = AnimatedTile(water_width, (tile * water_width + water_start, height), 'graphics/decoration/water')
            self.water_sprites.add(sprite)

    def draw(self, surface, delta):
        self.water_sprites.update(delta)
        self.water_sprites.draw(surface)


class Clouds:
    def __init__(self, horizon, level_width, cloud_amount):
        cloud_layouts = import_folder('graphics/decoration/clouds')
        min_x = -screen_width
        max_x = level_width + screen_width
        min_y = 0
        max_y = horizon
        self.clouds_sprites = pygame.sprite.Group()

        for cloud in range(cloud_amount):
            sprite = StaticTile(0, (random.randint(min_x, max_x), random.randint(min_y, max_y)), random.choice(cloud_layouts))
            self.clouds_sprites.add(sprite)

    def draw(self, surface, delta):
        self.clouds_sprites.update(delta)
        self.clouds_sprites.draw(surface)