import pygame
from tiles import *
from settings import *
from player import Player
from enemy import Enemy
from particles import ParticleEffect
from decorations import *
from support import *
from level_data import *


class Level:
    def __init__(self, current_level, surface, create_menu, change_coins):
        self.display_surface = surface
        self.change_coins = change_coins
        self.world_delta = 0
        self.current_x = 0

        self.current_level = current_level
        level_data = levels[current_level]
        self.new_max_level = level_data['max_level']
        self.create_menu = create_menu

        player_layout = import_csv(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal_player = pygame.sprite.GroupSingle()
        self.setup_player(player_layout)

        terrain_layout = import_csv(level_data['terrain'])
        self.terrain_sprites = self.create_group(terrain_layout, 'terrain')

        crates_layout = import_csv(level_data['crate'])
        self.crates_sprites = self.create_group(crates_layout, 'crate')

        grass_layout = import_csv(level_data['grass'])
        self.grass_sprites = self.create_group(grass_layout, 'grass')

        coins_layout = import_csv(level_data['coins'])
        self.coins_sprites = self.create_group(coins_layout, 'coins')

        palms_layout = import_csv(level_data['palms'])
        self.palms_sprites = self.create_group(palms_layout, 'palms')

        bg_palms_layout = import_csv(level_data['bg_palms'])
        self.bg_palms_sprites = self.create_group(bg_palms_layout, 'bg_palms')

        enemy_layout = import_csv(level_data['enemies'])
        self.enemies_sprites = self.create_group(enemy_layout, 'enemies')

        special_layout = import_csv(level_data['special'])
        self.special_sprites = self.create_group(special_layout, 'special_layout')

        self.sky = Sky(8)
        self.water = Water(screen_height - 20, len(terrain_layout[0]) * tile_size)
        self.clouds = Clouds(380, len(terrain_layout[0]) * tile_size, 30)

        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

    def create_group(self, layout, tile_type):
        group = pygame.sprite.Group()

        for index_row, row in enumerate(layout):
            for index_col, cell in enumerate(row):
                if cell != '-1':
                    x = index_col * tile_size
                    y = index_row * tile_size
                    sprite = ''

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
                            sprite = Coin(tile_size, (x, y), 'graphics/coins/gold', 3)
                        elif cell == '1':
                            sprite = Coin(tile_size, (x, y), 'graphics/coins/silver', 1)
                    if tile_type == 'palms':
                        if cell == '0':
                            sprite = Palm(tile_size, (x, y), 'graphics/terrain/palm_small', 39)
                        elif cell == '1':
                            sprite = Palm(tile_size, (x, y), 'graphics/terrain/palm_large', 65)
                    if tile_type == 'bg_palms':
                        sprite = Palm(tile_size, (x, y), 'graphics/terrain/palm_bg', 65)

                    if tile_type == 'enemies':
                        sprite = Enemy(tile_size, (x, y))

                    if tile_type == 'special_layout':
                        sprite = Tile(tile_size, (x, y))

                    group.add(sprite)
        return group

    def setup_player(self, layout):
        for index_row, row in enumerate(layout):
            for index_col, cell in enumerate(row):
                x = index_col * tile_size
                y = index_row * tile_size
                if cell == '0':
                    sprite = Player((x, y), self.display_surface, self.create_jump_particles)
                    self.player.add(sprite)
                if cell == '1':
                    hat_surface = pygame.image.load('graphics/character/hat.png').convert_alpha()
                    sprite = StaticTile(tile_size, (x, y), hat_surface)
                    self.goal_player.add(sprite)

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

        for tile in self.terrain_sprites.sprites() + self.crates_sprites.sprites() + self.palms_sprites.sprites():
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

        for tile in self.terrain_sprites.sprites() + self.crates_sprites.sprites() + self.palms_sprites.sprites():
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

    def enemy_reverse_speed(self):
        for enemy in self.enemies_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.special_sprites, False):
                enemy.change_speed()

    def input_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.create_menu(self.current_level, self.new_max_level)
        if keys[pygame.K_ESCAPE]:
            self.create_menu(self.current_level, 0)

    def check_death(self):
        if self.player.sprite.rect.top > screen_height:
            self.create_menu(self.current_level, 0)

    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal_player, False):
            self.create_menu(self.current_level, self.new_max_level)

    def check_coin_collisions(self):
        coins_collided = pygame.sprite.spritecollide(self.player.sprite, self.coins_sprites, True)
        if coins_collided:
            for coin in coins_collided:
                self.change_coins(coin.value)

    def check_enemy_collisions(self):
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite, self.enemies_sprites, False)
        if enemy_collisions:
            for enemy in enemy_collisions:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                    self.player.sprite.direction.y = -15
                    enemy.kill()
                else:
                    self.player.sprite.get_damage()

    def run(self):
        self.scroll_x()

        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface, self.world_delta)

        self.dust_sprite.update(self.world_delta)
        self.dust_sprite.draw(self.display_surface)

        self.bg_palms_sprites.update(self.world_delta)
        self.bg_palms_sprites.draw(self.display_surface)

        self.terrain_sprites.update(self.world_delta)
        self.terrain_sprites.draw(self.display_surface)

        self.special_sprites.update(self.world_delta)
        self.enemies_sprites.update(self.world_delta)
        self.enemy_reverse_speed()
        self.enemies_sprites.draw(self.display_surface)

        self.grass_sprites.update(self.world_delta)
        self.grass_sprites.draw(self.display_surface)

        self.crates_sprites.update(self.world_delta)
        self.crates_sprites.draw(self.display_surface)

        self.coins_sprites.update(self.world_delta)
        self.coins_sprites.draw(self.display_surface)

        self.palms_sprites.update(self.world_delta)
        self.palms_sprites.draw(self.display_surface)

        self.goal_player.update(self.world_delta)
        self.goal_player.draw(self.display_surface)

        self.player.update()
        self.horizontal_move_collision()
        self.get_player_on_ground()
        self.vertical_move_collision()
        self.create_landing_dust()
        self.player.draw(self.display_surface)

        self.check_death()
        self.check_win()

        self.check_enemy_collisions()
        self.check_coin_collisions()

        self.water.draw(self.display_surface, self.world_delta)
