import pygame
from pygame.constants import *

import config
from UI.grid import Grid
from UI.infoBar.coordintes import Coordinates
from UI.infoBar.fps_counter import FPSCounter
from UI.infoBar.zoom import Zoom
from UI.drawingPanel.button_draw import DrawRoadButton
from UI.draw_single_road import DrawSingleRoad


class App:
    pygame.font.init()
    pygame.display.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((config.display_width, config.display_height), config.display_flags)

    user_position = config.map_default_pos
    grid_density = config.start_grid_density

    every_frame_render = []

    event_handlers = []
    renderables = []

    dirty_rectangles = []

    zoom = 1
    grid_position = [0, 0]
    prev_mouse_pos = None

    moving = False
    running = True
    render_all = False

    drawing = False

    info_bar_width = 0

    def set_info_bar_width(self, width):
        self.info_bar_width = width

    def __init__(self):
        self.grid = Grid(self, self.screen)
        FPSCounter(self, self.screen)
        Zoom(self, self.screen)
        Coordinates(self, self.screen)

        DrawSingleRoad(self, self.screen)

        DrawRoadButton(self, self.screen)

        self.video_resize(None)

    def render(self):
        if self.render_all:
            for renderable in self.renderables:
                renderable.render()
            pygame.display.update()
            self.render_all = False
        else:
            pygame.display.update(self.dirty_rectangles)
            self.dirty_rectangles.clear()

    def run(self):
        while self.running:
            self.clock.tick(config.max_fps)
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    break

                self.handle_event(event)
                for event_handler in self.event_handlers:
                    event_handler.handle_event(event)
            for element in self.every_frame_render:
                element.render()
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
        self.render_all = True

    def mouse_motion(self, event):
        if not self.moving:
            cursor_position = pygame.mouse.get_pos()
            prev_grid_position = self.grid_position
            self.grid_position = [
                (cursor_position[0] - self.grid_density // 2 - self.user_position[0]) // self.grid_density,
                -(cursor_position[1] - self.grid_density // 2 - self.user_position[1]) // self.grid_density]


if __name__ == '__main__':
    App().run()
