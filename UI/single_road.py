import pygame
from pygame.surface import Surface


class SingleRoad:

    def __init__(self, parent, screen: Surface, start_point, end_point):
        self.parent = parent
        self.screen = screen

        self.start_point = start_point
        self.end_point = end_point

        self.parent.renderables.append(self)

    def render(self):
        a = (self.start_point[0] * self.parent.grid_density + self.parent.user_position[0],
             -self.start_point[1] * self.parent.grid_density + self.parent.user_position[1])
        b = (self.end_point[0] * self.parent.grid_density + self.parent.user_position[0],
             -self.end_point[1] * self.parent.grid_density + self.parent.user_position[1])
        pygame.draw.line(self.screen, (0, 0, 0), a, b)
