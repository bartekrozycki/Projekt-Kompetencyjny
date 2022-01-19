import pygame

from src import constants, state
from src.constants import CELL_SIZE, BLACK
from src.state import drawing, modes, selecting


def recreate_background(x, y, color=constants.SKY_BLUE):
    res_w, res_h = state.resolution

    background = pygame.sprite.Sprite()
    background.rect = pygame.Rect(x, y, res_w * 3, res_h * 3)
    background.image = pygame.Surface(background.rect.size)

    background.image.fill(color)

    state.visible_roads = []

    for road in state.roads:
        if road.colliderect(background.rect):
            state.visible_roads.append(road)
            pygame.draw.rect(background.image, BLACK, road.move(res_w, res_h))

    return background


def background_display_rectangle(x, y):
    res_w, res_h = state.resolution
    return pygame.rect.Rect(res_w + x, res_h + y, res_w - state.menu.width, res_h)


def recreate_menu():
    res_w, res_h = state.resolution

    menu = pygame.sprite.Sprite()
    menu.rect = pygame.Rect(0, 0, state.menu.width, res_h)
    menu.image = pygame.Surface(menu.rect.size)

    menu.image.fill(constants.BLACK)

    render_buttons()

    return menu


def button_select():
    for mode in modes:
        mode.on = False
    selecting.on = True


def button_draw():
    for mode in modes:
        mode.on = False
    drawing.on = True


def render_button(index, color=constants.WHITE):
    button = state.buttons[index]
    rect = pygame.rect.Rect(5, 5 + index * 30, state.menu.width - 10, 20)
    text_render = state.font_consolas.render(button.text, False, constants.BLACK)
    pygame.draw.rect(state.window, color, rect),
    pygame.Surface.blit(state.window, text_render, rect.move(rect.w // 2 - text_render.get_rect().w // 2, 3))


def render_buttons():
    for i in range(len(state.buttons)):
        render_button(i)

    if state.highlighted_button_index < len(state.buttons):
        render_button(state.highlighted_button_index, constants.GREEN)


def create_ver_hor_rectangle(start, end, thickness):
    x1, y1 = start
    x2, y2 = end

    diff_x = abs(x2 - x1)
    diff_y = abs(y2 - y1)

    if diff_x > diff_y:
        rect = pygame.Rect(x1 * thickness, y1 * thickness, thickness * (diff_x + 1),
                           thickness)
        if x1 > x2:
            rect = rect.move(-diff_x * thickness, 0)
    else:
        rect = pygame.Rect(x1 * thickness, y1 * thickness, thickness, thickness * (diff_y + 1))
        if y1 > y2:
            rect = rect.move(0, -diff_y * thickness)

    return rect


def render_cursor():
    x, y = state.coordinates
    size = CELL_SIZE
    cursor_rect = pygame.Rect(x * size, y * size, size, size)

    prev_cursor_rect = state.prev_cursor_rect

    res_x, res_y = state.resolution
    left, top = state.background.rect.topleft

    if prev_cursor_rect:
        state.window.blit(state.background.image, prev_cursor_rect,
                          area=prev_cursor_rect.move(left + 2 * res_x, top + 2 * res_y))
        pygame.display.update(prev_cursor_rect)

    state.prev_cursor_rect = cursor_rect

    pygame.draw.rect(state.window, constants.WHITE, cursor_rect, 1)
    pygame.display.update(cursor_rect)
