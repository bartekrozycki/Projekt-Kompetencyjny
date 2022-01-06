from types import SimpleNamespace

import pygame

from src import state, constants, logic


def menu_mouse_button_down(event: pygame.event.Event):
    for button in state.buttons:
        if button.rect.collidepoint(state.mouse_pos.x, state.mouse_pos.y):
            button.use()
            break


# drawing road
start = SimpleNamespace(x=0, y=0)
end = None
prev_rect = pygame.Rect(0, 0, 0, 0)


def board_mouse_button_up(event: pygame.event.Event):
    if event.button is not constants.MOUSE_LEFT_CLICKED:
        return
    global start, end, prev_rect

    road = SimpleNamespace(start=start, end=end, rect=prev_rect, draw=None)

    road.draw = lambda: (
        pygame.draw.rect(state.background.image, constants.BLACK, road.rect.move(*state.resolution))
    )
    road.draw()

    state.roads.append(road)
    end = None


def board_mouse_button_down(event: pygame.event.Event):
    if event.button is not constants.MOUSE_LEFT_CLICKED:
        return

    if not state.drawing:
        return

    global start, end

    start = SimpleNamespace(**state.coordinates.__dict__)
    end = SimpleNamespace(**state.coordinates.__dict__)
    rect = pygame.Rect(start.x * state.cell.size, start.y * state.cell.size, state.cell.size, state.cell.size)
    pygame.draw.rect(state.window, constants.BLACK, rect)
    pygame.display.update()


def board_mouse_motion(event: pygame.event.Event):
    global end, prev_rect

    if end is None or (end.x == state.coordinates.x and end.y == state.coordinates.y):
        return
    end = SimpleNamespace(**state.coordinates.__dict__)

    rect = logic.create_ver_hor_rectangle(start, end, state.cell.size)

    state.window.blit(state.background.image, prev_rect, area=prev_rect.move(*state.resolution))
    pygame.draw.rect(state.window, constants.BLACK, rect)
    pygame.display.update()
    prev_rect = rect


def handle_event(event: pygame.event.Event):
    try:
        if state.mouse_pos.x <= state.menu.width:
            {
                pygame.MOUSEBUTTONDOWN: menu_mouse_button_down,
            }[event.type](event)
        else:
            {
                pygame.MOUSEBUTTONDOWN: board_mouse_button_down,
                pygame.MOUSEBUTTONUP: board_mouse_button_up,
                pygame.MOUSEMOTION: board_mouse_motion,
            }[event.type](event)
    except KeyError:
        pass
