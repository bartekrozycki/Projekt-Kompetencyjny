from typing import Callable

import pygame

from const import color
from resources import core, images

BUTTON_WIDTH = 30


class Button(pygame.sprite.DirtySprite):
    _active = False

    drawActive = lambda self, color: pygame.draw.rect(self.image, color, [0, 0, self.rect.w, self.rect.h], 1)

    def __init__(self, image, position, onActivate: Callable = None, onDeactivate: Callable = None):
        super().__init__(core.group_ui_menu_buttons)
        self.onActivate = onActivate
        self.onDeactivate = onDeactivate
        self.image = image

        leftOffset, topOffset = position

        self.image = pygame.transform.scale(self.image, (BUTTON_WIDTH, BUTTON_WIDTH))
        self.rect = self.image.get_rect()

        pygame.draw.rect(self.image, color.BLACK, self.rect, 1)

        self.rect.top = topOffset
        self.rect.left = leftOffset

    def toggle(self):
        self._active = not self._active
        if self._active:
            self.drawActive(color.RED)
            self.dirty = 1
            if self.onActivate:
                self.onActivate()
        else:
            pygame.draw.rect(self.image, color.BLACK, [0, 0, self.rect.w, self.rect.h], 1)
            self.dirty = 1
            if self.onDeactivate:
                self.onDeactivate()
