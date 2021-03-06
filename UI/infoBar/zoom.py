import pygame
from pygame.event import Event

import settings
from resources import context, core, renderable, event_handler


class Zoom:
    surface = None
    offset = 0

    @renderable
    @event_handler
    def __init__(self):
        self.font_consolas = pygame.font.SysFont('Consolas', 14)

        test_render = self.font_consolas.render(
            '{}zoom: {:.02f}  '.format(' ' if context.info_bar_width == 0 else '',
                                       settings.GRID_MAX_DENSITY / settings.GRID_START_DENSITY), False, (255, 255, 255))

        self.size = (test_render.get_width(), test_render.get_height())

        self.surface = pygame.Surface(self.size)

        self.offset = context.info_bar_width
        context.info_bar_width = context.info_bar_width + self.size[0]

        self.render()

    def render(self):
        text_render = self.font_consolas.render(' zoom: {:.2f} '.format(
            context.zoom_sensitivity,
        ), False, (255, 255, 255))

        self.surface.fill((0, 0, 0))
        self.surface.blit(text_render, (0, 0, self.size[0], self.size[1]))
        core.screen.blit(self.surface, (
            self.offset, core.screen.get_height() - self.size[1], self.size[0], self.size[1]
        ))

        core.dirty_rectangles.append(
            (self.offset, core.screen.get_height() - self.size[1], self.size[0], self.size[1])
        )

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
        # zoom_sensitivity in
        def button_wheel_up():
            self.render()

        # zoom_sensitivity out
        def button_wheel_down():
            self.render()

        options = {
            pygame.BUTTON_WHEELUP: button_wheel_up,
            pygame.BUTTON_WHEELDOWN: button_wheel_down,
        }
        options[event.button]()
