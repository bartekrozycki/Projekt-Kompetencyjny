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
        pygame.font.init()
        self.console_font = pygame.font.SysFont('Consolas', 12)
        self.screen = pygame.display.set_mode((config.display_width, config.display_height), config.display_flags)
        self.user_position = config.map_default_pos
        self.zoom = 1
        self.moving = False
        self.prev_mouse_pos = None
        self.test = [(0, 0), (2, 0), (5, 0)]
        self.grid_density = config.grid_density

        self.event_handlers.append(Grid(self, self.screen))

        self.running = True

    def render(self):
        self.screen.fill((135, 206, 250))  # White background
        for o in self.event_handlers:
            o.render()
        for pos in self.test:
            pygame.draw.circle(self.screen, (255, 0, 0), (self.user_position[0] + pos[0] * self.grid_density + 1,
                                                          self.user_position[1] + pos[1] * self.grid_density + 1),
                               4 * self.zoom, 1)


        cursor_position = pygame.mouse.get_pos()
        cursor_position_text = self.console_font.render(' x: {:.0f} y: {:.0f}'.format(
            (cursor_position[0] - self.user_position[0]) // self.grid_density,
            -(cursor_position[1] - self.user_position[1]) // self.grid_density,
        ),
            False, (255, 255, 255))
        cursor_position_height = cursor_position_text.get_height()
        cursor_position_width = cursor_position_text.get_width() + 5
        pygame.draw.rect(self.screen, (0, 0, 0), (
            0, config.display_height - cursor_position_height, cursor_position_width, cursor_position_height), 0)
        self.screen.blit(cursor_position_text, (
            0, config.display_height - cursor_position_height, cursor_position_width, cursor_position_height))
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
