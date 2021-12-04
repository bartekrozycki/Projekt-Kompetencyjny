import math

import pygame

import settings


class Line(pygame.sprite.Sprite):
    start: tuple[int, int]
    end: tuple[int, int]

    def __init__(self, start: tuple[int, int], end: tuple[int, int]):
        super().__init__()
        self.start = start
        self.end = end

        ax, ay = start
        bx, by = end

        self.length = math.sqrt((bx - ax) ** 2 + (by - ay) ** 2)
        size = (abs(bx - ax), abs(by - ay))
        self.image = pygame.Surface(size, pygame.SRCALPHA, 32)

        left = min(ax, bx)
        top = min(ay, by)

        self.rect = pygame.Rect((left, top), size)

        y_where_x_is_smaller = ay if ax < bx else by
        y_where_x_is_bigger = ay if y_where_x_is_smaller == by else by

        if y_where_x_is_smaller > y_where_x_is_bigger:
            pygame.draw.line(self.image, settings.COLOR_BLACK, (0, self.rect.h), (self.rect.w, 0))
        else:
            pygame.draw.line(self.image, settings.COLOR_BLACK, (0, 0), (self.rect.w, self.rect.h))
