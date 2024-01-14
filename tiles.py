import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, position, size):
        super(Tile, self).__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill('green')
        self.rect = self.image.get_rect(topleft=position)

    def update(self, x_delta):
        self.rect.x += x_delta
