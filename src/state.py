from types import SimpleNamespace

import pygame

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
drawing = SimpleNamespace(on=False, start=None, prev=pygame.Rect(0, 0, 0, 0))

modes = [drawing, selecting]

mouse_pos = [0, 0]
coordinates = [0, 0]
offset = [0, 0]
offset_change = [0, 0]

font_consolas = None

cursor = SimpleNamespace(cur=None, prev=None)
prev_cursor_rect = None
