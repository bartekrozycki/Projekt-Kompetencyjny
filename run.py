import pygame
from pygame.constants import QUIT

import config
from UI.zoom import Zoom
from app import App


class Run:
    pygame.font.init()
    pygame.display.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((config.display_width, config.display_height), config.display_flags)

    every_frame_render = []
    event_handlers = []
    dirty_rectangles = []

    running = True
    render_all = False

    def set_info_bar_width(self, width):
        self.info_bar_width = width

    def __init__(self):
        App(self.screen, self.every_frame_render.append, self.event_handlers.append, self.dirty_rectangles.append)

        # self.add_renderer(Grid)
        # self.add_renderer(Coordinates)
        # self.add_renderer(FPSCounter)
        Zoom()

        self.video_resize(None)

    def render(self):
        if self.render_all:
            for event_handler in self.event_handlers:
                event_handler.render()
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
            pygame.VIDEORESIZE: self.video_resize,
            pygame.MOUSEMOTION: self.mouse_motion,
        }

        try:
            options[event.type](event)
        except:
            pass

    def video_resize(self, event):
        self.render_all = True

    def mouse_motion(self, event):
        cursor_position = pygame.mouse.get_pos()
        self.grid_position = [
            (cursor_position[0] - self.grid_density // 2 - self.user_position[0]) // self.grid_density,
            -(cursor_position[1] - self.grid_density // 2 - self.user_position[1]) // self.grid_density]


if __name__ == '__main__':
    Run().run()
