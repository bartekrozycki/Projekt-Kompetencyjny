import pygame
from pygame.event import Event

import config


class Grid:

    def __init__(self, parent, screen):
        self.parent = parent
        self.screen = screen
        self.prev_mouse_pos = None

    def render(self):
        if self.parent.grid_density < 5:
            return
        win_width, win_height = self.screen.get_size()
        pos_x, pos_y = self.parent.user_position

        x = pos_x % self.parent.grid_density
        y = pos_y % self.parent.grid_density

        dot_size = 2 if self.parent.grid_density > 20 else 1

        while x < win_width:
            while y < win_height:
                pygame.draw.rect(self.screen, (0, 0, 0), (x, y, dot_size, dot_size), 1)
                y += self.parent.grid_density
            y = pos_y % self.parent.grid_density
            x += self.parent.grid_density

    def handle_event(self, event: Event):
        options = {
            pygame.MOUSEBUTTONDOWN: self.mouse_button_down,
            pygame.MOUSEBUTTONUP: self.mouse_button_up,
            pygame.MOUSEMOTION: self.mouse_motion,
        }

        try:
            options[event.type](event)
        except:
            pass

    def mouse_button_down(self, event: Event):
        mouse_pos = pygame.mouse.get_pos()
        factor = 1.125

        def button_middle():
            self.parent.moving = True

        def button_wheel_up():
            self.parent.zoom *= factor
            self.parent.grid_density *= factor

            dx = int(mouse_pos[0] - self.parent.user_position[0]) * (factor - 1)
            dy = int(mouse_pos[1] - self.parent.user_position[1]) * (factor - 1)

            self.parent.user_position[0] -= dx
            self.parent.user_position[1] -= dy

        def button_wheel_down():
            self.parent.zoom /= factor
            self.parent.grid_density /= factor

            dx = int(mouse_pos[0] - self.parent.user_position[0]) * (1/factor - 1)
            dy = int(mouse_pos[1] - self.parent.user_position[1]) * (1/factor - 1)

            self.parent.user_position[0] -= dx
            self.parent.user_position[1] -= dy


        options = {
            pygame.BUTTON_MIDDLE: button_middle,
            pygame.BUTTON_WHEELUP: button_wheel_up,
            pygame.BUTTON_WHEELDOWN: button_wheel_down,
        }
        options[event.button]()

    def mouse_button_up(self, event: Event):
        def button_middle():
            self.parent.moving = False
            self.prev_mouse_pos = None

        options = {
            pygame.BUTTON_MIDDLE: button_middle,
        }
        options[event.button]()

    def mouse_motion(self, event: Event):
        if self.parent.moving:
            try:
                mouse_pos = pygame.mouse.get_pos()
                self.parent.user_position[0] += mouse_pos[0] - self.prev_mouse_pos[0]
                self.parent.user_position[1] += mouse_pos[1] - self.prev_mouse_pos[1]
            finally:
                self.prev_mouse_pos = pygame.mouse.get_pos()
