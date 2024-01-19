import pygame
from tiles import *
from settings import *
from player import Player
from particles import ParticleEffect
from support import *


class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        # self.setup_level(level_data)
        self.world_delta = -2
        self.current_x = 0

        terrain_layout = import_csv(level_data['terrain'])
        self.terrain_sprites = self.create_group(terrain_layout, 'terrain')

        grass_layout = import_csv(level_data['grass'])
        self.grass_sprites = self.create_group(grass_layout, 'grass')

        crates_layout = import_csv(level_data['crate'])
        self.crates_sprites = self.create_group(crates_layout, 'crate')

        coins_layout = import_csv(level_data['coins'])
        self.coins_sprites = self.create_group(coins_layout, 'coins')

        palms_layout = import_csv(level_data['palms'])
        self.palms_sprites = self.create_group(palms_layout, 'palms')

        bg_palms_layout = import_csv(level_data['bg_palms'])
        self.bg_palms_sprites = self.create_group(bg_palms_layout, 'bg_palms')

        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

    def create_group(self, layout, tile_type):
        group = pygame.sprite.Group()

        for index_row, row in enumerate(layout):
            for index_col, cell in enumerate(row):
                if cell != '-1':
                    x = index_col * tile_size
                    y = index_row * tile_size

                    if tile_type == 'terrain':
                        terrain_tile_list = import_cut_graphics('graphics/terrain/terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(cell)]
                        sprite = StaticTile(tile_size, (x, y), tile_surface)
                    if tile_type == 'grass':
                        grass_tile_list = import_cut_graphics('graphics/decoration/grass/grass.png')
                        tile_surface = grass_tile_list[int(cell)]
                        sprite = StaticTile(tile_size, (x, y), tile_surface)
                    if tile_type == 'crate':
                        sprite = Crate(tile_size, (x, y))

                    if tile_type == 'coins':
                        if cell == '0':
                            sprite = Coin(tile_size, (x, y), 'graphics/coins/gold')
                        elif cell == '1':
                            sprite = Coin(tile_size, (x, y), 'graphics/coins/silver')
                    if tile_type == 'palms':
                        if cell == '0':
                            sprite = Palm(tile_size, (x, y), 'graphics/terrain/palm_small', 39)
                        elif cell == '1':
                            sprite = Palm(tile_size, (x, y), 'graphics/terrain/palm_large', 65)
                    if tile_type == 'bg_palms':
                        sprite = Palm(tile_size, (x, y), 'graphics/terrain/palm_bg', 65)

                    group.add(sprite)
        return group

    def create_jump_particles(self, pos):
        if self.player.sprite.face_right:
            pos -= pygame.math.Vector2(10, 5)
        else:
            pos += pygame.math.Vector2(10, -5)
        jump_particle_sprite = ParticleEffect(pos, 'jump')
        self.dust_sprite.add(jump_particle_sprite)

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.face_right:
                offset = pygame.math.Vector2(10, 15)
            else:
                offset = pygame.math.Vector2(-10, 15)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(fall_dust_particle)

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for index_row, row in enumerate(layout):
            for index_col, cell in enumerate(row):
                if cell == 'X':
                    tile = Tile((index_col * tile_size, index_row * tile_size), tile_size)
                    self.tiles.add(tile)
                if cell == 'P':
                    player = Player((index_col * tile_size, index_row * tile_size), self.display_surface,
                                    self.create_jump_particles)
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

    def horizontal_move_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for tile in self.tiles.sprites():
            if tile.rect.colliderect(player.rect):
                if player.direction.x == 1:
                    player.rect.right = tile.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
                elif player.direction.x == -1:
                    player.rect.left = tile.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left

        if player.on_left and (player.on_left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        elif player.on_right and (player.on_right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical_move_collision(self):
        player = self.player.sprite
        player.add_gravity()

        for tile in self.tiles.sprites():
            if tile.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = tile.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = tile.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    def run(self):
        self.dust_sprite.update(self.world_delta)
        self.dust_sprite.draw(self.display_surface)

        self.bg_palms_sprites.update(self.world_delta)
        self.bg_palms_sprites.draw(self.display_surface)

        self.terrain_sprites.update(self.world_delta)
        self.terrain_sprites.draw(self.display_surface)

        self.grass_sprites.update(self.world_delta)
        self.grass_sprites.draw(self.display_surface)

        self.crates_sprites.update(self.world_delta)
        self.crates_sprites.draw(self.display_surface)

        self.coins_sprites.update(self.world_delta)
        self.coins_sprites.draw(self.display_surface)

        self.palms_sprites.update(self.world_delta)
        self.palms_sprites.draw(self.display_surface)

        #
        # self.tiles.update(self.world_delta)
        # self.tiles.draw(self.display_surface)
        # self.scroll_x()
        #
        # self.player.update()
        # self.horizontal_move_collision()
        # self.get_player_on_ground()
        # self.vertical_move_collision()
        # self.create_landing_dust()
        # self.player.draw(self.display_surface)
