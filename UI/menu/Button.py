from typing import Callable

import pygame

from const import color
from resources import core, images

WIDTH = 30


class Button(pygame.sprite.DirtySprite):
    _active = False

    def __init__(self, parent: pygame.Surface, image, topOffset, onActivate: Callable = None,
                 onDeactivate: Callable = None):
        super().__init__(core.group_ui_menu_buttons)
        self.onActivate = onActivate
        self.onDeactivate = onDeactivate
        parent_rect = parent.get_rect()

        self.image = image
        self.image = pygame.transform.scale(self.image, (WIDTH, WIDTH))

        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, color.BLACK, self.rect, 1)

        self.rect.top = topOffset
        self.rect.centerx = parent_rect.centerx

    def toggle(self):
        self._active = not self._active
        if self._active:
            pygame.draw.rect(self.image, color.RED, [0, 0, self.rect.w, self.rect.h], 1)
            self.dirty = 1
            if self.onActivate:
                self.onActivate()
        else:
            pygame.draw.rect(self.image, color.GREEN, [0, 0, self.rect.w, self.rect.h], 1)
            self.dirty = 1
            if self.onDeactivate:
                self.onDeactivate()
