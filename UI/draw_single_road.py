import pygame
from pygame.event import Event

from line import Line
from resources import context, core, correct_rectangle
from const import color


class DrawSingleRoad:
    start_point = None
    end_point = None
    rectangle = pygame.Rect(0, 0, 0, 0)

    group = pygame.sprite.GroupSingle()

    def __init__(self):
        core.event_handlers.append(self)
        pass

    def dirty_render(self):
        core.background_rectangles.append(correct_rectangle(self.rectangle))

        a = (self.start_point[0] * context.grid_density + context.user_position[0],
             -self.start_point[1] * context.grid_density + context.user_position[1])
        b = self.end_point

        self.rectangle = Line(a, b).get_rect().inflate(2, 2)

        core.roads_to_draw.append((a, b))

        # for line in core.lines:
        #     if line.colliderect(self.rectangle):
        #         core.roads_to_draw.append((line.start, line.end))

        core.dirty_rectangles.append(self.rectangle)

    def handle_event(self, event: Event):
        options = {
            pygame.MOUSEBUTTONDOWN: self.mouse_button_down,
            pygame.MOUSEBUTTONUP: self.mouse_button_up,
            pygame.MOUSEMOTION: self.mouse_motion,
        }

        try:
            options[event.type](event)
        except KeyError:
            pass

    def mouse_button_down(self, event: Event):
        def button_left():
            # if not self.parent.drawing:
            #     return
            x, y = context.mouse_coordinates
            x *= context.grid_density
            y *= context.grid_density
            x_fix = core.foreground.rect.x % context.grid_density
            y_fix = core.foreground.rect.y % context.grid_density
            self.start_point = (x + x_fix, abs(y))
            self.end_point = pygame.mouse.get_pos()
            # self.dirty_render()


        options = {
            pygame.BUTTON_LEFT: button_left,
        }
        options[event.button]()

    def mouse_button_up(self, event: Event):
        def button_left():
            # single_road = SingleRoad(self.start_point, context.mouse_coordinates)
            # core.road_group.add(single_road)
            # self.dirty_render()
            pygame.draw.line(core.foreground.image, color.BLACK, self.start_point, self.end_point)
            core.foreground.render()
            self.start_point = None
            self.end_point = None

        options = {
            pygame.BUTTON_LEFT: button_left,
        }
        options[event.button]()

    def mouse_motion(self, event: Event):
        if self.start_point is not None:
            if self.group.sprites():
                self.group.clear(core.screen, core.foreground.image)

            self.end_point = pygame.mouse.get_pos()
            self.group.empty()
            self.group.add(Line(self.start_point, self.end_point))
            self.group.draw(core.screen)
