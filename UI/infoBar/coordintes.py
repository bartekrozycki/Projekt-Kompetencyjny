import pygame
from pygame.event import Event

from context import core, context


class Coordinates:
    surface = None

    def __init__(self, screen: pygame.Surface):
        self.font_consolas = pygame.font.SysFont('Consolas', 14)
        self.screen = screen
        test_render = self.font_consolas.render(
            '{}x: -1234 y: -1234 '.format(' ' if context.info_bar_width == 0 else ''), False, (255, 255, 255))

        self.size = (test_render.get_width(), test_render.get_height())

        self.surface = pygame.Surface(self.size)

        core.event_handlers.append(self)
        core.renderables.append(self)
        self.offset = context.info_bar_width
        context.info_bar_width = context.info_bar_width + self.size[0]

        self.render()

    def render(self):
        self.mouse_motion()
        return self.size

    def handle_event(self, event: Event):
        options = {
            pygame.MOUSEMOTION: self.mouse_motion,
        }

        try:
            options[event.type](event)
        except KeyError:
            pass
        except Exception as e:
            print(type(e), e)

    def mouse_motion(self, event: Event = None):
        text_render = self.font_consolas.render(' x: {:.0f} y: {:.0f} '.format(
            context.grid_position[0],
            context.grid_position[1]
        ), False, (255, 255, 255))

        self.surface.fill((0, 0, 0))
        self.surface.blit(text_render, (0, 0, self.size[0], self.size[1]))
        self.screen.blit(self.surface,
                         (self.offset, self.screen.get_height() - self.size[1], self.size[0], self.size[1])
                         )

        core.dirty_rectangles.append(
            (self.offset, self.screen.get_height() - self.size[1], self.size[0], self.size[1])
        )
