from types import SimpleNamespace

import pygame
from dataclasses import dataclass


@dataclass
class Road:
    connections: list[list[int, int]]
    rect: pygame.Rect
    start: list[int, int]
    end: list[int, int]


@dataclass
class Window:
    moving: bool
    area: pygame.Rect


@dataclass
class Select:
    hovered: pygame.Rect


resolution: tuple[int, int]
display: pygame.Surface
background: pygame.Surface

roads: list[Road] = []
visible_roads: list[Road] = []
selected_roads: list[Road] = []

select_mode = SimpleNamespace(prev=pygame.Rect(0, 0, 0, 0))
draw_mode = SimpleNamespace(start=None, prev=pygame.Rect(0, 0, 0, 0), p_lines=[])
moving = SimpleNamespace(on=False)
window = Window(False, pygame.Rect(0, 0, 0, 0))
select = Select(pygame.Rect(0, 0, 0, 0))

modes = {'select', 'draw'}
selected_mode = 'select'
button_names = ['select', 'draw', 'clear']

coordinates = [0, 0]
offset = [0, 0]

font_consolas = None
