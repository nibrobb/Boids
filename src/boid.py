import pygame
from config import *

class Boid(pygame.sprite.Sprite):
    def __init__(self, color, scale):
        super().__init__()
        self.color = color
        self.scale = scale

        self.width = self.height = (10 * scale)

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, color, [0, 0, self.width, self.height])

        self.rect = self.image.get_rect()
