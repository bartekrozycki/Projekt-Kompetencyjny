from types import SimpleNamespace

import pygame

fps_limit = 60

menu = SimpleNamespace(width=100)

buttons = []
highlighted_button_index = 0

resolution = None
window = None

background: pygame.sprite.Sprite
bg_menu: pygame.sprite.Sprite

roads: list[pygame.Rect] = []
visible_roads: list[pygame.Rect] = []

clock = pygame.time.Clock()

selecting = SimpleNamespace(on=True)
drawing = SimpleNamespace(on=False, start_point=None, prev_rect=None)
moving = SimpleNamespace(on=True)

modes = [drawing, selecting]

mouse_pos = SimpleNamespace(x=0, y=0)
coordinates = [0, 0]
offset = [0, 0]

prev_coordinates = (0, 0)

font_consolas = None

prev_cursor_rect = None
