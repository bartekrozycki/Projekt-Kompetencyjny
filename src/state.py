from types import SimpleNamespace

import pygame

clock = pygame.time.Clock()

menu = SimpleNamespace(width=100)

resolution = None
window = None

# background: pygame.sprite.Sprite
background: pygame.Surface

roads: list[SimpleNamespace(connections=[], rect=None, start=[], end=[])] = []
visible_roads: list[SimpleNamespace(connections=[], rect=None, start=[], end=[])] = []
selected_roads: list[SimpleNamespace(connections=[], rect=None, start=[], end=[])] = []

select_mode = SimpleNamespace(prev=pygame.Rect(0, 0, 0, 0))
draw_mode = SimpleNamespace(start=None, prev=pygame.Rect(0, 0, 0, 0), p_lines=[])
moving = SimpleNamespace(on=False)

modes = {
    'select': True,
    'draw': False
}
selected_mode = 'select'
button_names = ['select', 'draw', 'clear']

mouse_pos = [0, 0]
coordinates = [0, 0]
offset = [0, 0]
offset_change = [0, 0]

font_consolas = None

cursor = SimpleNamespace(cur=None, prev=None)
prev_cursor_rect = None
