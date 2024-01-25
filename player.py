import pygame
from support import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface, create_jump_particles, change_health):
        super(Player, self).__init__()
        self.import_assets()
        self.frame_index = 0
        self.animation_speed = 0.1
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface
        self.create_jump_particles = create_jump_particles

        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16
        self.collision_rectangle = pygame.Rect(self.rect.topleft, (50, self.rect.height))

        self.status = 'idle'
        self.face_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        self.change_health = change_health
        self.damaged = False
        self.duration_damage = 500
        self.hurt_time = 0

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

    def import_dust_run_particles(self):
        self.dust_run_particles = import_folder('graphics/character/dust_particles/run')

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.face_right:
            self.image = image
            self.rect.bottomleft = self.collision_rectangle.bottomleft
        else:
            self.image = pygame.transform.flip(image, True, False)
            self.rect.bottomright = self.collision_rectangle.bottomright

        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def run_dust_animation(self):
        if self.status == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0

            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

            if self.face_right:
                pos = self.rect.bottomleft - pygame.math.Vector2(6, 10)
                self.display_surface.blit(dust_particle, pos)
            else:
                pos = self.rect.bottomright - pygame.math.Vector2(6, 10)
                flipped_dust_particle = pygame.transform.flip(dust_particle, True, False)
                self.display_surface.blit(flipped_dust_particle, pos)

    def get_input(self):
        buttons = pygame.key.get_pressed()

        if buttons[pygame.K_RIGHT]:
            self.direction.x = 1
            self.face_right = True
        elif buttons[pygame.K_LEFT]:
            self.direction.x = -1
            self.face_right = False
        else:
            self.direction.x = 0

        if buttons[pygame.K_SPACE] and self.on_ground:
            self.jump()
            self.create_jump_particles(self.rect.midbottom)

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
        self.collision_rectangle.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def get_damage(self):
        if not self.damaged:
            self.change_health(-10)
            self.damaged = True
            self.hurt_time = pygame.time.get_ticks()

    def not_damaged_timer(self):
        if self.damaged:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.duration_damage:
                self.damaged = False

    def update(self):
        self.get_input()
        self.get_status_info()
        self.animate()
        self.run_dust_animation()
        self.not_damaged_timer()

