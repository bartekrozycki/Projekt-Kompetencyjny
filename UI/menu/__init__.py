import pygame
from pygame.event import Event

from UI.menu.Button import Button, BUTTON_WIDTH
from const import color
from resources import core, event_handler


class ButtonMenu(pygame.sprite.DirtySprite):
    active: Button = None

    @event_handler
    def __init__(self, props, size: (int, int), frame_offset=(15, 10), item_offset=(5, 5)):
        super().__init__()

        cols, rows = size
        width_offset, height_offset = frame_offset
        width_item_offset, height_item_offset = item_offset

        width_total = width_offset * 2
        width_total += cols * BUTTON_WIDTH
        width_total += (cols - 1) * width_item_offset

        height_total = height_offset * 2
        height_total += rows * BUTTON_WIDTH
        height_total += (rows - 1) * height_item_offset

        left_offset = lambda pos: width_offset + \
                                  ((pos - 1) * width_item_offset) + \
                                  ((pos - 1) * BUTTON_WIDTH)

        top_offset = lambda pos: height_offset + \
                                 ((pos - 1) * height_item_offset) + \
                                 ((pos - 1) * BUTTON_WIDTH)

        self.image = pygame.surface.Surface((width_total, height_total))
        self.rect = self.image.get_rect()

        self.image.fill((255, 255, 255))
        pygame.draw.rect(self.image, color.BLACK, self.rect, 1)

        self.rect.top = core.screen_rect.top + 5
        self.rect.left = core.screen_rect.left + 5

        for col in range(1, cols + 1):
            for row in range(1, rows + 1):
                try:
                    img, activate = props[(((col - 1) * rows) + row) - 1]
                    Button(img, (left_offset(col), top_offset(row)), onActivate=activate)
                except IndexError:
                    pass

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
