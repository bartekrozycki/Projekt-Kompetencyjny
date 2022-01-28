import pygame

D_GREY = (50, 50, 50)
L_GREY = (169, 183, 198)
LL_GREY = (192, 197, 206)



BLACK = (0, 0, 0)
BLUE = (83, 148, 236)
CYAN = (41, 153, 153)
GRAY = (85, 85, 85)
GREEN = (55, 156, 26)
MAGENTA = (174, 138, 190)
RED = (231, 70, 68)
WHITE = (238, 238, 238)
YELLOW = (220, 196, 87)

MENU_W = 100
CELL_SIZE = 20
BUTTON_H = 20
BUTTON_GAP_H = 10
BUTTON_GAP_V = 5

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
