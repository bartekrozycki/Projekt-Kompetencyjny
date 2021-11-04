from abc import ABC, abstractmethod
from typing import Callable

from pygame.event import Event

from context.context_provider import ContextProvider


class AbstractObject(ABC, ContextProvider):
    options = {}

    def add_event_handler(self, event: int, func: Callable):
        self.options[event] = func

    def handle_event(self, event: Event) -> None:
        try:
            self.options[event.type](event)
        except KeyError:
            pass
        except Exception as e:
            print(type(e), e)

    @abstractmethod
    def render(self) -> None:
        pass
