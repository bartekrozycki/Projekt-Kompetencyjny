from types import SimpleNamespace

import pygame

from src import state, logic
from src.constants import CELL_SIZE, EVENT_NAMES, MENU_W, BUTTON_NAMES, BLACK, WHITE, GREEN, RED
from src.state import drawing


def window(event: pygame.event.Event):
    # manages display while moving and cursor display
    def mouse_motion():
        prev_pos = state.mouse_pos
        pos = event.pos
        prev_coor = state.coordinates
        coor = [c // CELL_SIZE for c in pos]
        prev_rect = state.cursor.prev

        # clear previous cursor
        if pos[0] <= state.menu.width or coor != prev_coor:
            if prev_rect:
                state.window.blit(state.background.image, prev_rect, area=prev_rect.move(*state.resolution))
                pygame.display.update(prev_rect)
                state.cursor.prev = None
        # draw cursor
        if pos[0] > state.menu.width and coor != prev_coor:
            cursor_rect = pygame.Rect(pos[0] - pos[0] % 10, pos[1] - pos[1] % 10, CELL_SIZE, CELL_SIZE)

            pygame.draw.rect(state.window, WHITE, cursor_rect, 1)
            pygame.display.update(cursor_rect)
            state.cursor.prev = cursor_rect
        # move and display
        if pos[0] > state.menu.width and pygame.mouse.get_pressed(3)[1]:
            state.offset_change = [(state.offset_change[i] + prev_pos[i] - pos[i]) for i in range(2)]
            x, y = state.offset_change
            x = x - x % CELL_SIZE
            y = y - y % CELL_SIZE
            w, h = state.resolution
            state.window.blit(state.background.image, (MENU_W, 0), area=(w + MENU_W + x, h + y, w - MENU_W, h))

            pygame.display.update((MENU_W, 0, w - MENU_W, h))

        state.mouse_pos = pos
        state.coordinates = coor

    def video_resize():
        state.resolution = event.size
        state.background = logic.recreate_background()  # create background

        res_w, res_h = state.resolution
        state.window.blit(state.background.image, (100, 0), area=(res_w + 100, res_h, res_w - 100, res_h))

        state.bg_menu = logic.recreate_menu()

        pygame.display.update()

    def mouse_button_up():
        def button_middle():
            x, y = state.offset_change
            state.offset_change = [x - x % CELL_SIZE, y - y % CELL_SIZE]
            state.offset = [state.offset[i] + state.offset_change[i] for i in range(2)]
            state.offset_change = [0, 0]
            state.background = logic.recreate_background()
            w, h = state.resolution
            state.window.blit(state.background.image, (MENU_W, 0), (w + MENU_W, h, w - MENU_W, h))
            pygame.display.update((MENU_W, 0, w - MENU_W, h))

        locals()[BUTTON_NAMES[event.button]]()

    try:
        locals()[EVENT_NAMES[event.type]]()
    except KeyError:
        pass


def menu(event: pygame.event.Event):
    # click menu button
    def mouse_button_down():
        pos = state.mouse_pos
        for i, button in enumerate(state.buttons):
            rect = pygame.rect.Rect(CELL_SIZE / 2, CELL_SIZE / 2 + i * 30, state.menu.width - 10, 20)
            if rect.collidepoint(*pos):
                button.use()

                if state.highlighted_button_index != -1:
                    logic.render_button(state.highlighted_button_index)

                logic.render_button(i, GREEN)
                state.highlighted_button_index = i

                pygame.display.update()

                break

    try:
        locals()[EVENT_NAMES[event.type]]()
    except KeyError:
        pass


def draw(event: pygame.event.Event):
    def mouse_button_up():
        def button_left():
            w, h = state.resolution

            road = logic.create_road(drawing.start, state.coordinates)

            for rect in state.visible_roads:
                if road.colliderect(rect):
                    state.window.blit(state.background.image, road, road.move(w, h))
                    pygame.display.update(road)
                    drawing.prev = pygame.Rect(0, 0, 0, 0)
                    drawing.start = None
                    return

            state.roads.append(
                SimpleNamespace(startPoint=drawing.start, endPoint=state.coordinates, rect=road)
            )

            state.visible_roads.append(road)

            x, y = state.offset

            pygame.draw.rect(state.background.image, BLACK, road.move(w - x, h - y))
            pygame.draw.rect(state.window, BLACK, road.move(- x, - y))

            pygame.display.update(road.move(- x, - y))

            drawing.prev = pygame.Rect(0, 0, 0, 0)
            drawing.start = None

        locals()[BUTTON_NAMES[event.button]]()

    def mouse_button_down():
        def button_left():
            x, y = drawing.start = state.coordinates
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(state.window, WHITE, rect)
            pygame.display.update(rect)

        locals()[BUTTON_NAMES[event.button]]()

    def mouse_motion():
        if drawing.start and pygame.mouse.get_pressed(3)[0]:
            prev = drawing.prev

            state.window.blit(state.background.image, prev, area=prev.move(*state.resolution))
            pygame.display.update(prev)

            x, y = state.offset
            rect = logic.create_road(drawing.start, state.coordinates)

            color = WHITE
            for road in state.visible_roads:
                if road.colliderect(rect):
                    color = RED
                    break

            rect = rect.move(-x, -y)

            pygame.draw.rect(state.window, color, rect)
            pygame.display.update(rect)

            drawing.prev = rect

    try:
        locals()[EVENT_NAMES[event.type]]()
    except KeyError:
        pass


def select(event: pygame.event.Event):
    def mouse_motion():
        if state.selecting.prev.collidepoint(*event.pos):
            pygame.draw.rect(state.window, WHITE, state.selecting.prev, 1)
            pygame.display.update(state.selecting.prev)
            return

        prev_rect = state.selecting.prev

        state.window.blit(state.background.image, prev_rect, area=prev_rect.move(*state.resolution))
        pygame.display.update(prev_rect)

        state.selecting.prev = pygame.rect.Rect(0, 0, 0, 0)

        for road in state.visible_roads:
            if road.collidepoint(*event.pos):
                x, y = state.offset
                pygame.draw.rect(state.window, WHITE, road.move(-x, -y), 1)
                pygame.display.update(road.move(-x, -y))

                state.selecting.prev = road.move(-x, -y)

                break

    try:
        locals()[EVENT_NAMES[event.type]]()
    except KeyError:
        pass
