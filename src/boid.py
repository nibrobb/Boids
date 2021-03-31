from random import randint
import pygame
from pygame import math
from config import *


class Boid(pygame.sprite.Sprite):
    """Boid class"""
    def __init__(self, game, startpos, color = WHITE):
        super().__init__()

        self.game = game

        self.image = game.boid_img          # Copying the original boid-image
        self.rect = self.image.get_rect()

        self.color = color

        self.pos = pygame.Vector2(startpos)
        self.vel = pygame.Vector2(0, 0)
        self.angle = 0                            # Initial rotation of 0 degrees
        self.up_vector = pygame.Vector2(0, -1)    # Vector for the direction of the original image

        # Initial random speed and direction (might delete leater)
        self.vel = pygame.Vector2(randint(-BOID_SPEED, BOID_SPEED), randint(-BOID_SPEED, BOID_SPEED))


    def update(self):
        """ Update """
        # TODO: Implement these rules
        self.separation()
        self.alignment()
        self.cohesion(self.game.master_coh_weight)

        self.move()

    def move(self):
        """ Calculate the next position and rotate image """
        # if self.vel.magnitude() > SPEED_LIMIT:
        #         self.vel *= 0.95
        if self.vel.magnitude() > SPEED_LIMIT:
            self.vel = self.vel.normalize() * SPEED_LIMIT
        self.angle = self.vel.angle_to(self.up_vector) % 360   # Find the angle to draw the boid
        self.pos += self.vel * self.game.delta_time                    # Caluculate new position
        self.rect = self.image.get_rect(center=self.pos)       # Get a new rect and set its center to pos
        self.image = pygame.transform.rotate(self.game.boid_img, self.angle)


    # Rule that applies to all rules of boids:
    #   * A boid can only "see" some amount of its neighbors. It has a radius
    #       boids in that radius are neighbors, and those outside are not.
    def separation(self):
        """ Steer to avoid crowding """
        # Find distance to neighbors, if the distance to a neighbor is too close
        #   steer so that you get a larger distance

        ### Some piece of code to not have the boids fly off into the void (i.e. off screen) ###
        # self.avoid_wall()       # This is added to prevent boids from escaping the "play area"
        self.wrap()               # Make the boid appear on the other side of the window if it crosses the edge


    def alignment(self):
        """ Steer towards the average direction of nearby boids """
        # Makes boids steer to the average heading of neighbors
        # Little snippet to set a random velocity


    def cohesion(self, weight = 1):
        """ Steer towards the center of mass of nearby boids """
        # Makes all boids in a radius stay in the same general direction.
        # A boid should navigate towards the center of all other neighbors

        ### Code for finding neighbors ###
        _neighbors = pygame.sprite.Group()
        for boid in self.game.all_sprites:
            _dist = self.pos.distance_to(boid.pos)
            # Add a boid to the neighbors group if they are within "line of sight"
            if self.pos != boid.pos and _dist < VIEW_DISTANCE:
                _neighbors.add(boid)
        
        # Find average position of neighboring boids
        if len(_neighbors) != 0:
            average_boid_pos = pygame.Vector2()
            for neighbor in _neighbors:
                average_boid_pos += neighbor.pos
            average_boid_pos /= len(_neighbors)

            average_boid_pos -= self.pos # Prøve nokka nytt

            self.vel += weight * average_boid_pos * self.game.delta_time
            # self.vel = weight * average_boid_pos * self.game.delta_time
            # self.vel = self.vel.rotate(self.vel.angle_to(average_boid_pos) * weight * self.game.delta_time)
            

    def avoid_wall(self):
        """ Make boids avoid walls """
        _turn = 500     # Rate of rotation, how fast the boid turns around
        _sign = 1       # Sign before turn-amount, + clockwise, - anti-clockwise
        _margin = 100   # How close a boid can get to a wall before it turns
        if self.pos.x < _margin:
            if self.angle <= 90 or self.angle >= 270:
                _sign = 1
            else:
                _sign = -1
            self.vel = self.vel.rotate(_sign * _turn * self.game.delta_time)
        elif self.pos.x > SCREEN_X - (_margin):
            if self.angle >= 270 or self.angle <= 90:
                _sign = -1
            else:
                _sign = 1
            self.vel = self.vel.rotate(_sign * _turn * self.game.delta_time)
        elif self.pos.y < _margin:
            if self.angle <= 180:
                _sign = -1
            else:
                _sign = 1
            self.vel = self.vel.rotate(_sign * _turn * self.game.delta_time)
        elif self.pos.y > SCREEN_Y - (_margin):
            if self.angle <= 180:
                _sign = 1
            else:
                _sign = -1
            self.vel = self.vel.rotate(_sign * _turn * self.game.delta_time)

    def wrap(self):
        """ Cheap way of wrapping boids around to the other side of the window when they hit a wall """
        self.pos.x %= SCREEN_X
        self.pos.y %= SCREEN_Y
