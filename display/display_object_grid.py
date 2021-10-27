import pygame
from pygame.event import Event

import config
from display.display_object_interface import DisplayObjectInterface


class Grid(DisplayObjectInterface):
    grid_density = config.grid_density

    def __init__(self, parent, screen):
        super().__init__(parent, screen)
        self.parent = parent
        self.screen = screen
        self.prev_mouse_pos = None

    def dispatch_event(self, events: list[Event]):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_MIDDLE:
                    self.parent.moving = True
                elif event.button == pygame.BUTTON_WHEELUP:
                    self.parent.zoom *= 1.125
                    self.grid_density *= 1.125
                elif event.button == pygame.BUTTON_WHEELDOWN:
                    self.parent.zoom /= 1.125
                    self.grid_density /= 1.125
            elif event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_MIDDLE:
                self.parent.moving = False
                self.prev_mouse_pos = None
            elif event.type == pygame.MOUSEMOTION and self.parent.moving:
                if self.prev_mouse_pos is not None:
                    mouse_pos = pygame.mouse.get_pos()
                    self.parent.user_position[0] += mouse_pos[0] - self.prev_mouse_pos[0]
                    self.parent.user_position[1] += mouse_pos[1] - self.prev_mouse_pos[1]
                self.prev_mouse_pos = pygame.mouse.get_pos()

    def render(self):
        win_width, win_height = self.screen.get_size()
        pos_x, pos_y = self.parent.user_position

        x = pos_x % self.grid_density
        y = pos_y % self.grid_density

        while x < win_width:
            while y < win_height:
                pygame.draw.rect(self.screen, (0, 0, 0), (x, y, 1, 1), 1)
                y += self.grid_density
            y = pos_y % self.grid_density
            x += self.grid_density
