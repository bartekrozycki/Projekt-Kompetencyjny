import math

import pygame

import settings
from const import color
from resources import context, core


class Line(pygame.sprite.Sprite):
    start: tuple[int, int]
    end: tuple[int, int]

    def __init__(self, start: tuple[int, int], end: tuple[int, int]):
        super().__init__()

        self.start = start
        self.end = end

        ax, ay = start
        bx, by = end

        self.delta_x = bx - ax
        self.delta_y = by - ay
        theta_radians = math.atan2(self.delta_y, self.delta_x)

        if math.pi * 3 / 4 > theta_radians > math.pi * 1 / 4 or -math.pi * 3 / 4 < theta_radians < -math.pi * 1 / 4:
            self.delta_x = 0
        else:
            self.delta_y = 0

        self.rect = pygame.Rect(0, 0, 0, 0)

        self.draw()
        self.render()

    def draw(self):
        ax, ay = self.start
        self.rect.size = (
            (abs(self.delta_x) + 1) * context.grid_density, (abs(self.delta_y) + 1) * context.grid_density)
        self.rect.centerx = ax * context.grid_density + self.delta_x * context.grid_density // 2 + core.foreground.rect.x
        self.rect.centery = -ay * context.grid_density - self.delta_y * context.grid_density // 2 + core.foreground.rect.y

    def render(self):
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)
        self.image.fill(color.BLACK)
