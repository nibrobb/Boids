import math
from random import randint, choice
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
        self.looking = pygame.Vector2(0, -1)
        self.rot = 0                        # rot=0 means pointing at +x
        self.rot_speed = 0


    def update(self):
        self.get_keys()                                                         # Testing

        # Find angle from where we are now, to were we are going
        # Use that angle to rotate the sprite

        
        
        # self.rot = (self.rot - 90 + self.rot_speed * self.game.dt) % 360
        self.rot %= 360
        self.image = pygame.transform.rotate(self.game.boid_img, self.rot)

        self.pos += self.vel * self.game.dt
        self.rect = self.image.get_rect(center=self.pos)

        angle = self.get_angle((self.looking.x, self.looking.y), (self.pos.x, self.pos.y))
        angle = angle * 180 / math.pi
        self.rot += angle
        print(f"Angle = {angle}")

        self.looking = self.pos     # set looking to the new position

        self.separation()
        self.alignment()
        self.cohesion()

    def get_angle(self, origin, destination):
        """Returns angle in radians from origin to destination.
        This is the angle that you would get if the points were
        on a cartesian grid. Arguments of (0,0), (1, -1)
        return .25pi(45 deg) rather than 1.75pi(315 deg).
        """
        x_dist = destination[0] - origin[0]
        y_dist = destination[1] - origin[1]
        return math.atan2(-y_dist, x_dist) % (2 * math.pi)

    def get_keys(self):
        """ testing """
        self.rot_speed = 0
        keys = pygame.key.get_pressed()
        

    def separation(self):
        """ Steer to avoid crowding """
        pass

    def alignment(self):
        """ Steer towards the average direction of nearby boids """

        # Little snippet to set a random velocity
        if self.vel.x == 0 and self.vel.y == 0:
            self.vel += pygame.Vector2(randint(-100, 100), randint(-100, 100))
        # self.vel = pygame.Vector2(BOID_SPEED, 0).rotate(-self.rot)

    def cohesion(self):
        """ Steer towards the center of mass of nearby boids """
        pass
