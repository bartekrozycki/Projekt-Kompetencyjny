import pygame

from src import state, constants, logic
from src.constants import CELL_SIZE, BLACK, EVENT_NAMES, BUTTON_NAMES
from src.state import drawing, coordinates


def window(event: pygame.event.Event):
    def mouse_motion():
        state.mouse_pos.x = event.pos[0]
        state.mouse_pos.y = event.pos[1]

        state.prev_coordinates = state.coordinates
        state.coordinates = [c // CELL_SIZE for c in event.pos]

        if state.mouse_pos.x > state.menu.width:
            logic.render_cursor()

            if state.coordinates != state.prev_coordinates and pygame.mouse.get_pressed(3)[1]:
                coor = state.coordinates
                prev = state.prev_coordinates

                state.offset = [(-coor[i] + prev[i]) * CELL_SIZE for i in range(2)]

                state.prev_coordinates = state.coordinates

                res_w, res_h = state.resolution
                state.window.blit(state.background.image, (100, 0),
                                  area=(left + 2 * res_w + 100, top + 2 * res_h, res_w - 100, res_h))

                pygame.display.update()

    def video_resize():
        state.resolution = event.size
        state.background = logic.recreate_background(*state.background.rect.topleft)  # create background

        res_w, res_h = state.resolution
        state.window.blit(state.background.image, (100, 0), area=(res_w + 100, res_h, res_w - 100, res_h))

        state.bg_menu = logic.recreate_menu()

        pygame.display.update()

    try:
        locals()[EVENT_NAMES[event.type]]()
    except KeyError:
        pass


def menu(event: pygame.event.Event):
    def mouse_button_down():
        for i, button in enumerate(state.buttons):
            rect = pygame.rect.Rect(CELL_SIZE / 2, CELL_SIZE / 2 + i * 30, state.menu.width - 10, 20)
            if rect.collidepoint(state.mouse_pos.x, state.mouse_pos.y):
                button.use()

                if state.highlighted_button_index != -1:
                    logic.render_button(state.highlighted_button_index)

                logic.render_button(i, constants.GREEN)
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
            start = drawing.start_point
            x, y = coordinates
            res_w, res_h = state.resolution
            left, top = state.background.rect.topleft
            x1, y1 = start[0] + (left + res_w) // CELL_SIZE, start[1] + (top + res_h) // CELL_SIZE
            x2, y2 = x + (left + res_w) // CELL_SIZE, y + (top + res_h) // CELL_SIZE
            road = logic.create_ver_hor_rectangle((x1, y1), (x2, y2), CELL_SIZE)
            state.roads.append(road)
            state.visible_roads.append(road)

            pygame.draw.rect(state.background.image, BLACK, road.move(res_w, res_h))
            state.window.blit(state.background.image, (100, 0),
                              area=(left + 2 * res_w + 100, top + 2 * res_h, res_w - 100, res_h))

            pygame.display.update()

            drawing.prev_rect = None

        def button_middle():
            state.moving = False
            state.background = logic.recreate_background(*state.background.rect.topleft)
            state.prev_coordinates = coordinates

        locals()[BUTTON_NAMES[event.button]]()

    def mouse_button_down():
        def button_left():
            x, y = drawing.start_point = coordinates
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(state.window, constants.WHITE, rect)
            pygame.display.update(rect)

        def button_middle():
            state.prev_coordinates = coordinates
            state.moving = True

        locals()[BUTTON_NAMES[event.button]]()

    def mouse_motion():
        if drawing.start_point and pygame.mouse.get_pressed(3)[0]:
            x, y = coordinates

            if drawing.prev_rect:
                state.window.blit(state.background.image, drawing.prev_rect,
                                  area=drawing.prev_rect.move(*state.resolution))
                pygame.display.update(drawing.prev_rect)

            rect = logic.create_ver_hor_rectangle(drawing.start_point, (x, y), CELL_SIZE)
            pygame.draw.rect(state.window, constants.WHITE, rect)

            pygame.display.update(rect)

            drawing.prev_rect = rect

    try:
        locals()[EVENT_NAMES[event.type]]()
    except KeyError:
        pass
