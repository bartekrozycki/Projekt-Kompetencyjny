import math

import pygame

import settings
from const import color
from resources import context


class Line(pygame.sprite.Sprite):
    start: tuple[int, int]
    end: tuple[int, int]

    def __init__(self, start: tuple[int, int], end: tuple[int, int]):
        super().__init__()

        self.start = start
        self.end = end

        ax, ay = start
        bx, by = end

        delta_x = bx - ax
        delta_y = by - ay
        theta_radians = math.atan2(delta_y, delta_x)

        width = abs(delta_x)
        height = abs(delta_y)

        if math.pi * 3/4 > theta_radians > math.pi * 1/4 or -math.pi * 3/4 < theta_radians < -math.pi * 1/4:
            self.rect = pygame.Rect((0, 0), (context.grid_density, (height + 1) * context.grid_density))
            self.rect.centerx = ax * context.grid_density
            self.rect.centery = -ay * context.grid_density - delta_y * context.grid_density // 2
        else:
            self.rect = pygame.Rect((0, 0), ((width + 1) * context.grid_density, context.grid_density))
            self.rect.centerx = ax * context.grid_density + delta_x * context.grid_density // 2
            self.rect.centery = -ay * context.grid_density

        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)
        self.image.fill(color.BLACK)
