import pygame
from support import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, size, position):
        super(Tile, self).__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=position)

    def update(self, x_delta):
        self.rect.x += x_delta


class StaticTile(Tile):
    def __init__(self, size, position, surface):
        super(StaticTile, self).__init__(size, position)
        self.image = surface


class Crate(StaticTile):
    def __init__(self, size, position):
        super().__init__(size, position, pygame.image.load('graphics/terrain/crate.png').convert_alpha())
        x = position[0]
        y = position[1]
        self.rect = self.image.get_rect(bottomleft=(x, y + size))


class AnimatedTile(Tile):
    def __init__(self, size, position, path):
        super().__init__(size, position)
        self.layouts = import_folder(path)
        self.layout_index = 0
        self.image = self.layouts[self.layout_index]

    def animate(self):
        self.layout_index += 0.1
        if self.layout_index >= len(self.layouts):
            self.layout_index = 0
        self.image = self.layouts[int(self.layout_index)]

    def update(self, x_delta):
        self.animate()
        self.rect.x += x_delta


class Coin(AnimatedTile):
    def __init__(self, size, position, path):
        super().__init__(size, position, path)
        x = position[0]
        y = position[1]
        self.rect = self.image.get_rect(center=(x + int(size / 2), y + int(size / 2)))


class Palm(AnimatedTile):
    def __init__(self, size, position, path, add_y):
        super().__init__(size, position, path)
        x = position[0]
        y = position[1]
        self.rect = self.image.get_rect(topleft=(x, y - add_y))