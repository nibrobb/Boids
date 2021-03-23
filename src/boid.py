import math
from random import randint
from random import choice
import pygame
from config import *


class Boid(pygame.sprite.Sprite):
    """Boid class"""
    def __init__(self, game, startpos):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.image = game.boid_img          # Copying the originale boid-image
        self.rect = self.image.get_rect()

        self.color = WHITE

        self.pos = pygame.Vector2(startpos)
        self.vel = pygame.Vector2(0, 0)
        self.rot = 0                        # rot=0 means pointing at +x


    def update(self):
        self.get_keys()                                                         # Testing
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360

        self.image = pygame.transform.rotate(self.game.boid_img, self.rot)

        self.alignment()

        self.pos += self.vel * self.game.dt

        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        # Make so we point to the direction we are facing

    def get_keys(self):
        """ testing """
        self.rot_speed = 0
        keys = pygame.key.get_pressed()
        if keys[ord('q')]:
            self.rot_speed = BOID_ROT_SPEED
        elif keys[ord('e')]:
            self.rot_speed = -BOID_ROT_SPEED
        

    def separation(self):
        """ Steer to avoid crowding """
        pass

    def alignment(self):
        """ Steer towards the average direction of nearby boids """
        if self.vel.x == 0 or self.vel.y == 0:
            self.vel += pygame.Vector2(choice([-1, 0, 1])*BOID_SPEED, choice([-1, 0, 1])*BOID_SPEED)
        self.vel = pygame.Vector2(BOID_SPEED, 0).rotate(-self.rot)

    def cohesion(self):
        """ Steer towards the center of mass of nearby boids """
        pass
