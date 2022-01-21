import pygame

SKY_BLUE = (135, 206, 250)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
D_YELLOW = (200, 200, 0)
D_GRAY = (70, 70, 90)
L_GRAY = (140, 140, 160)

MENU_W = 100
CELL_SIZE = 10

EVENT_NAMES = {
    pygame.MOUSEBUTTONUP: "mouse_button_up",
    pygame.MOUSEBUTTONDOWN: "mouse_button_down",
    pygame.MOUSEMOTION: "mouse_motion",
    pygame.VIDEORESIZE: "video_resize"
}
BUTTON_NAMES = {
    pygame.BUTTON_LEFT: "button_left",
    pygame.BUTTON_MIDDLE: "button_middle",
    pygame.BUTTON_WHEELUP: "button_wheelup",
    pygame.BUTTON_WHEELDOWN: "button_wheeldown",
    pygame.BUTTON_RIGHT: "button_right"
}

ROADS_FILENAME = "roads.data"
