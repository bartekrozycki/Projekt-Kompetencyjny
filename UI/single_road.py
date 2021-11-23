import pygame

from line import Line
from resources import core, context


class SingleRoad(pygame.sprite.Sprite):
    line: Line

    def __init__(self, start_point, end_point):
        super().__init__()
        self.line = Line(start_point, end_point)
        core.renderables.append(self)
        core.lines.append(self.line)

        self.image = pygame.Surface(self.line.get_rect().size, pygame.SRCALPHA, 32)
        if type(self.line.a) is float:
            if self.line.a > 0:
                pygame.draw.line(self.image, (0, 0, 0), (self.line.left, self.line.bottom),
                                 (self.line.top, self.line.right))
            elif self.line.a < 0:
                pygame.draw.line(self.image, (0, 0, 0), (0, 0), (self.line.right, self.line.bottom))

        print(type(self.line.a))

        self.rect = self.image.get_rect()

        # core.road_group.add(self)
        # print(self.line)

    def render(self):
        a = (self.line.start[0] * context.grid_density + context.user_position[0],
             -self.line.start[1] * context.grid_density + context.user_position[1])
        b = (self.line.end[0] * context.grid_density + context.user_position[0],
             -self.line.end[1] * context.grid_density + context.user_position[1])

        pygame.draw.line(core.screen, (0, 0, 0), a, b)
