from random import randint
import pygame
from config import *


class Boid(pygame.sprite.Sprite):
    """Boid class"""
    def __init__(self, game, startpos):
        super().__init__()

        self.game = game

        self.image = game.boid_img          # Copying the originale boid-image
        self.rect = self.image.get_rect()

        self.color = WHITE

        self.pos = pygame.Vector2(startpos)
        self.vel = pygame.Vector2(0, 0)
        self.angle = 0                            # Initial rotation of 0 degrees
        self.up_vector = pygame.Vector2(0, -1)    # Vector for the direction of the original image


    def update(self):
        self.get_keys()                                                         # Testing

        self.angle = self.vel.angle_to(self.up_vector)   # Find the angle to draw the boid
        self.pos += self.vel * self.game.dt              # Caluculate new position
        self.rect = self.image.get_rect(center=self.pos) # Get a new rect and set its center to pos
        self.image = pygame.transform.rotate(self.game.boid_img, self.angle)



        self.separation()
        self.alignment()
        self.cohesion()

    
    def get_keys(self):
        """ testing """
        keys = pygame.key.get_pressed()
        

    def separation(self):
        """ Steer to avoid crowding """
        pass

    def alignment(self):
        """ Steer towards the average direction of nearby boids """

        # Little snippet to set a random velocity
        if self.vel.x == 0 and self.vel.y == 0:
            self.vel += pygame.Vector2(randint(-BOID_SPEED, BOID_SPEED), randint(-BOID_SPEED, BOID_SPEED))

    def cohesion(self):
        """ Steer towards the center of mass of nearby boids """
        pass
