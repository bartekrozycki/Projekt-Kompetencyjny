import pygame
from pygame.constants import QUIT

import config
from display.grid import Grid


class App:
    event_handlers = []

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

        self.event_handlers.append(Grid(self, self.screen))

        self.running = True

    def render(self):
        self.screen.fill((255, 255, 255))  # White background
        for o in self.event_handlers:
            o.render()
        # for pos in self.test:
        #     pygame.draw.circle(self.screen, (255, 0, 0), (self.pos_x + pos[0] + 1, self.pos_y + pos[1] + 1),
        #                        4 * self.zoom, 1)
        pygame.display.update()

    def run(self):
        """Run the main event loop."""
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    break

                for event_handler in self.event_handlers:
                    event_handler.handle_event(event)
            self.render()
        pygame.quit()


if __name__ == '__main__':
    App().run()
