import config

class Context():
    zoom = 1
    grid_position = [0, 0]
    info_bar_width = 0

    isDrawing = False

    grid_density = config.start_grid_density
    user_position = config.map_default_pos

    moving = False


class Core():
    every_frame_render = []
    event_handlers = []
    renderables = []
    dirty_rectangles = []

    render_all = False

context = Context()
core = Core()
