import pygame
from pygame.event import Event
from pygame.time import Clock

from resources import config
from resources.context import core, context, event_handler, renderable_every_frame


class FPSCounter:
    surface = None
    offset = 0

    @event_handler
    @renderable_every_frame
    def __init__(self, screen: pygame.Surface, clock: Clock):
        self.font_consolas = pygame.font.SysFont('Consolas', 14)
        self.screen = screen
        self.clock = clock

        test_render = self.font_consolas.render(
            '{}fps: {} '.format(' ' if context.info_bar_width == 0 else '', config.max_fps), False, (255, 255, 255))

        self.size = (test_render.get_width(), test_render.get_height())

        self.surface = pygame.Surface(self.size)

        self.offset = context.info_bar_width
        context.info_bar_width = context.info_bar_width + self.size[0]

        self.render()

    def render(self):
        text_render = self.font_consolas.render(' fps: {:.0f} '.format(
            self.clock.get_fps(),
        ), False, (255, 255, 255))

        self.surface.fill((0, 0, 0))
        self.surface.blit(text_render, (0, 0, self.size[0], self.size[1]))
        self.screen.blit(self.surface,
                         (self.offset, self.screen.get_height() - self.size[1], self.size[0], self.size[1]))

        core.dirty_rectangles.append(
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
