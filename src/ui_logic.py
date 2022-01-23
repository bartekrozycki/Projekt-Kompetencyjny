from src import state, logic
from src.constants import *


def window(event: pygame.event.Event):
    # manages display while moving and cursor display
    def mouse_motion():
        prev_pos = state.mouse_pos
        pos = event.pos
        coor = [c // CELL_SIZE for c in pos]

        # move and display
        if pos[0] > state.menu.width and pygame.mouse.get_pressed(3)[1]:
            state.offset_change = [(state.offset_change[i] + prev_pos[i] - pos[i]) for i in range(2)]
            x, y = state.offset_change
            x = x - x % CELL_SIZE
            y = y - y % CELL_SIZE
            w, h = state.resolution
            state.window.blit(state.background, (MENU_W, 0), area=(w + MENU_W + x, h + y, w - MENU_W, h))

            pygame.display.update((MENU_W, 0, w - MENU_W, h))

            state.moving.on = True

        state.mouse_pos = pos
        state.coordinates = coor

    def video_resize():
        state.resolution = event.size
        state.background = logic.create_background()  # create background

        res_w, res_h = state.resolution
        state.window.blit(state.background, (100, 0), area=(res_w + 100, res_h, res_w - 100, res_h))

        pygame.display.update()

    def mouse_button_up():
        def button_middle():
            x, y = state.offset_change
            state.offset_change = [x - x % CELL_SIZE, y - y % CELL_SIZE]
            state.offset = [state.offset[i] + state.offset_change[i] for i in range(2)]
            state.offset_change = [0, 0]
            state.background = logic.create_background()
            w, h = state.resolution
            state.window.blit(state.background, (MENU_W, 0), (w + MENU_W, h, w - MENU_W, h))
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
        x, y = state.mouse_pos
        if not (BUTTON_GAP_V < x < MENU_W - BUTTON_GAP_V):
            return
        if not (BUTTON_GAP_H < y % (BUTTON_GAP_H + BUTTON_H)):
            return

        try:
            logic.press_button(state.button_names[y // (BUTTON_H + BUTTON_GAP_H)])
        except IndexError:
            pass

    try:
        locals()[EVENT_NAMES[event.type]]()
    except KeyError:
        pass


def draw(event: pygame.event.Event):
    ox, oy = state.offset
    w, h = state.resolution
    x, y = state.mouse_pos
    cx, cy = state.coordinates

    def mouse_button_up():
        def button_left():
            road = logic.create_road(state.draw_mode.start, state.coordinates)

            # check if new road collide with existing visible roads and remove it
            for v_road in state.visible_roads:
                if road.rect.colliderect(v_road.rect):
                    state.window.blit(state.background, road.rect.move(-ox, -oy), road.rect.move(w - ox, h - oy))
                    pygame.display.update(road.rect.move(-ox, -oy))
                    state.draw_mode.prev = pygame.Rect(0, 0, 0, 0)
                    state.draw_mode.start = None
                    return

            inflated_h = road.rect.inflate(CELL_SIZE, 0)
            inflated_v = road.rect.inflate(0, CELL_SIZE)

            neighbours = []
            count_h = count_v = 0

            for v_road in state.visible_roads:
                if road.rect.h == CELL_SIZE and v_road.rect.h == CELL_SIZE and inflated_h.colliderect(v_road.rect):
                    neighbours.append(v_road)
                    count_h += 1

                if road.rect.w == CELL_SIZE and v_road.rect.w == CELL_SIZE and inflated_v.colliderect(v_road.rect):
                    neighbours.append(v_road)
                    count_v += 1

            for n_road in neighbours:
                if n_road.rect.top == road.rect.top and n_road.rect.h == CELL_SIZE and count_h >= count_v:
                    n_road.rect.width += road.rect.width
                    if n_road.rect.left > road.rect.left:
                        n_road.rect.left = road.rect.left
                        n_road.start = road.start if road.start[0] < road.end[0] else road.end
                    else:
                        n_road.end = road.end if road.start[0] < road.end[0] else road.start
                    road = n_road
                    state.roads.remove(n_road)
                    state.visible_roads.remove(n_road)
                if n_road.rect.left == road.rect.left and n_road.rect.w == CELL_SIZE and count_h < count_v:
                    n_road.rect.height += road.rect.height
                    if n_road.rect.top > road.rect.top:
                        n_road.rect.top = road.rect.top
                        n_road.start = road.start if road.start[0] < road.end[0] else road.end
                    else:
                        n_road.end = road.end if road.start[0] < road.end[0] else road.start
                    road = n_road
                    state.roads.remove(n_road)
                    state.visible_roads.remove(n_road)

            state.roads.append(road)
            state.visible_roads.append(road)

            # draw road with actual map position offset and update this part of screen
            pygame.draw.rect(state.background, BLACK, road.rect.move(w - ox, h - oy))
            pygame.draw.rect(state.window, BLACK, road.rect.move(- ox, - oy))
            pygame.display.update(road.rect.move(- ox, - oy))

            # clear variables used in process
            state.draw_mode.prev = pygame.Rect(0, 0, 0, 0)
            state.draw_mode.p_line = pygame.Rect(0, 0, 0, 0)
            state.draw_mode.start = None

        locals()[BUTTON_NAMES[event.button]]()

    def mouse_button_down():
        def button_left():
            x, y = state.draw_mode.start = state.coordinates
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(state.window, WHITE, rect)
            pygame.display.update(rect)

        locals()[BUTTON_NAMES[event.button]]()

    def mouse_motion():
        for line in state.draw_mode.p_lines:
            state.window.blit(state.background, line, area=line.move(*state.resolution))
        pygame.display.update(state.draw_mode.p_lines)

        lines = []
        lines.append(pygame.Rect(state.menu.width, cy * CELL_SIZE, w - state.menu.width, 1))
        lines.append(pygame.Rect(state.menu.width, (cy + 1) * CELL_SIZE - 1, w - state.menu.width, 1))
        lines.append(pygame.Rect(cx * CELL_SIZE, 0, 1, h))
        lines.append(pygame.Rect((cx + 1) * CELL_SIZE - 1, 0, 1, h))

        for line in lines:
            pygame.draw.rect(state.window, L_GRAY, line)

        pygame.display.update(lines)
        state.draw_mode.p_lines = lines

        if state.draw_mode.start and pygame.mouse.get_pressed(3)[0]:
            prev = state.draw_mode.prev

            state.window.blit(state.background, prev, area=prev.move(*state.resolution))

            pygame.display.update([prev])

            road = logic.create_road(state.draw_mode.start, state.coordinates)

            color = WHITE
            for v_road in state.visible_roads:
                if v_road.rect.colliderect(road.rect):
                    color = RED
                    break

            road.rect = road.rect.move(-ox, -oy)

            pygame.draw.rect(state.window, color, road.rect)

            pygame.display.update([road.rect])

            state.draw_mode.prev = road.rect

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
                    pygame.draw.rect(state.background, YELLOW, v_road.rect.move(w - ox, h - oy), 1)
                    pygame.display.update(v_road.rect.move(-ox, -oy))

                    state.selected_roads.append(v_road)
                    return

            for s_road in state.selected_roads:
                pygame.draw.rect(state.window, BLACK, s_road.rect.move(-ox, -oy))
                pygame.draw.rect(state.background, BLACK, s_road.rect.move(w - ox, h - oy))
                pygame.display.update(s_road.rect.move(-ox, -oy))

            state.selected_roads = []

        def button_right():
            for s_road in state.selected_roads:
                if s_road.rect.move(-ox, -oy).collidepoint(x, y):
                    for road in state.selected_roads:
                        pygame.draw.rect(state.window, D_GRAY, road.rect.move(-ox, -oy))
                        pygame.draw.rect(state.background, D_GRAY, road.rect.move(w - ox, h - oy))
                        pygame.display.update(road.rect.move(-ox, -oy))
                        state.roads.remove(road)
                        state.visible_roads.remove(road)

                    state.selected_roads = []
                    return

            for v_road in state.visible_roads:
                if v_road.rect.move(-ox, -oy).collidepoint(x, y):
                    pygame.draw.rect(state.window, D_GRAY, v_road.rect.move(-ox, -oy))
                    pygame.draw.rect(state.background, D_GRAY, v_road.rect.move(w - ox, h - oy))
                    pygame.display.update(v_road.rect.move(-ox, -oy))
                    state.roads.remove(v_road)
                    state.visible_roads.remove(v_road)
                    state.select_mode.prev = pygame.rect.Rect(0, 0, 0, 0)
                    return

        locals()[BUTTON_NAMES[event.button]]()

    def mouse_motion():
        prev_rect = state.select_mode.prev

        state.window.blit(state.background, prev_rect, area=prev_rect.move(*state.resolution))
        pygame.display.update(prev_rect)

        for v_road in state.visible_roads:
            if v_road.rect.collidepoint(x + ox, y + oy):
                pygame.draw.rect(state.window, WHITE, v_road.rect.move(-ox, -oy), 1)
                sx, sy = v_road.start
                sx = sx * CELL_SIZE - ox
                sy = sy * CELL_SIZE - oy
                ex, ey = v_road.end
                ex = ex * CELL_SIZE - ox
                ey = ey * CELL_SIZE - oy

                if ex < sx:
                    ex -= CELL_SIZE // 2
                    sx += CELL_SIZE // 2

                if ey < sy:
                    ey -= CELL_SIZE // 2
                    sy += CELL_SIZE // 2

                if v_road.rect.h == CELL_SIZE:
                    pygame.draw.rect(state.window, GREEN, (sx, sy, CELL_SIZE // 2, CELL_SIZE))
                    pygame.draw.rect(state.window, RED, (ex + CELL_SIZE // 2, ey, CELL_SIZE // 2, CELL_SIZE))
                else:
                    pygame.draw.rect(state.window, GREEN, (sx, sy, CELL_SIZE, CELL_SIZE // 2))
                    pygame.draw.rect(state.window, RED, (ex, ey + CELL_SIZE // 2, CELL_SIZE, CELL_SIZE // 2))

                pygame.display.update(v_road.rect.move(-ox, -oy))
                state.select_mode.prev = v_road.rect.move(-ox, -oy)

                break

        for s_road in state.selected_roads:
            if s_road.rect.collidepoint(x + ox, y + oy):
                for road in state.selected_roads:
                    pygame.draw.rect(state.window, YELLOW, road.rect.move(-ox, -oy))
                    pygame.display.update(road.rect.move(-ox, -oy))
                return

        for s_road in state.selected_roads:
            state.window.blit(state.background, s_road.rect.move(-ox, -oy), area=s_road.rect.move(w - ox, h - oy))
            pygame.display.update(s_road.rect.move(-ox, -oy))

        if state.select_mode.prev.collidepoint(x, y):
            pygame.draw.rect(state.window, WHITE, state.select_mode.prev, 1)
            pygame.display.update(state.select_mode.prev)
            return

        state.select_mode.prev = pygame.rect.Rect(0, 0, 0, 0)



    try:
        locals()[EVENT_NAMES[event.type]]()
    except KeyError:
        pass
