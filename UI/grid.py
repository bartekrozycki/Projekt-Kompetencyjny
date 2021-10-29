import pygame
from pygame.event import Event
from pygame.surface import Surface

import config


class Grid:
    surface = None

    def __init__(self, parent, screen: Surface):
        self.parent = parent
        self.screen = screen
        self.size = [0, 0]
        self.generate_grid()
        self.prev_mouse_pos = None

        self.parent.event_handlers.append(self)

    def generate_grid(self):
        self.size = [self.screen.get_width() + self.parent.grid_density,
                     self.screen.get_height() + self.parent.grid_density]

        self.surface = pygame.Surface(self.size)

        self.surface.fill((135, 206, 250))

        if self.parent.grid_density <= config.min_grid_density:
            return

        x = 0
        y = 0
        dot_size = 2 if self.parent.grid_density > 20 else 1

        # drawing grid dots
        while x <= self.screen.get_width() + self.parent.grid_density:
            while y <= self.screen.get_height() + self.parent.grid_density:
                pygame.draw.rect(self.surface, (0, 0, 0), (x, y, dot_size, dot_size), 1)
                y += self.parent.grid_density
            y = 0
            x += self.parent.grid_density

    def render(self):
        x = -(self.parent.grid_density - self.parent.user_position[0] % self.parent.grid_density)
        y = -(self.parent.grid_density - self.parent.user_position[1] % self.parent.grid_density)

        self.screen.blit(self.surface, (x, y, self.size[0], self.size[1]))

    def handle_event(self, event: Event):
        options = {
            pygame.MOUSEBUTTONDOWN: self.mouse_button_down,
            pygame.MOUSEBUTTONUP: self.mouse_button_up,
            pygame.MOUSEMOTION: self.mouse_motion,
            pygame.VIDEORESIZE: self.video_resize,
        }

        try:
            options[event.type](event)
        except:
            pass

    def mouse_button_down(self, event: Event):
        mouse_pos = pygame.mouse.get_pos()
        zoom_factor = 1.125

        # moving the grid
        def button_middle():
            self.parent.moving = True

        # zoom in
        def button_wheel_up():
            if not self.parent.grid_density <= config.max_grid_density:
                return

            self.parent.zoom *= zoom_factor
            self.parent.grid_density *= zoom_factor

            dx = int(mouse_pos[0] - self.parent.user_position[0]) * (zoom_factor - 1)
            dy = int(mouse_pos[1] - self.parent.user_position[1]) * (zoom_factor - 1)

            self.parent.user_position[0] -= dx
            self.parent.user_position[1] -= dy

            self.generate_grid()
            self.parent.render_all = True

        # zoom out
        def button_wheel_down():
            if not self.parent.grid_density >= config.min_grid_density:
                self.generate_grid()
                self.parent.render_all = True
                return
            self.parent.zoom /= zoom_factor
            self.parent.grid_density /= zoom_factor

            dx = int(mouse_pos[0] - self.parent.user_position[0]) * (1 / zoom_factor - 1)
            dy = int(mouse_pos[1] - self.parent.user_position[1]) * (1 / zoom_factor - 1)

            self.parent.user_position[0] -= dx
            self.parent.user_position[1] -= dy

            if not self.parent.grid_density > 2:
                return
            self.generate_grid()
            self.parent.render_all = True

        options = {
            pygame.BUTTON_MIDDLE: button_middle,
            pygame.BUTTON_WHEELUP: button_wheel_up,
            pygame.BUTTON_WHEELDOWN: button_wheel_down,
        }
        options[event.button]()

    def mouse_button_up(self, event: Event):
        # moving the grid
        def button_middle():
            self.parent.moving = False
            self.prev_mouse_pos = None

        options = {
            pygame.BUTTON_MIDDLE: button_middle,
        }
        options[event.button]()

    def mouse_motion(self, event: Event):
        # moving the grid
        if self.parent.moving:
            try:
                mouse_pos = pygame.mouse.get_pos()
                self.parent.user_position[0] += mouse_pos[0] - self.prev_mouse_pos[0]
                self.parent.user_position[1] += mouse_pos[1] - self.prev_mouse_pos[1]
            finally:
                self.prev_mouse_pos = pygame.mouse.get_pos()
                self.parent.render_all = True

    def video_resize(self, event: Event):
        self.generate_grid()
