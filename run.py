import pygame
from pygame.constants import QUIT

import config
from UI.grid import Grid
from UI.coordintes import Coordinates
from UI.fps_counter import FPSCounter
from UI.zoom import Zoom


class App:
    pygame.font.init()
    pygame.display.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((config.display_width, config.display_height), config.display_flags)

    user_position = config.map_default_pos
    grid_density = config.start_grid_density

    every_frame_render = []
    event_handlers = []
    dirty_rectangles = []

    zoom = 1
    grid_position = [0, 0]
    prev_mouse_pos = None

    moving = False
    running = True

    info_bar_width = 0

    def set_info_bar_width(self, width):
        self.info_bar_width = width

    def __init__(self):
        Grid(self, self.screen)
        Coordinates(self, self.screen)
        FPSCounter(self, self.screen)
        Zoom(self, self.screen)

        self.video_resize(None)

    def render(self, everything=False):
        # for event_handler in self.event_handlers:
        #     event_handler.render()
        # pygame.display.update()
        if everything:
            for event_handler in self.event_handlers:
                event_handler.render()
            pygame.display.update()
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
            pygame.VIDEORESIZE: self.video_resize,
            pygame.MOUSEMOTION: self.mouse_motion,
        }

        try:
            options[event.type](event)
        except:
            pass

    def video_resize(self, event):
        for event_handler in self.event_handlers:
            event_handler.render()
        pygame.display.update()

    def mouse_motion(self, event):
        cursor_position = pygame.mouse.get_pos()
        self.grid_position = [
            (cursor_position[0] - self.grid_density // 2 - self.user_position[0]) // self.grid_density,
            -(cursor_position[1] - self.grid_density // 2 - self.user_position[1]) // self.grid_density]


if __name__ == '__main__':
    App().run()
