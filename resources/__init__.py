import pygame

from resources._core import Core
from resources.context import Context

context: Context = Context()
core = Core()



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
