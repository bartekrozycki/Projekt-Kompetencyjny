from typing import Callable

import pygame
from pygame.event import Event

import settings
from foreground import Foreground
from resources import event_handler, context, core
from const import color


class Grid:
    surface: pygame.Surface
    rect: pygame.Rect

    prev_mouse_pos = None

    @event_handler
    def __init__(self):
        self.generate_grid()
        core.foreground = Foreground(core.screen, context)
        core.foreground.update_background(self.surface)
        core.foreground.render()

    def generate_grid(self):
        self.surface = pygame.Surface(core.screen.get_rect().inflate((context.grid_density, context.grid_density)).size)

        self.surface.fill(color.SKY_BLUE)

        if context.grid_density <= settings.GRID_MIN_DENSITY:
            return

        dot_size = 2 if context.grid_density > 20 else 1

        # drawing grid dots
        for x in range(int(core.screen.get_width() // context.grid_density) + 2):
            for y in range(int(core.screen.get_height() // context.grid_density) + 2):
                pygame.draw.rect(self.surface, (0, 0, 0), (x * context.grid_density, y * context.grid_density, dot_size, dot_size), 1)

    def handle_event(self, event: Event):
        options: dict[int, Callable[[Event], None]] = {
            pygame.MOUSEBUTTONDOWN: self.mouse_button_down,
            pygame.MOUSEBUTTONUP: self.mouse_button_up,
            pygame.MOUSEMOTION: self.mouse_motion,
            pygame.VIDEORESIZE: self.video_resize,
        }

        try:
            options[event.type](event)
        except KeyError:
            pass

    def mouse_button_down(self, event: Event):
        mouse_pos = pygame.mouse.get_pos()
        zoom_factor = 1.125

        # is_moving the grid
        def button_middle():
            context.is_moving = True

        # zoom_sensitivity in
        def button_wheel_up():
            if not context.grid_density <= settings.GRID_MAX_DENSITY:
                return

            context.zoom_sensitivity *= zoom_factor
            context.grid_density *= zoom_factor

            x = core.foreground.rect.x
            y = core.foreground.rect.y

            dx = int(mouse_pos[0] - x) * (zoom_factor - 1)
            dy = int(mouse_pos[1] - y) * (zoom_factor - 1)

            core.foreground.move((-dx, -dy))
            context.user_position[0] -= dx
            context.user_position[1] -= dy

            self.generate_grid()
            core.render_all = True

            core.foreground.update_background(self.surface)
            core.foreground.update_roads()
            core.foreground.render()

        # zoom_sensitivity out
        def button_wheel_down():
            if not context.grid_density >= settings.GRID_MIN_DENSITY:
                self.generate_grid()
                core.render_all = True
                return
            context.zoom_sensitivity /= zoom_factor
            context.grid_density /= zoom_factor

            x = core.foreground.rect.x
            y = core.foreground.rect.y

            dx = int(mouse_pos[0] - x) * (1 / zoom_factor - 1)
            dy = int(mouse_pos[1] - y) * (1 / zoom_factor - 1)

            core.foreground.move((-dx, -dy))
            context.user_position[0] -= dx
            context.user_position[1] -= dy

            if not context.grid_density > 2:
                return
            self.generate_grid()
            core.render_all = True

            core.foreground.update_background(self.surface)
            core.foreground.update_roads()
            core.foreground.render()


        options = {
            pygame.BUTTON_MIDDLE: button_middle,
            pygame.BUTTON_WHEELUP: button_wheel_up,
            pygame.BUTTON_WHEELDOWN: button_wheel_down,
        }
        options[event.button]()

    def mouse_button_up(self, event: Event):
        # is_moving the grid
        def button_middle():
            context.is_moving = False
            self.prev_mouse_pos = None

        options = {
            pygame.BUTTON_MIDDLE: button_middle,
        }
        options[event.button]()

    def mouse_motion(self, event: Event):
        # is_moving the grid
        if context.is_moving:
            try:
                mouse_pos = pygame.mouse.get_pos()

                core.foreground.move((mouse_pos[0] - self.prev_mouse_pos[0], mouse_pos[1] - self.prev_mouse_pos[1]))

                core.foreground.update_background(self.surface)
                core.foreground.update_roads()
                core.foreground.render()
            except TypeError:
                pass
            finally:
                self.prev_mouse_pos = pygame.mouse.get_pos()
                core.render_all = True

    def video_resize(self, event: Event):
        self.generate_grid()
        core.foreground.update_background(self.surface)
        core.foreground.render()
