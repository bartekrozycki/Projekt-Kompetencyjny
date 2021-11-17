import pygame
from pygame.event import Event
from pygame.surface import Surface

import config
from context import context, core


class Grid:
    surface = None

    def __init__(self, screen: Surface):
        self.screen = screen
        self.size = [0, 0]
        self.generate_grid()
        self.prev_mouse_pos = None

        core.event_handlers.append(self)
        core.renderables.append(self)

    def generate_grid(self):
        self.size = [self.screen.get_width() + context.grid_density,
                     self.screen.get_height() + context.grid_density]

        self.surface = pygame.Surface(self.size)

        self.surface.fill((135, 206, 250))

        if context.grid_density <= config.min_grid_density:
            return

        x = 0
        y = 0
        dot_size = 2 if context.grid_density > 20 else 1

        # drawing grid dots
        while x <= self.screen.get_width() + context.grid_density:
            while y <= self.screen.get_height() + context.grid_density:
                pygame.draw.rect(self.surface, (0, 0, 0), (x, y, dot_size, dot_size), 1)
                y += context.grid_density
            y = 0
            x += context.grid_density

    def render(self):
        x = -(context.grid_density - context.user_position[0] % context.grid_density)
        y = -(context.grid_density - context.user_position[1] % context.grid_density)

        self.screen.blit(self.surface, (x, y, self.size[0], self.size[1]))

    def dirty_render(self, rectangle: pygame.Rect):
        x = (context.grid_density - context.user_position[0] % context.grid_density)
        y = (context.grid_density - context.user_position[1] % context.grid_density)

        self.screen.blit(self.surface, rectangle.move(x, y))
        core.dirty_rectangles.append(rectangle.move(x, y))

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

        # is_moving the grid
        def button_middle():
            context.is_moving = True

        # zoom_sensitivity in
        def button_wheel_up():
            if not context.grid_density <= config.max_grid_density:
                return

            context.zoom_sensitivity *= zoom_factor
            context.grid_density *= zoom_factor

            dx = int(mouse_pos[0] - context.user_position[0]) * (zoom_factor - 1)
            dy = int(mouse_pos[1] - context.user_position[1]) * (zoom_factor - 1)

            context.user_position[0] -= dx
            context.user_position[1] -= dy

            self.generate_grid()
            core.render_all = True

        # zoom_sensitivity out
        def button_wheel_down():
            if not context.grid_density >= config.min_grid_density:
                self.generate_grid()
                core.render_all = True
                return
            context.zoom_sensitivity /= zoom_factor
            context.grid_density /= zoom_factor

            dx = int(mouse_pos[0] - context.user_position[0]) * (1 / zoom_factor - 1)
            dy = int(mouse_pos[1] - context.user_position[1]) * (1 / zoom_factor - 1)

            context.user_position[0] -= dx
            context.user_position[1] -= dy

            if not context.grid_density > 2:
                return
            self.generate_grid()
            core.render_all = True

        options = {
            pygame.BUTTON_MIDDLE: button_middle,
            pygame.BUTTON_WHEELUP: button_wheel_up,
            pygame.BUTTON_WHEELDOWN: button_wheel_down,
        }
        options[event.button]()

    def mouse_button_up(self, event: Event):
        # is_moving the grid
        def button_middle():
            context.is_moving = False
            self.prev_mouse_pos = None

        options = {
            pygame.BUTTON_MIDDLE: button_middle,
        }
        options[event.button]()

    def mouse_motion(self, event: Event):
        # is_moving the grid
        if context.is_moving:
            try:
                mouse_pos = pygame.mouse.get_pos()
                context.user_position[0] += mouse_pos[0] - self.prev_mouse_pos[0]
                context.user_position[1] += mouse_pos[1] - self.prev_mouse_pos[1]
            finally:
                self.prev_mouse_pos = pygame.mouse.get_pos()
                core.render_all = True

    def video_resize(self, event: Event):
        self.generate_grid()
