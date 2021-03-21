import pygame
from config import *
import math

class Boid(pygame.sprite.Sprite):
    """Boid class"""
    def __init__(self, color, startpos, startdir : pygame.Vector2):
        super().__init__()
        self.color = color

        self.width = BOID_WIDTH
        self.height = BOID_HEIGHT

        self.speed = 2

        self.direction = pygame.Vector2(startdir).normalize()
        self.heading = pygame.Vector2(0, -1).normalize()

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.polygon(self.image, self.color, BOID_SHAPE)

        self.rect = self.image.get_rect( center=(round(startpos[0]), round(startpos[1])) )

        self.angle = 0
        self.angle_change = 0

        self.x = self.rect.x
        self.y = self.rect.y

    def draw(self, surface):
        img_copy = self.image.copy()
        img_copy = pygame.transform.rotate(img_copy, self.angle_change)
        surface.blit(img_copy, (self.x, self.y))

    def update(self):
        self.x += self.direction.x * self.speed
        self.y += self.direction.y * self.speed

        direction = pygame.Vector2(self.rect.x, self.rect.y) - pygame.Vector2(self.x, self.y)
        direction.normalize()
        self.angle_change = math.atan2(direction.x, direction.y)
        self.angle = self.angle - self.angle_change
        self.angle = self.angle*180/math.pi
        self.angle %= 360
        print("Direction = \t{}".format(direction))
        print("Total angle = \t{}".format(self.angle))
        print("Angle change = \t{}".format(self.angle_change))

        self.rect.x = self.x
        self.rect.y = self.y
        
        # self.rect.x += self.direction.x * self.speed_x
        # self.rect.y += self.direction.y * self.speed_y


    def separation(self):
        """ Steer to avoid crowding """
        pass

    def alignment(self):
        """ Steer towards the average direction of nearby boids """
        pass

    def cohesion(self):
        """ Steer towards the center of mass of nearby boids """
        pass
