from resources.components import Components
from resources.context import Context
from resources.core import Core

core = Core()
context = Context()
components = Components()

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


def event_handler(func):
    def inner(self, *args, **kwargs):
        core.event_handlers.append(self)
        return func(self, *args, **kwargs)

    return inner
