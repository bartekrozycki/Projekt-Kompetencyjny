import pickle
from types import SimpleNamespace

from src import constants, state
from src.constants import *


def create_background():
    w, h = state.resolution
    x, y = state.offset

    background = pygame.Surface((3 * w, 3 * h))
    background.fill(constants.D_GRAY)

    state.visible_roads = []
    b_rect = pygame.Rect(-w, -h, 3 * w, 3 * h)

    for index in b_rect.collidelistall(state.roads):
        state.visible_roads.append(state.roads[index])
        pygame.draw.rect(background, BLACK, state.roads[index].rect.move(w - x, h - y))

    for index in b_rect.collidelistall(state.selected_roads):
        pygame.draw.rect(background, YELLOW, state.selected_roads[index].rect.move(w - x, h - y), 1)

    return background


def bg_visible_area():
    w, h = state.resolution
    return pygame.Rect(w + state.menu.width, h, w - state.menu.width, h)


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

    if name not in state.modes.keys():
        return
    state.modes[name] = True
    draw_button(name, GREEN)
    state.selected_mode = name
    locals()[state.selected_mode]()


def mode_destructor(name):
    def select():
        pass

    def draw():
        for line in state.draw_mode.p_lines:
            state.window.blit(state.background, line, area=line.move(*state.resolution))
        pygame.display.update(state.draw_mode.p_lines)

    state.modes[name] = False
    draw_button(name, WHITE)
    locals()[name]()


def erase_all_roads():
    state.roads = []
    state.background = create_background()
    state.window.blit(state.background, (state.menu.width, 0), bg_visible_area())
    pygame.display.update()


def draw_button(name, color):
    i = state.button_names.index(name)
    rect = pygame.Rect(BUTTON_GAP_V, BUTTON_GAP_H + i * (BUTTON_GAP_H + BUTTON_H), MENU_W - 2 * BUTTON_GAP_V, BUTTON_H)
    text_render = state.font_consolas.render(name, False, constants.BLACK)
    pygame.draw.rect(state.window, color, rect),
    pygame.Surface.blit(state.window, text_render, rect.move(rect.w // 2 - text_render.get_rect().w // 2, 3))
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

    return SimpleNamespace(rect=rect.move(ox, oy), connections=[], start=start, end=end)


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
