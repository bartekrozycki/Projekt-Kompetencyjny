import pygame

from src import state, logic
from src.constants import CELL_SIZE, EVENT_NAMES, MENU_W, BUTTON_NAMES, BLACK, WHITE, GREEN, RED, YELLOW, D_YELLOW, \
    SKY_BLUE, D_GRAY
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
        if pos[0] > state.menu.width and coor != prev_coor and not state.moving.on:
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

            state.moving.on = True

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

            state.moving.on = False

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
    ox, oy = state.offset
    w, h = state.resolution
    x, y = state.mouse_pos

    def mouse_button_up():
        def button_left():

            p_line = drawing.p_line

            state.window.blit(state.background.image, p_line, area=p_line.move(*state.resolution))
            pygame.display.update([p_line])

            road = logic.create_road(drawing.start, state.coordinates)

            # check if new road collide with existing visible roads and remove it
            for v_road in state.visible_roads:
                if road.rect.colliderect(v_road.rect):
                    state.window.blit(state.background.image, road.rect.move(-ox, -oy), road.rect.move(w - ox, h - oy))
                    pygame.display.update(road.rect.move(-ox, -oy))
                    drawing.prev = pygame.Rect(0, 0, 0, 0)
                    drawing.start = None
                    return

            state.roads.append(road)
            state.visible_roads.append(road)

            # draw road with actual map position offset and update this part of screen
            pygame.draw.rect(state.background.image, BLACK, road.rect.move(w - ox, h - oy))
            pygame.draw.rect(state.window, BLACK, road.rect.move(- ox, - oy))
            pygame.display.update(road.rect.move(- ox, - oy))

            # clear variables used in process
            drawing.prev = pygame.Rect(0, 0, 0, 0)
            drawing.p_line = pygame.Rect(0, 0, 0, 0)
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
            p_line = drawing.p_line

            state.window.blit(state.background.image, prev, area=prev.move(*state.resolution))
            state.window.blit(state.background.image, p_line, area=p_line.move(*state.resolution))
            pygame.display.update([prev, p_line])

            road = logic.create_road(drawing.start, state.coordinates)

            color = WHITE
            for v_road in state.visible_roads:
                if v_road.rect.colliderect(road.rect):
                    color = RED
                    break

            road.rect = road.rect.move(-ox, -oy)

            if road.rect.height != CELL_SIZE:
                height = road.rect.top - oy
                if road.rect.top - oy < y - y % 10:
                    height += road.rect.height
                line = pygame.Rect(state.menu.width, height, w - state.menu.width, 1)
            elif road.rect.width != CELL_SIZE:
                width = road.rect.left - ox
                if road.rect.left - ox < x - x % 10:
                    width += road.rect.width
                line = pygame.Rect(width, 0, 1, h)
            else:
                line = pygame.Rect(0, 0, 0, 0)

            print(road.rect.width)

            pygame.draw.rect(state.window, color, road.rect)
            pygame.draw.rect(state.window, color, line)
            pygame.display.update([road.rect, line])

            drawing.prev = road.rect
            drawing.p_line = line

    try:
        locals()[EVENT_NAMES[event.type]]()
    except KeyError:
        pass


def select(event: pygame.event.Event):
    ox, oy = state.offset
    x, y = state.mouse_pos
    w, h = state.resolution

    def mouse_button_down():
        def button_left():
            for v_road in state.visible_roads:
                if v_road.rect.collidepoint(x + ox, y + oy):
                    pygame.draw.rect(state.window, YELLOW, v_road.rect.move(-ox, -oy))
                    for s_road in state.selected_roads:
                        pygame.draw.rect(state.window, YELLOW, s_road.rect.move(-ox, -oy))
                        pygame.display.update(s_road.rect.move(-ox, -oy))
                    pygame.draw.rect(state.background.image, YELLOW, v_road.rect.move(w - ox, h - oy), 1)
                    pygame.display.update(v_road.rect.move(-ox, -oy))

                    state.selected_roads.append(v_road)
                    return

            for s_road in state.selected_roads:
                pygame.draw.rect(state.window, BLACK, s_road.rect.move(-ox, -oy))
                pygame.draw.rect(state.background.image, BLACK, s_road.rect.move(w - ox, h - oy))
                pygame.display.update(s_road.rect.move(-ox, -oy))

            state.selected_roads = []

        def button_right():
            for s_road in state.selected_roads:
                if s_road.rect.collidepoint(x, y):
                    for road in state.selected_roads:
                        pygame.draw.rect(state.window, D_GRAY, road.rect.move(-ox, -oy))
                        pygame.draw.rect(state.background.image, D_GRAY, road.rect.move(w - ox, h - oy))
                        pygame.display.update(road.rect.move(-ox, -oy))
                        state.roads.remove(road)
                        state.visible_roads.remove(road)

                    state.selected_roads = []
                    return

            for v_road in state.visible_roads:
                if v_road.rect.collidepoint(x, y):
                    pygame.draw.rect(state.window, D_GRAY, v_road.rect.move(-ox, -oy))
                    pygame.draw.rect(state.background.image, D_GRAY, v_road.rect.move(w - ox, h - oy))
                    pygame.display.update(v_road.rect.move(-ox, -oy))
                    state.roads.remove(v_road)
                    state.visible_roads.remove(v_road)
                    state.selecting.prev = pygame.rect.Rect(0, 0, 0, 0)
                    return

        locals()[BUTTON_NAMES[event.button]]()

    def mouse_motion():

        for s_road in state.selected_roads:
            if s_road.rect.collidepoint(x, y):
                for road in state.selected_roads:
                    pygame.draw.rect(state.window, YELLOW, road.rect.move(-ox, -oy))
                    pygame.display.update(road.rect.move(-ox, -oy))
                return

        for s_road in state.selected_roads:
            state.window.blit(state.background.image, s_road.rect.move(-ox, -oy), area=s_road.rect.move(w - ox, h - oy))
            pygame.display.update(s_road.rect.move(-ox, -oy))

        if state.selecting.prev.collidepoint(x, y):
            pygame.draw.rect(state.window, WHITE, state.selecting.prev, 1)
            pygame.display.update(state.selecting.prev)
            return

        prev_rect = state.selecting.prev

        state.window.blit(state.background.image, prev_rect, area=prev_rect.move(*state.resolution))
        pygame.display.update(prev_rect)

        state.selecting.prev = pygame.rect.Rect(0, 0, 0, 0)

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
