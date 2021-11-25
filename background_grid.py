import pygame.sprite

import consts
from consts import LAYER_BACKGROUND
from resources import core


class BackgroundGrid(pygame.sprite.Sprite):
    _layer = LAYER_BACKGROUND
    _position = consts.MAP_DEFAULT_POS

    grid_density = consts.START_GRID_DENSITY

    def __init__(self):
        super().__init__(core.all_sprites)
        self.update_background()

    def update_background(self):
        x, y = pygame.display.get_window_size()
        self.image = pygame.Surface((x, y))
        self.rect = self.image.get_rect()
        dx, dy = (self._position[0] % self.grid_density, self._position[1] % self.grid_density)

        x += self.grid_density
        y += self.grid_density

        dots_x = int(x // self.grid_density) + 2
        dots_y = int(y // self.grid_density) + 2
        dots_size = 2 if self.grid_density > 20 else 1

        self.image.fill(consts.COLOR_SKY_BLUE)
        for x in range(dots_x):
            for y in range(dots_y):
                pygame.draw.rect(self.image, consts.COLOR_BLACK,
                                 (x * self.grid_density + dx, y * self.grid_density + dy, dots_size, dots_size), 1)

    def update(self):
        self.handle_mouse_events()
        x, y = self._position
        text_render = pygame.font.SysFont('Consolas', 14).render(' x: {:.0f} y: {:.0f} '.format(x, y), False,
                                                                 (255, 255, 255))
        size = (text_render.get_width(), text_render.get_height())
        self.image.blit(text_render, (0, 0, size[0], size[1]))

    def handle_mouse_events(self):
        mouse_pos = pygame.mouse.get_pos()
        zoom_factor = 1.125
        print(pygame.event.get())
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                self.update_background()
            if event.type == pygame.MOUSEBUTTONDOWN:
                left, middle, right = pygame.mouse.get_pressed()
                if left:
                    if self.grid_density > consts.MAX_GRID_DENSITY:
                        continue
                    self.grid_density *= zoom_factor

                    x, y = self._position
                    dx = int(mouse_pos[0] - x) * (zoom_factor - 1)
                    dy = int(mouse_pos[1] - y) * (zoom_factor - 1)

                    self._position = [x - dx, y - dy]
                    self.update_background()
                if right:
                    if self.grid_density < consts.MIN_GRID_DENSITY:
                        continue

                    self.grid_density /= zoom_factor

                    x = self._position[0]
                    y = self._position[1]

                    dx = int(mouse_pos[0] - x) * (1 / zoom_factor - 1)
                    dy = int(mouse_pos[1] - y) * (1 / zoom_factor - 1)

                    self._position = [x - dx, y - dy]
                    self.update_background()
