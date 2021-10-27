from __future__ import annotations

from pygame.event import Event
from pygame.surface import SurfaceType, Surface


class DisplayObjectInterface:
    def __init__(self, parent, screen: Surface | SurfaceType):
        self.screen = screen
        self.user_position = parent.user_position

    def dispatch_event(self, events: list[Event]):
        pass

    def render(self):
        pass
