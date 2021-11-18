import settings


class Context:
    zoom_sensitivity = 1

    mouse_coordinates = [0, 0]
    is_moving = False

    info_bar_width = 0

    grid_density = settings.start_grid_density
    user_position = settings.map_default_pos

    is_drawing = False
