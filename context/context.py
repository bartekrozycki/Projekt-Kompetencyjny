from typing import Callable

from pygame import Surface


class Context():
    screen: Surface = None
    grid_position: [int, int] = None
    info_bar_width: int = None
    zoom: int = None

    # Callable methods to add object to renderer #todo
    add_every_frame_render: Callable = None
    add_event_handlers: Callable = None
    add_dirty_rectangle: Callable = None

    def __init__(self):
        pass
