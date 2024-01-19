from os import walk
import pygame
from csv import reader
from settings import *


def import_folder(path):
    surface_list = []

    for folder_name, folders_in, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)

    return surface_list


def import_csv(path):
    level_map_terrain = list()

    with open(path) as map:
        level = reader(map, delimiter=',')
        for row in level:
            level_map_terrain.append(list(row))

    return level_map_terrain


def import_cut_graphics(path):
    surface = pygame.image.load(path).convert_alpha()

    num_x = int(surface.get_size()[0] // tile_size)
    num_y = int(surface.get_size()[1] // tile_size)
    tiles = list()
    for row in range(num_y):
        for col in range(num_x):
            x = col * tile_size
            y = row * tile_size
            new_surface = pygame.Surface((tile_size, tile_size))
            new_surface.blit(surface, (0, 0), pygame.Rect(x, y, tile_size, tile_size))
            tiles.append(new_surface)

    return tiles