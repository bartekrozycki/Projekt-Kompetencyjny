import pygame
from pygame.constants import *

import settings
from UI.draw_single_road import DrawSingleRoad
from UI.grid import Grid
from UI.infoBar.coordintes import Coordinates
from UI.menu import ButtonMenu
from const import tool
from resources import core, images, context


def set_active_tool_to_basic_cursor_callback():
    context._active_tool = tool.BASIC_CURSOR


def set_active_tool_to_draw_road_callback():
    context._active_tool = tool.DRAW_ROAD


if __name__ == '__main__':
    pygame.font.init()
    pygame.display.init()

    core.clock = pygame.time.Clock()
    core.screen = pygame.display.set_mode((settings.DISPLAY_WIDTH, settings.DISPLAY_HEIGHT), settings.DISPLAY_FLAGS)
    core.screen_rect = core.screen.get_rect()

    menu = pygame.sprite.GroupSingle(
        ButtonMenu([
            (images.cursor, set_active_tool_to_basic_cursor_callback),
            (images.road, set_active_tool_to_draw_road_callback),
        ], (1, 2)
        )
    )

    grid = Grid()
    # FPSCounter()
    # Zoom()
    Coordinates()
    #
    #
    DrawSingleRoad()


    #
    # DrawRoadButton()

    def render():
        if core.render_all:
            for renderable in core.renderables:
                renderable.render()
            core.render_all = False
        menu.draw(core.screen)
        core.group_ui_menu_buttons.draw(menu.sprite.image)
        pygame.display.update()


    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                running = False
                break
            elif event.type == VIDEORESIZE:
                core.render_all = True
            for event_handler in core.event_handlers:
                handle_event = event_handler.handle_event(event)
                if handle_event:
                    break
        render()

        core.clock.tick(settings.DISPLAY_MAX_FPS)
    pygame.quit()
