import pygame

from src import constants, state
from src.constants import CELL_SIZE, BLACK
from src.state import drawing, modes, selecting


def recreate_background():
    w, h = state.resolution
    x, y = state.offset

    background = pygame.sprite.Sprite()
    background.rect = pygame.Rect(0, 0, w * 3, h * 3)
    background.image = pygame.Surface(background.rect.size)

    background.image.fill(constants.SKY_BLUE)

    state.visible_roads = []

    background_pos = background.rect.move(x, y)

    for road in state.roads:
        if road.colliderect(background_pos):
            print(road, road.move(w - x, h - y))
            state.visible_roads.append(road)
            pygame.draw.rect(background.image, BLACK, road.move(w - x, h - y))

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


def create_road(start, end):
    x1, y1 = start
    x2, y2 = end

    diff_x = abs(x2 - x1)
    diff_y = abs(y2 - y1)

    if diff_x > diff_y:
        rect = pygame.Rect(x1 * CELL_SIZE, y1 * CELL_SIZE, CELL_SIZE * (diff_x + 1),
                           CELL_SIZE)
        if x1 > x2:
            rect = rect.move(-diff_x * CELL_SIZE, 0)
    else:
        rect = pygame.Rect(x1 * CELL_SIZE, y1 * CELL_SIZE, CELL_SIZE, CELL_SIZE * (diff_y + 1))
        if y1 > y2:
            rect = rect.move(0, -diff_y * CELL_SIZE)

    x, y = state.offset

    return rect.move(x - x % 10, y - y % 10)
