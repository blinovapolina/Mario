import pygame
from support import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Player, self).__init__()
        self.import_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16

        self.status = 'idle'

    def import_assets(self):
        chatacter_path = 'graphics/character/'
        self.animations = {
            'idle': [],
            'run': [],
            'jump': [],
            'fall': []
        }

        for animation in self.animations.keys():
            full_path = chatacter_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]

    def get_input(self):
        buttons = pygame.key.get_pressed()

        if buttons[pygame.K_RIGHT]:
            self.direction.x = 1
        elif buttons[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if buttons[pygame.K_SPACE]:
            self.jump()

    def get_status_info(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def add_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def update(self):
        self.get_input()
        self.get_status_info()
        self.animate()
