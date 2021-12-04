import pygame.sprite
from pygame import Surface
from pygame.time import Clock

from foreground import Foreground


class Core:
    screen: Surface
    foreground: Foreground
    clock: Clock

    every_frame_render = []
    event_handlers = []
    renderables = []
    dirty_rectangles = []
    background_rectangles = []
    roads_to_draw = []
    components_surfaces = []
    lines = []

    road_group = pygame.sprite.Group()



    render_all = True
