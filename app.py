from typing import Callable

from pygame import Surface

from context.context_provider import ContextProvider


class App(ContextProvider):
    def __init__(self, screen: Surface, add_every_frame_render: Callable, add_event_handlers: Callable, add_dirty_rectangle: Callable):
        super().context.screen = screen
        super().context.add_every_frame_render = add_every_frame_render
        super().context.add_event_handlers = add_event_handlers
        super().context.add_dirty_rectangle = add_dirty_rectangle

