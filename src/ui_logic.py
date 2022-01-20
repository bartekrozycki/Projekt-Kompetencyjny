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
                clicked_button = button

                clicked_button.use()

                if state.highlighted_button_index != -1 and clicked_button.activable:
                    logic.render_button(state.highlighted_button_index)
                    state.highlighted_button_index = i

                if clicked_button.activable:
                    logic.render_button(i, GREEN)


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

            x, y = state.offset

            for v_road in state.visible_roads:
                if road.rect.colliderect(v_road.rect):
                    state.window.blit(state.background.image, road.rect.move(-x, -y), road.rect.move(w - x, h - y))
                    pygame.display.update(road.rect.move(-x, -y))
                    drawing.prev = pygame.Rect(0, 0, 0, 0)
                    drawing.start = None
                    return

            state.roads.append(road)

            state.visible_roads.append(road)


            pygame.draw.rect(state.background.image, BLACK, road.rect.move(w - x, h - y))
            pygame.draw.rect(state.window, BLACK, road.rect.move(- x, - y))

            pygame.display.update(road.rect.move(- x, - y))

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
            road = logic.create_road(drawing.start, state.coordinates)

            color = WHITE
            for v_road in state.visible_roads:
                if v_road.rect.colliderect(road.rect):
                    color = RED
                    break

            road.rect = road.rect.move(-x, -y)

            pygame.draw.rect(state.window, color, road.rect)
            pygame.display.update(road.rect)

            drawing.prev = road.rect

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

        ox, oy = state.offset
        x, y = event.pos

        for v_road in state.visible_roads:
            if v_road.rect.collidepoint(x + ox, y + oy):
                pygame.draw.rect(state.window, WHITE, v_road.rect.move(-ox, -oy), 1)
                pygame.display.update(v_road.rect.move(-ox, -oy))

                state.selecting.prev = v_road.rect.move(-ox, -oy)

                break

    try:
        locals()[EVENT_NAMES[event.type]]()
    except KeyError:
        pass
