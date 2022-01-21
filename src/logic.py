import pickle
from types import SimpleNamespace

import pygame

from src import constants, state
from src.constants import *
from src.state import draw_mode, modes, select_mode


def create_background():
    w, h = state.resolution
    x, y = state.offset

    background = pygame.sprite.Sprite()
    background.rect = pygame.Rect(-w, -h, w * 3, h * 3)
    background.image = pygame.Surface(background.rect.size)

    background.image.fill(constants.D_GRAY)

    state.visible_roads = []

    background_pos = background.rect.move(x, y)

    for road in state.roads:
        if road.rect.colliderect(background_pos):
            state.visible_roads.append(road)
            pygame.draw.rect(background.image, BLACK, road.rect.move(w - x, h - y))

    for s_road in state.selected_roads:
        if s_road.rect.colliderect(background_pos):
            pygame.draw.rect(background.image, YELLOW, s_road.rect.move(w - x, h - y), 1)

    return background


def background_display_rectangle(x, y):
    res_w, res_h = state.resolution
    return pygame.rect.Rect(res_w + x, res_h + y, res_w - state.menu.width, res_h)


def create_menu():
    res_w, res_h = state.resolution

    menu = pygame.sprite.Sprite()
    menu.rect = pygame.Rect(0, 0, state.menu.width, res_h)
    menu.image = pygame.Surface(menu.rect.size)

    menu.image.fill(constants.BLACK)

    render_buttons()

    return menu


def press_button(name):
    if name == state.select_mode:
        return

    def select():
        mode_destructor()
        draw_button(name, GREEN)
        select_mode.on = True
        state.selected_mode = 'select'

    def draw():
        mode_destructor()
        draw_button(name, GREEN)
        draw_mode.on = True
        state.selected_mode = 'draw'

    def clear():
        erase_all_roads()

    locals()[name]()


def mode_destructor():
    def select():
        select_mode.on = False

    def draw():
        draw_mode.on = False
        for line in state.draw_mode.p_lines:
            state.window.blit(state.background.image, line, area=line.move(*state.resolution))
        pygame.display.update(draw_mode.p_lines)

    draw_button(state.selected_mode, WHITE)
    locals()[state.selected_mode]()


def erase_all_roads():
    state.roads = []
    state.background = create_background()
    res_w, res_h = state.resolution
    state.window.blit(state.background.image, (100, 0), area=(res_w + 100, res_h, res_w - 100, res_h))
    pygame.display.update()


def button_select():
    for mode in modes:
        mode.on = False
    select_mode.on = True

    for line in state.draw_mode.p_lines:
        state.window.blit(state.background.image, line, area=line.move(*state.resolution))
    pygame.display.update(draw_mode.p_lines)


def button_draw():
    for mode in modes:
        mode.on = False
    draw_mode.on = True


def render_button(index, color=constants.WHITE):
    button = state.buttons[index]
    rect = pygame.rect.Rect(BUTTON_GAP_V, 10 + index * 30, state.menu.width - 10, 20)
    text_render = state.font_consolas.render(button.text, False, constants.BLACK)
    pygame.draw.rect(state.window, color, rect),
    pygame.Surface.blit(state.window, text_render, rect.move(rect.w // 2 - text_render.get_rect().w // 2, 3))


def draw_button(name, color):
    i = state.button_names.index(name)
    rect = pygame.Rect(BUTTON_GAP_V, BUTTON_GAP_H + i * (BUTTON_GAP_H + BUTTON_H), MENU_W - 2 * BUTTON_GAP_V, BUTTON_H)
    text_render = state.font_consolas.render(name, False, constants.BLACK)
    pygame.draw.rect(state.window, color, rect),
    pygame.Surface.blit(state.window, text_render, rect.move(rect.w // 2 - text_render.get_rect().w // 2, 3))
    pygame.display.update(rect)


def render_buttons():
    # for i in range(len(state.buttons)):
    #     render_button(i)
    #
    # if state.highlighted_button_index < len(state.buttons):
    #     render_button(state.highlighted_button_index, constants.GREEN)
    for name in state.button_names:
        try:
            draw_button(name, GREEN if state.modes_on[name] else WHITE)
        except:
            draw_button(name, WHITE)



def create_road(start, end):
    x1, y1 = start
    x2, y2 = end

    diff_x = abs(x2 - x1)
    diff_y = abs(y2 - y1)

    if diff_x > diff_y:
        rect = pygame.Rect(x1 * CELL_SIZE, y1 * CELL_SIZE, CELL_SIZE * (diff_x + 1),
                           CELL_SIZE)
        end[1] = start[1]
        if x1 > x2:
            rect = rect.move(-diff_x * CELL_SIZE, 0)
    else:
        rect = pygame.Rect(x1 * CELL_SIZE, y1 * CELL_SIZE, CELL_SIZE, CELL_SIZE * (diff_y + 1))
        end[0] = start[0]
        if y1 > y2:
            rect = rect.move(0, -diff_y * CELL_SIZE)

    ox, oy = state.offset
    start = [start[0] + ox // CELL_SIZE, start[1] + oy // CELL_SIZE]
    end = [end[0] + ox // CELL_SIZE, end[1] + oy // CELL_SIZE]

    return SimpleNamespace(rect=rect.move(ox, oy), connections=[], start=start, end=end)


def button_clear_workspace():
    state.roads = []
    # update workspace
    state.background = create_background()  # create background
    res_w, res_h = state.resolution
    state.window.blit(state.background.image, (100, 0), area=(res_w + 100, res_h, res_w - 100, res_h))
    state.bg_menu = create_menu()
    pygame.display.update()
    ###
    roads_file = open(constants.ROADS_FILENAME, 'wb')
    pickle.dump(state.roads, roads_file)
    roads_file.close()


def save():
    roads_file = open(constants.ROADS_FILENAME, 'wb')
    pickle.dump(state.roads, roads_file)
    roads_file.close()


def load():
    try:
        roads_file = open(constants.ROADS_FILENAME, 'rb')
        state.roads = pickle.load(roads_file)
        roads_file.close()
    except EOFError:
        print("Empty file")
    except FileNotFoundError:
        print("Not found any roads file")
