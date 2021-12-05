import pygame
from pygame.event import Event

from UI.menu.Button import Button, WIDTH
from const import color, tool
from resources import core, event_handler, context, images


class Menu(pygame.sprite.Sprite):
    active: Button = None

    @event_handler
    def __init__(self):
        super().__init__()
        button_count = 2
        self.image = pygame.surface.Surface((10 * 2 + WIDTH,
                                             10 * (1 + button_count) + WIDTH * button_count))  # width, height = [10*2 + BUTTON->WIDTH, 10*2 + 30 * COUNT_OF_BUTTON]
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, color.BLACK, self.rect, 1)
        self.rect.top = 100
        self.rect.right = core.screen_rect.right

        self.a = Button(self.image, images.cursor, 10, onActivate=self.set_active_tool_to_basic_cursor_callback)
        self.b = Button(self.image, images.road, 50, onActivate=self.set_active_tool_to_draw_road_callback)

    @staticmethod
    def set_active_tool_to_basic_cursor_callback():
        context._active_tool = tool.BASIC_CURSOR

    @staticmethod
    def set_active_tool_to_draw_road_callback():
        context._active_tool = tool.DRAW_ROAD

    def handle_event(self, event: Event):
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos):  # not button but menu clicked
                return True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x, y = [pos[0] - self.rect.left, pos[1] - self.rect.top]
            for s in [s for s in core.group_ui_menu_buttons.sprites() if s.rect.collidepoint(x, y)]:
                if self.active:
                    self.active.toggle()
                self.active = s
                self.active.toggle()
                return True
            if self.rect.collidepoint(pos):  # not button but menu clicked
                return True
