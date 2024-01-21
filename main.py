import pygame
import sys
from level import Level
from menu import *
from info_graphics import *


class Game:
    def __init__(self, screen):
        self.screen = screen

        self.max_level = 2
        self.max_health = 100
        self.current_health = 100
        self.coins = 0

        self.menu = Menu(0, self.max_level, screen, self.create_level)
        self.status = 'menu'

        self.info = Info_graphics(screen)

    def create_level(self, current_level):
        self.level = Level(current_level, self.screen, self.create_menu, self.change_coins)
        self.status = 'level'

    def create_menu(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.menu = Menu(current_level, self.max_level, self.screen, self.create_level)
        self.status = 'menu'

    def change_coins(self, amount):
        self.coins += amount

    def run(self):
        if self.status == 'menu':
            self.menu.run()
        else:
            self.level.run()
            self.info.show_health(self.current_health, self.max_health)
            self.info.show_coins(self.coins)


def main():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    game = Game(screen)
    pygame.display.set_caption('Игра «Пират»')

    running = True
    fps = 60

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill('grey')
        game.run()

        pygame.display.update()
        pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    main()
