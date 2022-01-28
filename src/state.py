from types import SimpleNamespace

import pygame
from dataclasses import dataclass


@dataclass
class Road:
    connections: list[list[int, int]]
    rect: pygame.Rect
    start: tuple[int, int]
    end: tuple[int, int]
    start_rect: pygame.Rect
    end_rect: pygame.Rect
    vertical: bool


@dataclass
class Window:
    moving: bool
    area: pygame.Rect


@dataclass
class Select:
    hovered: pygame.Rect


@dataclass
class Connect:
    prev: pygame.Rect
    hovered: Road
    start: tuple[int, int]
    end: tuple[int, int]
    erase: pygame.Rect


resolution: tuple[int, int] = (0, 0)
display: pygame.Surface
background: pygame.Surface

roads: list[Road] = []
visible_roads: list[Road] = []
selected_roads: list[Road] = []

draw_mode = SimpleNamespace(start=None, prev=pygame.Rect(0, 0, 0, 0), p_lines=[])
moving = SimpleNamespace(on=False)
window = Window(False, pygame.Rect(0, 0, 0, 0))
select = Select(pygame.Rect(0, 0, 0, 0))
connect = Connect(pygame.Rect(0, 0, 0, 0), None, None, None, None)

modes = {'select', 'draw', 'connect'}
selected_mode = 'select'
button_names = ['select', 'draw', 'clear', 'connect']

coordinates = [0, 0]
offset = [0, 0]

font_consolas = None
