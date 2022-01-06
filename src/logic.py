from types import SimpleNamespace

import pygame

from src import constants, state


def create_background(x, y, color=constants.SKY_BLUE):
    res_w, res_h = state.resolution

    background = pygame.sprite.Sprite()
    background.rect = pygame.Rect(x, y, res_w * 3, res_h * 3)
    background.image = pygame.Surface(background.rect.size)

    background.image.fill(color)

    return background


def background_display_rectangle(x, y):
    res_w, res_h = state.resolution
    return pygame.rect.Rect(res_w + x, res_h + y, res_w - state.menu.width, res_h)


def create_button(function, text=""):
    button = SimpleNamespace(render=None, rect=pygame.rect.Rect(5, 5 + len(state.buttons) * 30, state.menu.width - 10, 20),
                             use=function, text=text)
    text_render = state.font_consolas.render(text, False, constants.BLACK)

    def update():
        pygame.draw.rect(state.window, constants.WHITE, button.rect)
        state.window.blit(text_render, button.rect)

    button.render = update
    update()
    state.buttons.append(button)


def mode_cursor():
    state.drawing = False


def mode_draw_single():
    state.drawing = True


def create_ver_hor_rectangle(start, end, thickness):
    diff_x = abs(end.x - start.x)
    diff_y = abs(end.y - start.y)
    if diff_x > diff_y:
        rect = pygame.Rect(start.x * thickness, start.y * thickness, thickness * diff_x,
                           thickness)
        if start.x > end.x:
            rect = rect.move(-diff_x * thickness, 0)
        else:
            rect.width += thickness
    else:
        rect = pygame.Rect(start.x * thickness, start.y * thickness, thickness,
                           thickness * diff_y)
        if start.y > end.y:
            rect = rect.move(0, -diff_y * thickness)
        else:
            rect.height += thickness

    return rect
