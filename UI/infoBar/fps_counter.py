import pygame
from pygame.event import Event

import config


class FPSCounter:
    surface = None
    offset = 0

    def __init__(self, parent, screen: pygame.Surface):
        self.font_consolas = pygame.font.SysFont('Consolas', 14)
        self.parent = parent
        self.screen = screen
        test_render = self.font_consolas.render(
            '{}fps: {} '.format(' ' if self.parent.info_bar_width == 0 else '', config.max_fps), False, (255, 255, 255))

        self.size = (test_render.get_width(), test_render.get_height())

        self.surface = pygame.Surface(self.size)

        self.parent.event_handlers.append(self)
        self.parent.every_frame_render.append(self)
        self.offset = self.parent.info_bar_width
        self.parent.set_info_bar_width(self.parent.info_bar_width + self.size[0])

        self.render()

    def render(self):
        text_render = self.font_consolas.render(' fps: {:.0f} '.format(
            self.parent.clock.get_fps(),
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
        }

        try:
            options[event.type](event)
        except KeyError:
            pass
        except Exception as e:
            print(type(e), e)
