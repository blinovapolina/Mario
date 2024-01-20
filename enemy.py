import pygame
from tiles import AnimatedTile
import random


class Enemy(AnimatedTile):
    def __init__(self, size, position):
        super().__init__(size, position, 'graphics/enemy/run')
        x = position[0]
        y = position[1]
        self.rect = self.image.get_rect(midbottom=(x, y + size - self.image.get_rect()[1]))
        self.speed = random.randint(2, 4)

    def face_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def change_speed(self):
        self.speed *= -1

    def move(self):
        self.rect.x += self.speed

    def update(self, x_delta):
        self.rect.x += x_delta
        self.animate()
        self.face_image()
        self.move()
