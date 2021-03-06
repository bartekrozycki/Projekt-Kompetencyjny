import settings


class Context:
    zoom_sensitivity = 1

    mouse_coordinates = [0, 0]
    is_moving = False

    info_bar_width = 0

    grid_density = settings.GRID_START_DENSITY
    user_position = settings.MAP_DEFAULT_POSITION

    is_drawing = False

    drawing_active = False