import pygame

from resources._core import Core
from resources.context import Context
from resources.images import Images
from resources.tool import ActiveTool

context: Context = Context()
core = Core()
images = Images()
activeTool = ActiveTool()


def renderable(func):
    def inner(self, *args, **kwargs):
        core.renderables.append(self)
        return func(self, *args, **kwargs)

    return inner


def renderable_every_frame(func):
    def inner(self, *args, **kwargs):
        core.every_frame_render.append(self)
        return func(self, *args, **kwargs)

    return inner

# if handler returns True, all other handler ll be cancelled.
def event_handler(func):
    def inner(self, *args, **kwargs):
        core.event_handlers.append(self)
        return func(self, *args, **kwargs)

    return inner


def rect_from_2points(a, b):
    return correct_rectangle(pygame.Rect(a, (b[0] - a[0], b[1] - a[1])))


def correct_rectangle(rectangle: pygame.Rect):
    x, y, w, h = rectangle

    if w < 0:
        x += w
        w = -w
    if h < 0:
        y += h
        h = -h

    return pygame.Rect(x, y, w, h)
