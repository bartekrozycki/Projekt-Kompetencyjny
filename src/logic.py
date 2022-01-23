import pickle
from types import SimpleNamespace

from src import constants, state
from src.constants import *


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

    draw_buttons()

    return menu


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
            state.window.blit(state.background.image, line, area=line.move(*state.resolution))
        pygame.display.update(state.draw_mode.p_lines)

    state.modes[name] = False
    draw_button(name, WHITE)
    locals()[name]()


def erase_all_roads():
    state.roads = []
    state.background = create_background()
    res_w, res_h = state.resolution
    state.window.blit(state.background.image, (100, 0), area=(res_w + 100, res_h, res_w - 100, res_h))
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
    start = [start[0] + ox // CELL_SIZE, start[1] + oy // CELL_SIZE]
    end = [end[0] + ox // CELL_SIZE, end[1] + oy // CELL_SIZE]

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
