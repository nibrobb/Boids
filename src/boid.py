import pygame
from config import *


class Boid(pygame.sprite.Sprite):
    """Boid class"""
    def __init__(self, color, startpos : pygame.Vector2, startdir : pygame.Vector2):
        super().__init__()
        self.color = color

        self.width = BOID_WIDTH
        self.height = BOID_HEIGHT

        self.pos = pygame.Vector2(startpos)
        self.velocity = pygame.Vector2(5,5)

        self.direction = pygame.Vector2(startdir).normalize()
        self.looking = pygame.Vector2(0, -1)

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.polygon(self.image, self.color, BOID_SHAPE)

        self.rect = self.image.get_rect( center=(round(self.pos.x), round(self.pos.y)) )

        self.angle = 0

    def update(self):
        self.pos += self.direction * 2
        self.angle = self.pos.angle_to(self.looking)