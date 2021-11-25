import pygame
from pygame.constants import *

import consts
from background_grid import BackgroundGrid
from resources import core

if __name__ == '__main__':
    pygame.font.init()
    pygame.display.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((consts.DISPLAY_WIDTH, consts.DISPLAY_HEIGHT), consts.DISPLAY_FLAGS)

    BackgroundGrid()

    running = True
    while running:
        clock.tick(consts.FPS_MAX)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                break
        core.all_sprites.draw(screen)
        core.all_sprites.update()
        pygame.display.update()

    pygame.quit()
