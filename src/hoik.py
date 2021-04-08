""" Class of hoiks """
# -*- coding: utf-8 -*-
import pygame
from boid import Boid
from config import *

class Hoik(Boid):
    """ The Hoik class """
    def __init__(self, game, pos):
        """ Initializing method """
        super().__init__(game, pos)

        self.image = self.game.hoik_img     # Making a copy of the hoik image
        self.rect = self.image.get_rect()   # Aquiring the bounding box


    def move(self, move):
        """ Calculate the next position and rotate image """
        self.vel += move
        if self.vel.magnitude() > MAX_HOIK_SPEED:
            self.vel = self.vel.normalize() * MAX_HOIK_SPEED
        self.angle = self.vel.angle_to(self.up_vector) % 360
        self.pos += self.vel * self.game.delta_time
        self.rect = self.image.get_rect(center=self.pos)

        self.image = pygame.transform.rotate(self.game.hoik_img, self.angle)

        # Upon hitting a boid, kill that boid
        neighboring_boids = self.get_neighbors()
        for innocent_boid in neighboring_boids:
            if self.pos.distance_to(innocent_boid.pos) < 10:
                innocent_boid.kill()

        self.wrap()


    def alignment(self, neighbors: pygame.sprite.Group) -> pygame.Vector2:
        """ Keep going which ever direction you are going """
        # Equivalent to not making any change in steering
        return self.vel

    # Inherit cohesion from parent class so that we chase boids

    def separation(self, neighbors: pygame.sprite.Group) -> pygame.Vector2:
        """ Do not try to separate, returns a null-vector, meaning no change """
        return pygame.Vector2()


    def get_neighbors(self) -> pygame.sprite.Group:
        """ Find neighboring boids """
        neighbors = pygame.sprite.Group()
        for boid in self.game.all_boids:
            dist = self.pos.distance_to(boid.pos)
            
            # Hoiks can see 10 times farther than boids
            if dist < 10*VIEW_DISTANCE:
                neighbors.add(boid)
        return neighbors
