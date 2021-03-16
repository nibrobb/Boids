import pygame
from config import *

class Boid(pygame.sprite.Sprite):
    def __init__(self, color, startpos, startdir):
        super().__init__()
        self.color = color

        self.width = BOID_WIDTH
        self.height = BOID_HEIGHT

        self.pos = pygame.Vector2(startpos)
        self.velocity = 5
        self.direction = pygame.Vector2(startdir).normalize()

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.polygon(self.image, self.color, BOID_SHAPE)

        self.rect = self.image.get_rect( center=(round(self.pos.x), round(self.pos.y)) )

        self.new_angle = 0
        self.old_angle = 0

    def update(self):
        self.pos += (self.direction * self.velocity)
        self.rect.center = round(self.pos.x), round(self.pos.y)

        self.old_angle = self.new_angle
        self.new_angle = self.direction.angle_to( pygame.Vector2( (1,1) ) )

        angle_change = self.new_angle - self.old_angle
        self.image = pygame.transform.rotate(self.image, angle_change)
        
        # angle = pygame.Vector2.angle_to(self.heading, pygame.Vector2( 1, 0 )
        # self.image = pygame.transform.rotate(self.image, angle)