import pygame
from pygame.event import Event


class DrawRoadButton:
    surface = None
    rectangle = None
    active = False

    def __init__(self, parent, screen: pygame.Surface):
        self.parent = parent
        self.screen = screen

        self.size = (15, 15)
        self.rectangle = pygame.Rect(screen.get_width() - 10 - self.size[0], 10, self.size[0], self.size[1])
        self.surface = pygame.Surface(self.size)
        self.surface.fill((0, 0, 0))

        self.parent.event_handlers.append(self)
        self.parent.renderables.append(self)

    def handle_event(self, event: Event):
        options = {
            pygame.MOUSEBUTTONDOWN: self.mouse_button_down,
            pygame.VIDEORESIZE: self. video_resize,
        }

        try:
            options[event.type](event)
        except KeyError:
            pass
        except Exception as e:
            print(type(e), e)

    def render(self):
        self.screen.blit(self.surface, self.rectangle)

    def dirty_render(self):
        self.screen.blit(self.surface, self.rectangle)
        self.parent.dirty_rectangles.append(self.rectangle)

    def video_resize(self, event):
        self.rectangle = pygame.Rect(self.screen.get_width() - 10 - self.size[0], 10, self.size[0], self.size[1])

    def mouse_button_down(self, event: Event):
        if event.button == pygame.BUTTON_LEFT:
            if self.rectangle.collidepoint(pygame.mouse.get_pos()):
                self.active = not self.active
                if self.active is True:
                    self.surface.fill((255, 255, 255))
                else:
                    self.surface.fill((0, 0, 0))

                self.dirty_render()
