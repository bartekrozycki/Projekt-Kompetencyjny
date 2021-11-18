from pygame import Surface
from pygame.time import Clock


class Core:
    screen: Surface
    clock: Clock

    every_frame_render = []
    event_handlers = []
    renderables = []
    dirty_rectangles = []

    render_all = True
