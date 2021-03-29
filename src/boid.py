from random import randint
import pygame
from config import *


class Boid(pygame.sprite.Sprite):
    """Boid class"""
    def __init__(self, game, startpos, color = WHITE):
        super().__init__()

        self.game = game

        self.image = game.boid_img          # Copying the originale boid-image
        self.rect = self.image.get_rect()

        self.color = color

        self.pos = pygame.Vector2(startpos)
        self.vel = pygame.Vector2(0, 0)
        self.angle = 0                            # Initial rotation of 0 degrees
        self.up_vector = pygame.Vector2(0, -1)    # Vector for the direction of the original image

        # Initial random speed and direction (might delete leater)
        self.vel = pygame.Vector2(randint(-BOID_SPEED, BOID_SPEED), randint(-BOID_SPEED, BOID_SPEED))


    def update(self):
        self.get_keys()                                                         # Testing

        # TODO: Implement these rules
        self.separation()
        self.alignment()
        self.cohesion()

        self.move()

    def move(self):
        self.angle = self.vel.angle_to(self.up_vector)   # Find the angle to draw the boid
        self.pos += self.vel * self.game.dt              # Caluculate new position
        self.rect = self.image.get_rect(center=self.pos) # Get a new rect and set its center to pos
        self.image = pygame.transform.rotate(self.game.boid_img, self.angle)
    
    def get_keys(self):
        """ testing """
        keys = pygame.key.get_pressed()
        

    # Rule that applies to all rules of boids:
    #   * A boid can only "see" some amount of its neighbors. It has a radius
    #       boids in that radius are neighbors, and those outside are not.
    def separation(self):
        """ Steer to avoid crowding """
        # Find distance to neighbors, if the distance to a neighbor is too close
        #   steer so that you get a larger distance
        _turn = 250
        _sign = 1
        if self.pos.x < self.rect.width:
            if self.angle < 90:
                _sign = 1
            else:
                _sign = -1
            self.vel = self.vel.rotate(_sign * _turn * self.game.dt)
        elif self.pos.x > SCREEN_X - (self.rect.width):
            if self.angle < 270:
                _sign = 1
            else:
                _sign = -1
            self.vel = self.vel.rotate(_sign * _turn * self.game.dt)
        elif self.pos.y < self.rect.height:
            if self.angle > 270:
                _sign = 1
            else:
                _sign = -1
            self.vel = self.vel.rotate(_sign * _turn * self.game.dt)
        elif self.pos.y > SCREEN_Y - (self.rect.height):
            if self.angle < 270:
                _sign = 1
            else:
                _sign = -1
            self.vel = self.vel.rotate(_sign * _turn * self.game.dt)


    def alignment(self):
        """ Steer towards the average direction of nearby boids """
        # Makes boids steer to the average heading of neighbors
        # Little snippet to set a random velocity
        

    def cohesion(self):
        """ Steer towards the center of mass of nearby boids """
        # Makes all boids in a radius stay in the same general direction.
        # A boid should navigate towards the center of all other neighbors

        pass
