import pygame
from pygame.event import Event

import config


class Zoom:
    surface = None
    offset = 0

    def __init__(self, parent, screen: pygame.Surface):
        self.font_consolas = pygame.font.SysFont('Consolas', 14)
        self.parent = parent
        self.screen = screen
        test_render = self.font_consolas.render(
            '{}zoom: {:.02f}  '.format(' ' if self.parent.info_bar_width == 0 else '',
                                       config.max_grid_density / config.start_grid_density), False, (255, 255, 255))

        self.size = (test_render.get_width(), test_render.get_height())

        self.surface = pygame.Surface(self.size)

        self.parent.event_handlers.append(self)
        self.parent.renderables.append(self)
        self.offset = self.parent.info_bar_width
        self.parent.set_info_bar_width(self.parent.info_bar_width + self.size[0])

        self.render()

    def render(self):
        text_render = self.font_consolas.render(' zoom: {:.2f} '.format(
            self.parent.zoom,
        ), False, (255, 255, 255))

        self.surface.fill((0, 0, 0))
        self.surface.blit(text_render, (0, 0, self.size[0], self.size[1]))
        self.screen.blit(self.surface,
                         (self.offset, self.screen.get_height() - self.size[1], self.size[0], self.size[1]))
        self.parent.dirty_rectangles.append(
            (self.offset, self.screen.get_height() - self.size[1], self.size[0], self.size[1]))

        return self.size

    def set_offset(self, offset):
        self.offset = offset

    def handle_event(self, event: Event):
        options = {
            pygame.MOUSEBUTTONDOWN: self.mouse_button_down,
        }

        try:
            options[event.type](event)
        except KeyError:
            pass
        except Exception as e:
            print(type(e), e)

    def mouse_button_down(self, event: Event):
        # zoom in
        def button_wheel_up():
            self.render()

        # zoom out
        def button_wheel_down():
            self.render()

        options = {
            pygame.BUTTON_WHEELUP: button_wheel_up,
            pygame.BUTTON_WHEELDOWN: button_wheel_down,
        }
        options[event.button]()