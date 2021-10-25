import time

import pygame
from pygame.locals import *


class App:
    """Create a single-window app with multiple scenes."""

    def __init__(self):
        """Initialize pygame and the application."""
        pygame.init()
        flags = RESIZABLE
        self.screen = pygame.display.set_mode((640, 640), flags)
        self.pos_x = 0
        self.pos_y = 0
        self.density = 10
        self.zoom = 1
        self.moving = False
        self.prev_mouse_pos = None
        self.test = [(0, 0)]

        self.running = True

    def draw_grid(self):
        win_width, win_height = self.screen.get_size()


        x = self.pos_x % self.density
        y = self.pos_y % self.density
        while x < win_width:
            while y < win_height:
                pygame.draw.rect(self.screen, (0, 0, 0), (x, y, 1, 1), 1)
                y += self.density
            y = self.pos_y % self.density
            x += self.density

    def render(self):
        self.screen.fill((255, 255, 255))  # White background
        self.draw_grid()
        for pos in self.test:
            pygame.draw.circle(self.screen, (255, 0, 0), (self.pos_x + pos[0] + 1, self.pos_y + pos[1] + 1), 4 * self.zoom, 1)
        pygame.display.update()

    def run(self):
        """Run the main event loop."""
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_MIDDLE:
                        self.moving = True
                    elif event.button == pygame.BUTTON_WHEELUP:
                        self.zoom *= 1.125
                        self.density *= 1.125
                    elif event.button == pygame.BUTTON_WHEELDOWN:
                        self.zoom /= 1.125
                        self.density /= 1.125
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == pygame.BUTTON_MIDDLE:
                        self.moving = False
                        self.prev_mouse_pos = None
                elif event.type == pygame.MOUSEMOTION and self.moving:
                    try:
                        mouse_pos = pygame.mouse.get_pos()
                        self.pos_x += mouse_pos[0] - self.prev_mouse_pos[0]
                        self.pos_y += mouse_pos[1] - self.prev_mouse_pos[1]
                    except:
                        pass
                    self.prev_mouse_pos = pygame.mouse.get_pos()
            self.render()
        pygame.quit()


if __name__ == '__main__':
    App().run()
