import pygame
from pygame.event import Event

from UI.road import Road
from const import tool
from resources import context, core


class DrawSingleRoad:
    start = None
    end = None
    group = pygame.sprite.GroupSingle()

    def __init__(self):
        core.event_handlers.append(self)
        pass

    def handle_event(self, event: Event):
        if not context.is_tool_active(tool.DRAW_ROAD):
            return

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
            self.start = tuple(context.mouse_coordinates)

        options = {
            pygame.BUTTON_LEFT: button_left,
        }
        options[event.button]()

    def mouse_button_up(self, event: Event):
        def button_left():
            core.foreground.roads.add(self.group.sprite)
            core.foreground.update_roads()
            core.foreground.render()
            self.start = None
            self.end = None

        options = {
            pygame.BUTTON_LEFT: button_left,
        }
        options[event.button]()

    def mouse_motion(self, event: Event):
        if self.start is None or self.end == tuple(context.mouse_coordinates):
            return

        self.group.clear(core.screen, core.foreground.image)
        self.group.empty()

        self.end = tuple(context.mouse_coordinates)

        line = Road(self.start, self.end)

        self.group.add(line)
        self.group.draw(core.screen)
