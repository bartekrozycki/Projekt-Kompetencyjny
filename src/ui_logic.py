import pygame

from src import state, logic
from src.constants import *


def window(event: pygame.event.Event):
    ox, oy = state.offset
    w, h = state.resolution
    cx, cy = state.coordinates

    # manages display while moving
    def mouse_motion():
        x, y = state.mouse_pos = event.pos
        cx2, cy2 = x // CELL_SIZE, y // CELL_SIZE
        # move and display
        if state.window.moving and (cx != cx2 or cy != cy2):
            dx, dy = (cx - cx2) * CELL_SIZE, (cy - cy2) * CELL_SIZE
            state.offset = ox + dx, oy + dy
            state.window.area.move_ip(dx, dy)

            state.display.blit(state.background, (MENU_W, 0), state.window.area)
            pygame.display.update((MENU_W, 0, w - MENU_W, h))

        state.coordinates = [cx2, cy2]

    def video_resize():
        state.resolution = event.size
        logic.create_background()

        logic.draw_buttons()
        logic.update_workspace()

    def mouse_button_up():
        def button_middle():
            logic.create_background()
            state.window.moving = False

        locals()[BUTTON_NAMES[event.button]]()

    def mouse_button_down():
        def button_middle():
            x, y = event.pos
            if x > MENU_W:
                state.window.area = logic.get_workspace_rect()
                state.window.moving = True

        locals()[BUTTON_NAMES[event.button]]()

    try:
        locals()[EVENT_NAMES[event.type]]()
    except KeyError:
        pass


