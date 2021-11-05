import pygame
from pygame.event import Event


class Coordinates:
    surface = None

    def __init__(self, parent, screen: pygame.Surface):
        self.font_consolas = pygame.font.SysFont('Consolas', 14)
        self.parent = parent
        self.screen = screen
        test_render = self.font_consolas.render(
            '{}x: -1234 y: -1234 '.format(' ' if self.parent.info_bar_width == 0 else ''), False, (255, 255, 255))

        self.size = (test_render.get_width(), test_render.get_height())

        self.surface = pygame.Surface(self.size)

        self.parent.event_handlers.append(self)
        self.parent.renderables.append(self)
        self.offset = self.parent.info_bar_width
        self.parent.set_info_bar_width(self.parent.info_bar_width + self.size[0])

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
            self.parent.grid_position[0],
            self.parent.grid_position[1]
        ), False, (255, 255, 255))

        self.surface.fill((0, 0, 0))
        self.surface.blit(text_render, (0, 0, self.size[0], self.size[1]))
        self.screen.blit(self.surface,
                         (self.offset, self.screen.get_height() - self.size[1], self.size[0], self.size[1]))
        self.parent.dirty_rectangles.append(
            (self.offset, self.screen.get_height() - self.size[1], self.size[0], self.size[1]))
