import pickle

import pygame.draw

from src import constants, state
from src.constants import *


def create_background():
    w, h = state.resolution
    ox, oy = state.offset

    state.background = pygame.Surface((3 * w, 3 * h))
    state.background.fill(constants.D_GREY)

    b_rect = pygame.Rect(-w, -h, 3 * w, 3 * h)

    state.visible_roads = []
    for road in [state.roads[i] for i in b_rect.collidelistall(state.roads)]:
        state.visible_roads.append(road)
        pygame.draw.rect(state.background, BLACK, road.rect.move(w - ox, h - oy))

    for road in [state.selected_roads[i] for i in b_rect.collidelistall(state.selected_roads)]:
        draw_road_on_bg(road, L_GREY, 1)
        draw_road_start_end_on_bg(road)


def get_workspace_rect():
    w, h = state.resolution
    return pygame.Rect(w + MENU_W, h, w - MENU_W, h)


def update_workspace():
    state.display.blit(state.background, (MENU_W, 0), get_workspace_rect())
    pygame.display.update()


def press_button(name):
    def select():
        mode_destructor(state.selected_mode)
        mode_constructor('select')

    def draw():
        mode_destructor(state.selected_mode)
        mode_constructor('draw')

    def clear():
        erase_all_roads()

    if name == state.select_mode:
        return
    locals()[name]()


def mode_constructor(name):
    def select():
        pass

    def draw():
        pass

    if name not in state.modes:
        return
    draw_button(name, GREEN)
    state.selected_mode = name
    locals()[state.selected_mode]()


def mode_destructor(name):
    def select():
        pass

    def draw():
        for line in state.draw_mode.p_lines:
            state.display.blit(state.background, line, area=line.move(*state.resolution))
        pygame.display.update(state.draw_mode.p_lines)

    draw_button(name, WHITE)
    locals()[name]()


def erase_all_roads():
    state.roads = []
    state.background = create_background()
    state.display.blit(state.background, (MENU_W, 0), get_workspace_rect())
    pygame.display.update()


def draw_button(name, color):
    i = state.button_names.index(name)
    rect = pygame.Rect(BUTTON_GAP_V, BUTTON_GAP_H + i * (BUTTON_GAP_H + BUTTON_H), MENU_W - 2 * BUTTON_GAP_V, BUTTON_H)
    text_render = state.font_consolas.render(name, False, constants.BLACK)
    pygame.draw.rect(state.display, color, rect),
    pygame.Surface.blit(state.display, text_render, rect.move(rect.w // 2 - text_render.get_rect().w // 2, 3))
    pygame.display.update(rect)


def draw_buttons():
    for name in state.button_names:
        draw_button(name, WHITE)
    draw_button(state.selected_mode, GREEN)


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
    offset = [o // CELL_SIZE for o in state.offset]
    start = [start[i] + offset[i] for i in range(2)]
    end = [end[i] + offset[i] for i in range(2)]

    return state.Road([], rect.move(ox, oy), start, end)


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


def draw_road(road: state.Road, color=BLACK, border=0):
    ox, oy = state.offset
    rect = road.rect.move(-ox, -oy)
    if rect.left <= MENU_W:
        rect.width -= MENU_W - rect.left
        rect.left = MENU_W
    pygame.draw.rect(state.display, color, rect, border)
    return rect


def draw_road_on_bg(road: state.Road, color=BLACK, border=0):
    ox, oy = state.offset
    w, h = state.resolution
    rect = road.rect.move(w - ox, h - oy)

    pygame.draw.rect(state.background, color, rect, border)


def get_fitted_road_rect(road: state.Road):
    ox, oy = state.offset
    rect = road.rect.move(-ox, -oy)
    if rect.left <= MENU_W:
        rect.width -= MENU_W - rect.left
        rect.left = MENU_W
    return rect


def draw_bg(rect: pygame.Rect):
    w, h = state.resolution
    state.display.blit(state.background, rect, rect.move(w, h))


def draw_road_start_end(road: state.Road):
    ox, oy = state.offset
    sx, sy = road.start
    sx = sx * CELL_SIZE - ox
    sy = sy * CELL_SIZE - oy
    ex, ey = road.end
    ex = ex * CELL_SIZE - ox
    ey = ey * CELL_SIZE - oy

    if ex < sx:
        ex -= CELL_SIZE // 2
        sx += CELL_SIZE // 2

    if ey < sy:
        ey -= CELL_SIZE // 2
        sy += CELL_SIZE // 2

    if road.rect.h == CELL_SIZE:
        pygame.draw.rect(state.display, GREEN, (sx, sy, CELL_SIZE // 2, CELL_SIZE))
        pygame.draw.rect(state.display, RED, (ex + CELL_SIZE // 2, ey, CELL_SIZE // 2, CELL_SIZE))
    else:
        pygame.draw.rect(state.display, GREEN, (sx, sy, CELL_SIZE, CELL_SIZE // 2))
        pygame.draw.rect(state.display, RED, (ex, ey + CELL_SIZE // 2, CELL_SIZE, CELL_SIZE // 2))

def draw_road_start_end_on_bg(road: state.Road):
    w, h = state.resolution
    ox, oy = state.offset
    sx, sy = road.start
    sx = sx * CELL_SIZE - ox
    sy = sy * CELL_SIZE - oy
    ex, ey = road.end
    ex = ex * CELL_SIZE - ox
    ey = ey * CELL_SIZE - oy

    if ex < sx:
        ex -= CELL_SIZE // 2
        sx += CELL_SIZE // 2

    if ey < sy:
        ey -= CELL_SIZE // 2
        sy += CELL_SIZE // 2

    if road.rect.h == CELL_SIZE:
        pygame.draw.rect(state.background, GREEN, (sx + w, sy + h, CELL_SIZE // 2, CELL_SIZE))
        pygame.draw.rect(state.background, RED, (ex + CELL_SIZE // 2 + w, ey + h, CELL_SIZE // 2, CELL_SIZE))
    else:
        pygame.draw.rect(state.background, GREEN, (sx + w, sy + h, CELL_SIZE, CELL_SIZE // 2))
        pygame.draw.rect(state.background, RED, (ex + w, ey + CELL_SIZE // 2 + h, CELL_SIZE, CELL_SIZE // 2))
