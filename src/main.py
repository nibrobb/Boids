#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random as rand
import pygame
from config import *
from boid import Boid


class Game:
    """ A simple flocking simulator """
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_RES)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.dt = 0

    def initialize(self):
        """ Denne metoden setter opp alt som trengs for å kjøre simulasjonen """
        self.load_boid()
        self.all_sprites = pygame.sprite.Group()

    def load_boid(self):
        """ Laster inn en egendefinert boid polygon """

        # Lager en overflate for å tegne boiden på og setter bakgrunnsfargen gjennomsiktig.
        temp = pygame.Surface([BOID_WIDTH, BOID_HEIGHT], pygame.SRCALPHA)
        # Tegner en polygon fra punktene definert i config.py med heldekkende fyll
        pygame.draw.polygon(temp, WHITE, BOID_SHAPE, 0)

        # self.boid_img = pygame.transform.scale(self.boid_img, [int(0.9*BOID_WIDTH), int(0.9*BOID_HEIGHT)])
        self.boid_img = pygame.transform.rotozoom(temp, 0, 0.9)



    def run(self):
        """ Kjøres ved start, holdes kjørende til brukeren avslutter """
        self.running = True
        self.spawn_boids(50)
        _boid = Boid(self, (SCREEN_X/2, SCREEN_Y/2), (255, 0, 0))
        self.all_sprites.add(_boid)
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000.0
            self.events()
            self.update()
            self.draw()


    def events(self):
        """ Event handler """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                self.spawn_boid_on_click()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.quit()
                elif event.key == pygame.K_r:
                    self.reset()
                
    def update(self):
        """ Updates sprites """
        self.all_sprites.update()

    def draw(self):
        """ Draws all boids on the screen """
        self.screen.fill(BG_COLOR)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, (sprite.rect.x, sprite.rect.y))
        pygame.display.flip()


    def spawn_boid_on_click(self):
        """ Spawn a single boid at mouse position """
        pos = pygame.mouse.get_pos()
        boid = Boid(self, pos)
        self.all_sprites.add(boid)

    def spawn_boids(self, n_boids : int):
        """ Spawn `n' amount of boids at random positions """
        for i in range(n_boids):
            boid = Boid(self, (rand.randint(0, SCREEN_X),
                               rand.randint(0, SCREEN_Y)))
            self.all_sprites.add(boid)

    def draw_heading_vector(self, boid : Boid, vec):
        """ Supposed to draw a heading-vector in front of the boid """
        pygame.draw.line(self.screen, (255,0,0),
                        (boid.pos.x, boid.pos.y),
                        (boid.pos.x + vec.x,
                        boid.pos.y + vec.y), 3)

    def reset(self):
        """ Reset the game state """
        pass

    def quit(self):
        """ Quit """
        pygame.quit()

def RNG_not_zero(a, b):
    rng = rand.randint(a, b)
    if rng == 0:
        rng = 1
    return rng

if __name__ == '__main__':
    game = Game()
    while True:
        game.initialize()
        game.run()
