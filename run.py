import pygame
from pygame.constants import *

import config
from UI.draw_single_road import DrawSingleRoad
from UI.drawingPanel.button_draw import DrawRoadButton
from UI.grid import Grid
from UI.infoBar.coordintes import Coordinates
from UI.infoBar.fps_counter import FPSCounter
from UI.infoBar.zoom import Zoom
from context import context, core


class App:
    pygame.font.init()
    pygame.display.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((config.display_width, config.display_height), config.display_flags)

    running = True

    def set_info_bar_width(self, width):
        self.info_bar_width = width

    def __init__(self):
        Grid(self.screen)
        FPSCounter(self.screen, self.clock)
        Zoom(self.screen)
        Coordinates(self.screen)

        DrawSingleRoad(self, self.screen)

        DrawRoadButton(self.screen)

        self.video_resize(None)

    def render(self):
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

    def run(self):
        core.event_handlers.append(self)

        while self.running:
            self.clock.tick(config.max_fps)
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    break

                for event_handler in core.event_handlers:
                    event_handler.handle_event(event)
            self.render()
        pygame.quit()

    def handle_event(self, event):
        options = {
            VIDEORESIZE: self.video_resize,
            MOUSEMOTION: self.mouse_motion,
        }

        try:
            options[event.type](event)
        except Exception as e:
            pass

    def video_resize(self, event):
        core.render_all = True

    def mouse_motion(self, event):
        if not context.moving:
            cursor_position = pygame.mouse.get_pos()
            context.grid_position = [
                (cursor_position[0] - context.grid_density // 2 - context.user_position[0]) // context.grid_density,
                -(cursor_position[1] - context.grid_density // 2 - context.user_position[1]) // context.grid_density]


if __name__ == '__main__':
    App().run()
