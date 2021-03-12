import pygame
from config import *

class Boid(pygame.sprite.Sprite):
    def __init__(self, color, scale):
        super().__init__()
        self.color = color
        self.scale = scale

        self.width = BOID_WIDTH
        self.height = BOID_HEIGHT

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.polygon(self.image, self.color, BOID_SHAPE)

        self.rect = self.image.get_rect()
