import pygame
from pygame.constants import QUIT

import config
from display.display_object_grid import Grid
from display.display_object_interface import DisplayObjectInterface


class App:
    objects: list[DisplayObjectInterface] = []

    """Create a single-window app with multiple scenes."""

    def __init__(self):
        """Initialize pygame and the application."""
        pygame.init()  # might be in wrong line (maybe above)
        self.screen = pygame.display.set_mode((config.display_width, config.display_height), config.display_flags)
        self.user_position = config.map_default_pos
        self.zoom = 1
        self.moving = False
        self.prev_mouse_pos = None
        self.test = [(0, 0), (20, 0), (50, 0)]

        self.objects.append(Grid(self, self.screen))

        self.running = True

    def render(self):
        self.screen.fill((255, 255, 255))  # White background
        for o in self.objects:
            o.render()
        # for pos in self.test:
        #     pygame.draw.circle(self.screen, (255, 0, 0), (self.pos_x + pos[0] + 1, self.pos_y + pos[1] + 1),
        #                        4 * self.zoom, 1)
        pygame.display.update()

    def run(self):
        """Run the main event loop."""
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    self.running = False
            for o in self.objects:
                o.dispatch_event(events)
            self.render()
        pygame.quit()


if __name__ == '__main__':
    App().run()
