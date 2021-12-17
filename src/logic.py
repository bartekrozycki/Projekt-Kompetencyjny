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


def create_button(function):
    button = SimpleNamespace(rect=pygame.rect.Rect(5, 5 + len(state.buttons) * 30, state.menu.width - 10, 20), use=function)
    pygame.draw.rect(state.window, constants.WHITE, button.rect)
    state.buttons.append(button)

def mode_cursor():
    state.background = create_background(*state.background.rect.topleft, constants.RED)
    state.window.blit(state.background.image, (state.menu.width, 0), background_display_rectangle(0, 0))
    pygame.display.update()

def mode_draw_single():
    state.background = create_background(*state.background.rect.topleft, constants.SKY_BLUE)
    state.window.blit(state.background.image, (state.menu.width, 0), background_display_rectangle(0, 0))
    pygame.display.update()
