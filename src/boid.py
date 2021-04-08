""" Class of boids """
# -*- coding: utf-8 -*-
from random import randint
import pygame
from config import *


class Boid(pygame.sprite.Sprite):
    """
    Boid class
    This class controls all boids in simulation
    """
    def __init__(self, game, startpos):
        super().__init__()

        self.game = game                    # Game "reference" to more easily access game variables

        self.image = game.boid_img          # Making a copy of the original boid-image
        self.rect = self.image.get_rect()   # Aquiring the bounding box for the image

        self.pos = pygame.Vector2(startpos)
        self.vel = pygame.Vector2(0, 0)
        self.angle = 0                            # Initial rotation of 0 degrees
        self.up_vector = pygame.Vector2(0, -1)    # Vector for the direction of the original image

        # Initial random velocity
        self.vel = pygame.Vector2(randint(-BOID_SPEED, BOID_SPEED), randint(-BOID_SPEED, BOID_SPEED))


    def update(self):
        """ Gets called once every frame, calls functions to update boid position """
        move = self.calculate_move()
        self.move(move)

    def calculate_move(self) -> pygame.Vector2:
        """ Calculates the next movement based on the three rules of boids """
        neighbors = self.get_neighbors()
        move = pygame.Vector2()

        rules = [self.alignment, self.cohesion, self.separation]
        partial_move : pygame.Vector2 = pygame.Vector2()
        for i in range(len(rules)):
            partial_move = rules[i](neighbors)
            if (partial_move != pygame.Vector2(0,0)):
                if partial_move.magnitude() > self.game.weights[i]:
                    partial_move.normalize()
                    partial_move *= self.game.weights[i]
                move += partial_move
        return move


    def move(self, move):
        """ Set the next position and rotate image accordingly """
        self.vel += move
        if self.vel.magnitude() > MAX_SPEED:
            self.vel = self.vel.normalize() * MAX_SPEED
        self.angle = self.vel.angle_to(self.up_vector) % 360   # Find the angle to draw the boid
        self.pos += self.vel * self.game.delta_time            # Caluculate new position
        self.rect = self.image.get_rect(center=self.pos)       # Get a new rect and set its center to pos
        self.image = pygame.transform.rotate(self.game.boid_img, self.angle)
        
        ### Some piece of code to not have the boid fly off into the void (i.e. off screen) ###
        self.wrap()            # Make the boid appear on the other side of the window if it crosses the edge

    # Rule no. 1
    def alignment(self, neighbors : pygame.sprite.Group) -> pygame.Vector2:
        """ Steer towards the average direction of nearby boids """
        # Makes boids steer to the average heading of neighbors
        # Skal innrømme at æ henta mye inspirasjon fra Board To Bits Games
        #       Kilde: https://youtu.be/7LDFLMRGyqs

        # If no neighbors, maintain our current heading
        if len(neighbors) == 0:
            return self.vel

        alignment_move = pygame.Vector2()
        for neighbor in neighbors:
            alignment_move += neighbor.vel
        alignment_move /= len(neighbors)

        return alignment_move


    # Rule no. 2
    def cohesion(self, neighbors : pygame.sprite.Group) -> pygame.Vector2:
        """ Steer towards the center of mass of nearby boids """
        # Makes all boids in a radius stay in the same general direction.
        # A boid should navigate towards the center of all other neighbors
        
        # Find average position of neighboring boids
        if len(neighbors) == 0:
            return self.vel
        cohesion_move = pygame.Vector2()
        for neighbor in neighbors:
            cohesion_move += neighbor.pos
        cohesion_move /= len(neighbors)

        cohesion_move -= self.pos # Getting the offset from the position boid is right now
        return cohesion_move
        # Funka ikkje som før, men d kanskje bedre for slutten(?)
        # ok ok ok, se her, alle funksjonan returnere en ny vektor
        # så det e ikkje sånn at hvert funksjon gjør nokka med vel

    
    # Rule no. 3
    def separation(self, neighbors : pygame.sprite.Group) -> pygame.Vector2:
        """ Steer to avoid crowding """
        # Find distance to neighbors, if the distance to a neighbor is too close
        #   steer so that you get a larger distance
        if len(neighbors) == 0:
            return pygame.Vector2()

        # En kan tenke seg at vi har flere radiier, en for naboer, og en for "plagsomme naboer"
        # Dette er metoden som håndterer den sistnevnte
        # Vi tenker oss en radius inni nabo-radiusen som hvis det forekommer noen boids i skal vi
        # prøve å få større avstand til
        separation_move = pygame.Vector2()
        n_avoid = 0

        for neighbor in neighbors:
            if (neighbor.pos.distance_to(self.pos) < AVOIDANCE_RADIUS):
                n_avoid += 1
                separation_move += (self.pos - neighbor.pos)
        
        if n_avoid > 0:
            separation_move /= n_avoid
        return separation_move




    def get_neighbors(self) -> pygame.sprite.Group:
        """ Code for finding neighbors """
        neighbors = pygame.sprite.Group()
        for boid in self.game.all_boids:
            dist = self.pos.distance_to(boid.pos)
            # Add a boid to the neighbors group if they are within "line of sight"
            if self.pos != boid.pos and dist < VIEW_DISTANCE:
                neighbors.add(boid)
        return neighbors


    def wrap(self):
        """ Cheap way of wrapping boids around to the other side of the window when they hit a wall """
        self.pos.x %= SCREEN_X
        self.pos.y %= SCREEN_Y
