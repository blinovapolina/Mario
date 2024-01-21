import pygame
from level_data import levels
from support import *


class Level_Platform(pygame.sprite.Sprite):
    def __init__(self, pos, status, icon_speed, path):
        super().__init__()
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        if status == 'available':
            self.status = 'available'
        else:
            self.status = 'locked'
        self.rect = self.image.get_rect(center=pos)

        self.detection_zone = pygame.Rect(self.rect.centerx - (icon_speed / 2), self.rect.centery - (icon_speed / 2),
                                          icon_speed, icon_speed)

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()


class Icon(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.position = position
        self.image = pygame.image.load('graphics/overworld/hat.png').convert_alpha()
        self.rect = self.image.get_rect(center=position)

    def update(self):
        self.rect.center = self.position


class Menu:
    def __init__(self, start_level, max_level, surface, create_level):
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level
        self.top_sky = pygame.image.load('graphics/decoration/sky/sky_top.png').convert_alpha()
        self.top_sky = pygame.transform.scale(self.top_sky, (screen_width, screen_height))
        self.create_level = create_level

        self.moving = False
        self.move_direction = pygame.math.Vector2(0, 0)
        self.speed = 6

        self.setup_nodes()
        self.setup_icon()

    def setup_nodes(self):
        self.platform_levels = pygame.sprite.Group()
        for index, data in enumerate(levels.values()):
            if index <= self.max_level:
                platform_sprite = Level_Platform(data['platform_pos'], 'available', self.speed, data['platform_graphics'])
            else:
                platform_sprite = Level_Platform(data['platform_pos'], 'locked', self.speed, data['platform_graphics'])
            self.platform_levels.add(platform_sprite)

    def draw_paths(self):
        points = [data['platform_pos'] for index, data in enumerate(levels.values()) if index <= self.max_level]
        pygame.draw.lines(self.display_surface, '#a04f45', False, points, 6)

    def draw(self, surface):
        surface.blit(self.top_sky, (0, 0))

    def setup_icon(self):
        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.platform_levels.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.moving:
            if keys[pygame.K_LEFT] and self.current_level > 0:
                self.move_direction = self.get_movement_data('previous')
                self.current_level -= 1
                self.moving = True
            elif keys[pygame.K_RIGHT] and self.current_level < self.max_level:
                self.move_direction = self.get_movement_data('next')
                self.current_level += 1
                self.moving = True
            elif keys[pygame.K_SPACE]:
                self.create_level(self.current_level)

    def get_movement_data(self, word):
        start = pygame.math.Vector2(self.platform_levels.sprites()[self.current_level].rect.center)
        if word == 'next':
            end = pygame.math.Vector2(self.platform_levels.sprites()[self.current_level + 1].rect.center)
        else:
            end = pygame.math.Vector2(self.platform_levels.sprites()[self.current_level - 1].rect.center)
        return end - start

    def update_icon_pos(self):
        if self.moving and self.move_direction:
            self.icon.sprite.position += self.move_direction * self.speed
            target_platform = self.platform_levels.sprites()[self.current_level]
            if target_platform.detection_zone.collidepoint(self.icon.sprite.position):
                self.moving = False
                self.move_direction = pygame.math.Vector2(0, 0)

    def run(self):
        self.draw(self.display_surface)
        self.input()
        self.update_icon_pos()
        self.icon.update()
        self.draw_paths()
        self.platform_levels.draw(self.display_surface)
        self.icon.draw(self.display_surface)
