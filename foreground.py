import pygame.sprite

from resources import context


class Foreground(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface, context):
        super().__init__()
        self.image = pygame.Surface(screen.get_size())
        self.background = pygame.Surface(screen.get_size())
        self.rect = pygame.Rect((0, 0), screen.get_size())
        self.screen = screen
        self.context = context
        self.roads = pygame.sprite.Group()

    def update_background(self, image: pygame.Surface):
        self.background = pygame.Surface(self.screen.get_size())
        self.rect.size = self.background.get_size()

        gd = self.context.grid_density
        x = -(gd - self.rect.x % gd)
        y = -(gd - self.rect.y % gd)

        self.background.blit(image, (
            (x, y), (self.rect.x % self.context.grid_density, self.rect.y % self.context.grid_density)))

        self.image = pygame.Surface(self.screen.get_size())
        self.image.blit(self.background, (0, 0))

        for road in self.roads:
            road.draw()
            road.render()

    def move(self, vector: tuple[int, int]):
        for road in self.roads:
            road.draw()
            road.render()
        self.rect = self.rect.move(*vector)

    def update_roads(self):
        self.roads.draw(self.image)

    def render(self):
        self.screen.blit(self.image, (0, 0))
