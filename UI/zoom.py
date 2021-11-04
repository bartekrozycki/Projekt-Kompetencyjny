import pygame
from pygame.event import Event

import config
from abstract_object import AbstractObject


class Zoom(AbstractObject):
    surface = None
    offset = 0

    def __init__(self):
        super().add_event_handler(pygame.MOUSEBUTTONDOWN, self.mouse_button_down)
        super().context.info_bar_width = 0
        super().context.zoom = 1

        self.font_consolas = pygame.font.SysFont('Consolas', 14)

        dummy_text = self.font_consolas.render(
            '{}zoom: {:.02f}  '.format(' ' if super().context.info_bar_width == 0 else '',
                                       config.max_grid_density / config.start_grid_density), False, (255, 255, 255))

        self.size = (dummy_text.get_width(), dummy_text.get_height())
        self.surface = pygame.Surface(self.size)

        super().context.add_event_handlers(self)

        super().context.info_bar_width += self.size[0]
        self.offset = super().context.info_bar_width

        self.render()

    def render(self):

        text_render = self.font_consolas.render(' zoom: {:.2f} '.format(
            super().context.zoom,
        ), False, (255, 255, 255))

        self.surface.fill((0, 0, 0))
        self.surface.blit(text_render, (0, 0, self.size[0], self.size[1]))

        super().context.screen.blit(self.surface,
                         (self.offset, super().context.screen.get_height() - self.size[1], self.size[0], self.size[1]))

        super().context.add_dirty_rectangle(
            (self.offset, super().context.screen.get_height() - self.size[1], self.size[0], self.size[1])
        )

        return self.size

    def mouse_button_down(self, event: Event):
        # zoom in
        def button_wheel_up():
            print("cipka up")
            self.context.zoom -= 1
            self.render()

        # zoom out
        def button_wheel_down():
            print("cipka down")
            self.context.zoom += 1
            self.render()

        options = {
            pygame.BUTTON_WHEELUP: button_wheel_up,
            pygame.BUTTON_WHEELDOWN: button_wheel_down,
        }
        options[event.button]()
