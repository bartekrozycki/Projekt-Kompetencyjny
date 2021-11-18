import pygame
from pygame.event import Event
from UI.single_road import SingleRoad
from resources import components, context, core


class DrawSingleRoad:
    start_point = None
    end_point = None
    rectangle = pygame.Rect(0, 0, 0, 0)

    def __init__(self):
        core.event_handlers.append(self)
        pass

    def dirty_render(self):
        components.grid.dirty_render(self.rectangle) # FIXME bruh

        a = (self.start_point[0] * context.grid_density + context.user_position[0],
             -self.start_point[1] * context.grid_density + context.user_position[1])
        b = self.end_point

        self.rectangle = pygame.draw.line(core.screen, (0, 0, 0), a, b)
        core.dirty_rectangles.append(self.rectangle)

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
            self.start_point = context.mouse_coordinates
            self.end_point = pygame.mouse.get_pos()
            self.dirty_render()

        options = {
            pygame.BUTTON_LEFT: button_left,
        }
        options[event.button]()

    def mouse_button_up(self, event: Event):
        def button_left():
            SingleRoad(self.start_point, context.mouse_coordinates)
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
