import pygame
from pygame.event import Event

from resources import core, context, event_handler, renderable


class Coordinates:
    surface = None

    @event_handler
    @renderable
    def __init__(self):
        self.font_consolas = pygame.font.SysFont('Consolas', 14)
        test_render = self.font_consolas.render(
            '{}x: -1234 y: -1234 '.format(' ' if context.info_bar_width == 0 else ''), False, (255, 255, 255))

        self.size = (test_render.get_width(), test_render.get_height())

        self.surface = pygame.Surface(self.size)

        self.offset = context.info_bar_width
        context.info_bar_width += self.size[0]

        self.render()

    def render(self):
        text_render = self.font_consolas.render(' x: {:.0f} y: {:.0f} '.format(
            context.mouse_coordinates[0],
            context.mouse_coordinates[1]
        ), False, (255, 255, 255))

        self.surface.fill((0, 0, 0))
        self.surface.blit(text_render, (0, 0, self.size[0], self.size[1]))
        core.screen.blit(self.surface,
                         (self.offset, core.screen.get_height() - self.size[1], self.size[0], self.size[1])
                         )

        core.dirty_rectangles.append(
            (self.offset, core.screen.get_height() - self.size[1], self.size[0], self.size[1])
        )
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
        if not context.is_moving:
            cursor_position = pygame.mouse.get_pos()
            context.mouse_coordinates = [
                (cursor_position[0] + context.grid_density // 2 - context.user_position[0]) // context.grid_density,
                -(cursor_position[1] - context.grid_density // 2 - context.user_position[1]) // context.grid_density]
            self.render()
