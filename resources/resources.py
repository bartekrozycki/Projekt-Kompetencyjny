from components import Components
from context import Context

context = Context()
core = Core()
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
