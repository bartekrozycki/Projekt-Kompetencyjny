import pygame

from resources import core, context


class SingleRoad:

    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point

        core.renderables.append(self)

    def render(self):
        a = (self.start_point[0] * context.grid_density + context.user_position[0],
             -self.start_point[1] * context.grid_density + context.user_position[1])
        b = (self.end_point[0] * context.grid_density + context.user_position[0],
             -self.end_point[1] * context.grid_density + context.user_position[1])

        pygame.draw.line(core.screen, (0, 0, 0), a, b)
