import pygame
from pygame.event import Event

import settings
from resources import core, context, event_handler, renderable_every_frame, renderable


class FPSCounter:
    surface = None
    offset = 0

    @renderable_every_frame
    @renderable
    def __init__(self):
        self.font_consolas = pygame.font.SysFont('Consolas', 14)

        test_render = self.font_consolas.render(
            '{}fps: {} '.format(' ' if context.info_bar_width == 0 else '', settings.max_fps), False, (255, 255, 255))

        self.size = (test_render.get_width(), test_render.get_height())

        self.surface = pygame.Surface(self.size)

        self.offset = context.info_bar_width
        context.info_bar_width = context.info_bar_width + self.size[0]

        self.render()

    def render(self):
        text_render = self.font_consolas.render(' fps: {:.0f} '.format(
            core.clock.get_fps(),
        ), False, (255, 255, 255))

        self.surface.fill((0, 0, 0))
        self.surface.blit(text_render, (0, 0, self.size[0], self.size[1]))
        core.screen.blit(self.surface,
                         (self.offset, core.screen.get_height() - self.size[1], self.size[0], self.size[1]))

        core.dirty_rectangles.append(
            (self.offset, core.screen.get_height() - self.size[1], self.size[0], self.size[1]))
