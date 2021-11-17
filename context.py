import config


class Context():
    zoom_sensitivity = 1

    mouse_coordinates = [0, 0]
    is_moving = False

    info_bar_width = 0

    grid_density = config.start_grid_density
    user_position = config.map_default_pos

    is_drawing = False


class Core():
    every_frame_render = []
    event_handlers = []
    renderables = []
    dirty_rectangles = []

    render_all = True


context = Context()
core = Core()
