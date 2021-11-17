import config


class Context():
    zoom_sensitivity = 1

    mouse_coordinates = [0, 0]
    is_moving = False

    info_bar_width = 0

    grid_density = config.start_grid_density
    user_position = config.map_default_pos

    is_drawing = False

context = Context()

class Core():
    every_frame_render = []
    event_handlers = []
    renderables = []
    dirty_rectangles = []

    render_all = True


core = Core()

def Renderable(func):
    def inner(self, *args, **kwargs):
        core.renderables.append(self)
        return func(self, *args, **kwargs)
    return inner

def RenderableEveryFrame(func):
    def inner(self, *args, **kwargs):
        core.every_frame_render.append(self)
        return func(self, *args, **kwargs)
    return inner

def EventHandler(func):
    def inner(self, *args, **kwargs):
        core.event_handlers.append(self)
        return func(self, *args, **kwargs)
    return inner