def menu(event: pygame.event.Event):
    # click menu button
    def mouse_button_down():
        def button_left():
            x, y = event.pos
            if not (BUTTON_GAP_V < x < MENU_W - BUTTON_GAP_V):
                return
            if not (BUTTON_GAP_H < y % (BUTTON_GAP_H + BUTTON_H)):
                return

            try:
                logic.press_button(state.button_names[y // (BUTTON_H + BUTTON_GAP_H)])
            except IndexError:
                pass

        locals()[BUTTON_NAMES[event.button]]()

    try:
        locals()[EVENT_NAMES[event.type]]()
    except KeyError:
        pass


def draw(event: pygame.event.Event):
    ox, oy = state.offset
    w, h = state.resolution
    cx, cy = state.coordinates

    def mouse_button_up():
        def button_left():
            road = logic.create_road(state.draw_mode.start, state.coordinates)

            # check if new road collide with existing visible roads and remove it
            for v_road in state.visible_roads:
                if road.rect.colliderect(v_road.rect):
                    state.display.blit(state.background, road.rect.move(-ox, -oy), road.rect.move(w - ox, h - oy))
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
            pygame.draw.rect(state.display, BLACK, road.rect.move(- ox, - oy))
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
            pygame.draw.rect(state.display, BLACK, rect, 1)
            pygame.display.update(rect)

        locals()[BUTTON_NAMES[event.button]]()

    def mouse_motion():
        for line in state.draw_mode.p_lines:
            state.display.blit(state.background, line, area=line.move(*state.resolution))
        pygame.display.update(state.draw_mode.p_lines)

        lines = [pygame.Rect(MENU_W, cy * CELL_SIZE, w - MENU_W, 1),
                 pygame.Rect(MENU_W, (cy + 1) * CELL_SIZE - 1, w - MENU_W, 1), pygame.Rect(cx * CELL_SIZE, 0, 1, h),
                 pygame.Rect((cx + 1) * CELL_SIZE - 1, 0, 1, h)]

        for line in lines:
            pygame.draw.rect(state.display, GRAY, line)

        pygame.display.update(lines)
        state.draw_mode.p_lines = lines

        if not state.draw_mode.start or not pygame.mouse.get_pressed(3)[0]:
            return

        prev = state.draw_mode.prev

        state.display.blit(state.background, prev, area=prev.move(*state.resolution))

        pygame.display.update([prev])

        road = logic.create_road(state.draw_mode.start, state.coordinates)

        color = L_GREY
        for v_road in state.visible_roads:
            if v_road.rect.colliderect(road.rect):
                color = RED
                break

        road.rect = road.rect.move(-ox, -oy)

        pygame.draw.rect(state.display, color, road.rect)

        pygame.display.update([road.rect])

        state.draw_mode.prev = road.rect

    try:
        locals()[EVENT_NAMES[event.type]]()
    except KeyError:
        pass


def select(event: pygame.event.Event):
    ox, oy = state.offset
    w, h = state.resolution
    cx, cy = state.coordinates
    x, y = ox + cx * CELL_SIZE, oy + cy * CELL_SIZE

    def mouse_button_down():
        def button_left():
            for s_road in state.selected_roads:
                if s_road.rect.collidepoint(x, y):
                    pygame.display.update(logic.draw_road(s_road))
                    logic.draw_road_on_bg(s_road)
                    state.selected_roads.remove(s_road)
                    return

            for v_road in state.visible_roads:
                if v_road not in state.selected_roads and v_road.rect.collidepoint(x, y):
                    rect = logic.draw_road(v_road, L_GREY)
                    logic.draw_road_start_end(v_road)
                    pygame.display.update(rect)
                    logic.draw_road_on_bg(v_road, L_GREY, 1)
                    logic.draw_road_start_end_on_bg(v_road)
                    state.selected_roads.append(v_road)
                    return

            for s_road in state.selected_roads:
                pygame.draw.rect(state.display, BLACK, s_road.rect.move(-ox, -oy))
                pygame.draw.rect(state.background, BLACK, s_road.rect.move(w - ox, h - oy))
                pygame.display.update(s_road.rect.move(-ox, -oy))

            state.selected_roads = []

        def button_right():
            for s_road in state.selected_roads:
                if s_road.rect.collidepoint(x, y):
                    for road in state.selected_roads:
                        pygame.draw.rect(state.display, D_GREY, road.rect.move(-ox, -oy))
                        pygame.draw.rect(state.background, D_GREY, road.rect.move(w - ox, h - oy))
                        pygame.display.update(road.rect.move(-ox, -oy))
                        state.roads.remove(road)
                        state.visible_roads.remove(road)

                    state.selected_roads = []
                    return

            for v_road in state.visible_roads:
                if v_road.rect.collidepoint(x, y):
                    pygame.draw.rect(state.display, D_GREY, v_road.rect.move(-ox, -oy))
                    pygame.draw.rect(state.background, D_GREY, v_road.rect.move(w - ox, h - oy))
                    pygame.display.update(v_road.rect.move(-ox, -oy))
                    state.roads.remove(v_road)
                    state.visible_roads.remove(v_road)
                    return

        locals()[BUTTON_NAMES[event.button]]()

    def mouse_motion():
        hovered = state.select.hovered

        if hovered.collidepoint(x, y):
            return
        else:
            logic.draw_bg(hovered)
            pygame.display.update(hovered)

            state.select.hovered = pygame.Rect(0, 0, 0, 0)
            for s_road in state.selected_roads:
                logic.draw_bg(s_road.rect.move(-ox, -oy))
                pygame.display.update(s_road.rect.move(-ox, -oy))

        for s_road in state.selected_roads:
            if s_road.rect.collidepoint(x, y):
                for road in state.selected_roads:
                    rect = logic.draw_road(road, L_GREY)
                    logic.draw_road_start_end(road)
                    pygame.display.update(rect)

                state.select.hovered = logic.get_fitted_road_rect(s_road)
                return

        for v_road in state.visible_roads:
            if v_road.rect.collidepoint(x, y):
                rect = logic.draw_road(v_road, L_GREY)
                logic.draw_road_start_end(v_road)

                pygame.display.update(rect)
                state.select.hovered = rect
                break

    try:
        locals()[EVENT_NAMES[event.type]]()
    except KeyError:
        pass


def connect(event: pygame.event.Event):
    ox, oy = state.offset

    def mouse_button_down():
        def button_left():
            if state.connect.hovered:
                state.connect.start = state.connect.hovered.end_rect.move(-ox, -oy).center

        locals()[BUTTON_NAMES[event.button]]()

    def mouse_button_up():
        def button_left():
            for v_road in state.visible_roads:
                if v_road is not state.connect.hovered and v_road.start_rect.move(-ox, -oy).collidepoint(*event.pos):
                    if v_road.start in state.connect.hovered.connections:
                        break
                    hx, hy = state.connect.hovered.end
                    if state.connect.hovered.rect.top != hy * CELL_SIZE:
                        hy += 1
                    if state.connect.hovered.rect.left != hx * CELL_SIZE:
                        hx += 1

                    vx, vy = v_road.start
                    # if state.connect.hovered.rect.top < v_road.rect.top:
                    #     vy += 1
                    if state.connect.hovered.rect.left != hx * CELL_SIZE:
                        vx += 1

                    if state.connect.hovered.vertical:
                        rect = pygame.Rect(hx * CELL_SIZE, hy * CELL_SIZE, CELL_SIZE, (vy - hy) * CELL_SIZE)
                        pygame.draw.rect(state.display, WHITE, rect, 1)
                        rect2 = pygame.Rect(hx * CELL_SIZE, v_road.rect.move(-ox, -oy).top, (vx - hx) * CELL_SIZE,
                                            CELL_SIZE)
                        pygame.draw.rect(state.display, WHITE, rect2, 1)
                    else:
                        rect = pygame.Rect(hx * CELL_SIZE, state.connect.hovered.rect.top, (vx - hx) * CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(state.display, WHITE, rect, 1)
                        rect2 = pygame.Rect(v_road.rect.move(-ox, -oy).left, hy * CELL_SIZE, CELL_SIZE, (vy - hy) * CELL_SIZE)
                        pygame.draw.rect(state.display, WHITE, rect2, 1)
                    # state.connect.hovered.connections.append(v_road.start)
                    break
            state.connect.start = None
            state.connect.prev = pygame.Rect(0, 0, 0, 0)
            # logic.draw_bg()
            pygame.display.update()

        locals()[BUTTON_NAMES[event.button]]()

    def mouse_motion():
        if state.connect.start:
            logic.draw_bg(state.connect.erase)
            pygame.display.update(state.connect.erase)

            rect = pygame.draw.line(state.display, WHITE, state.connect.start, event.pos)
            pygame.display.update(rect)
            state.connect.erase = rect

        if state.connect.prev.collidepoint(*event.pos):
            return

        for v_road in state.visible_roads:
            if v_road.end_rect.move(-ox, -oy).collidepoint(*event.pos):
                # pygame.draw.rect(state.display, WHITE, v_road.end_rect.move(-ox, -oy), 1)
                # pygame.display.update(v_road.end_rect.move(-ox, -oy))
                # state.connect.prev = v_road.end_rect.move(-ox, -oy)
                state.connect.hovered = v_road
                break

    try:
        locals()[EVENT_NAMES[event.type]]()
    except KeyError:
        pass
