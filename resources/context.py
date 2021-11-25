import consts


class Context:
    zoom_sensitivity = 1

    mouse_coordinates = [0, 0]
    is_moving = False

    info_bar_width = 0

    grid_density = consts.START_GRID_DENSITY
    user_position = consts.MAP_DEFAULT_POS

    is_drawing = False
