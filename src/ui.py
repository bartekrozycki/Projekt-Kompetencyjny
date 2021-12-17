from types import SimpleNamespace

import pygame

import src.constants
from src import state


def menu_mouse_button_down(event: pygame.event.Event):
    for button in state.buttons:
        if button.rect.collidepoint(state.mouse_pos.x, state.mouse_pos.y):
            button.use()
            break


# drawing road
start = None
end = None

def board_mouse_button_up(event: pygame.event.Event):
    global end
    end = None


def board_mouse_button_down(event: pygame.event.Event):
    global start, end
    start = SimpleNamespace(**state.coordinates.__dict__)
    end = SimpleNamespace(**state.coordinates.__dict__)


def board_mouse_motion(event: pygame.event.Event):
    global end

    if end is None or (end.x == state.coordinates.x and end.y == state.coordinates.y):
        return
    end = SimpleNamespace(**state.coordinates.__dict__)

    diff = end.x - start.x
    rect = (end.x * state.cell.size, end.y * state.cell.size, state.cell.size)
    pygame.draw.rect(state.window, src.constants.BLACK, ())


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
