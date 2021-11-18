import pygame
from pygame.constants import *

import settings
from resources import core

if __name__ == '__main__':
    pygame.font.init()
    pygame.display.init()

    core.clock = pygame.time.Clock()
    core.screen = pygame.display.set_mode((settings.display_width, settings.display_height), settings.display_flags)


    def render():
        for element in core.every_frame_render:
            element.render()
        if core.render_all:
            for renderable in core.renderables:
                renderable.render()
            pygame.display.update()
            core.render_all = False
        else:
            pygame.display.update(core.dirty_rectangles)
            core.dirty_rectangles.clear()


    running = True
    while running:
        core.clock.tick(settings.max_fps)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                break
            elif event.type == VIDEORESIZE:
                core.render_all = True
            for event_handler in core.event_handlers:
                event_handler.handle_event(event)
        render()
    pygame.quit()
