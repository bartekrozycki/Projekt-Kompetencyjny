from types import SimpleNamespace

import pygame

fps_limit = 60

cell = SimpleNamespace(min=4, max=64, size=8)
menu = SimpleNamespace(width=100)
buttons = []

resolution = None
window = None

background: pygame.sprite.Sprite
bg_menu: pygame.sprite.Sprite

roads = []

clock = pygame.time.Clock()

drawing = False

mouse_pos = SimpleNamespace(x=0, y=0)
coordinates = SimpleNamespace(x=0, y=0)

font_consolas = None
