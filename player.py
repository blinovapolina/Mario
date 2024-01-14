import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Player, self).__init__()
        self.image = pygame.Surface((32, 64))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft=pos)

        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16

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

    def add_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def update(self):
        self.get_input()
        self.rect.x += self.direction.x * self.speed
        self.add_gravity()
