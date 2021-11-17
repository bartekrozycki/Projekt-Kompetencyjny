import pygame
from pygame.event import Event
from pygame.surface import Surface
from UI.single_road import SingleRoad


class DrawSingleRoad:
    start_point = None
    end_point = None
    rectangle = pygame.Rect(0, 0, 0, 0)

    def __init__(self, parent, screen: Surface):
        self.parent = parent
        self.screen = screen

        self.parent.event_handlers.append(self)

    def dirty_render(self):
        self.parent.grid.dirty_render(self.rectangle)

        a = (self.start_point[0] * self.parent.grid_density + self.parent.user_position[0],
             -self.start_point[1] * self.parent.grid_density + self.parent.user_position[1])
        b = self.end_point
        self.rectangle = pygame.draw.line(self.screen, (0, 0, 0), a, b)
        self.parent.dirty_rectangles.append(self.rectangle)

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
        def button_left():
            # if not self.parent.drawing:
            #     return
            self.start_point = self.parent.grid_position
            self.end_point = pygame.mouse.get_pos()
            self.dirty_render()

        options = {
            pygame.BUTTON_LEFT: button_left,
        }
        options[event.button]()

    def mouse_button_up(self, event: Event):
        def button_left():
            SingleRoad(self.parent, self.screen, self.start_point, self.parent.grid_position)
            self.start_point = None
            self.end_point = None

        options = {
            pygame.BUTTON_LEFT: button_left,
        }
        options[event.button]()

    def mouse_motion(self, event: Event):
        if self.start_point is not None:
            self.end_point = pygame.mouse.get_pos()
            self.dirty_render()
