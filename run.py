import pygame
from pygame.constants import *

import settings
from resources import core

from UI.draw_single_road import DrawSingleRoad
from UI.drawingPanel.button_draw import DrawRoadButton
from UI.grid import Grid
from UI.infoBar.coordintes import Coordinates
from UI.infoBar.fps_counter import FPSCounter
from UI.infoBar.zoom import Zoom

if __name__ == '__main__':
    pygame.font.init()
    pygame.display.init()

    core.clock = pygame.time.Clock()
    core.screen = pygame.display.set_mode((settings.display_width, settings.display_height), settings.display_flags)

    grid = Grid()
    # FPSCounter()
    # Zoom()
    Coordinates()
    #
    DrawSingleRoad()
    #
    # DrawRoadButton()


    def render():
        # for element in core.every_frame_render:
        #     element.render()

        if core.render_all:
            for renderable in core.renderables:
                renderable.render()
            # pygame.display.update()
            core.render_all = False
        # elif core.dirty_rectangles:
            # for rect in core.background_rectangles:
            #     grid.dirty_render(rect)
            #     # pygame.draw.rect(core.screen, (255, 0, 0), rect, 1)
            # core.background_rectangles.clear()

            # for road in core.roads_to_draw:
            #     core.dirty_rectangles.append(pygame.draw.line(core.screen, (0, 0, 0), road[0], road[1]))
            # core.roads_to_draw.clear()

            # core.road_group.clear(core.screen, core.background)
            # core.road_group.draw(core.screen)

            # pygame.display.update(core.dirty_rectangles)
            # core.dirty_rectangles.clear()

        # core.road_group.clear(core.screen, core.background)
        # core.road_group.draw(core.screen)
        pygame.display.update()


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
