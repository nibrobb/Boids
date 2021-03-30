#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random as rand
from typing import Tuple
import pygame
from config import *
from boid import Boid


class Game:
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
        self.boid_img = pygame.Surface([BOID_WIDTH, BOID_HEIGHT], pygame.SRCALPHA)

        # Tegner en polygon fra punktene definert i config.py med heldekkende fyll
        pygame.draw.polygon(self.boid_img, WHITE, BOID_SHAPE, 0)

    def run(self):
        """ Kjøres ved start, holdes kjørende til brukeren avslutter """
        self.running = True
        self.spawn_boids(10)
        _boid = Boid(self, (SCREEN_X/2, SCREEN_Y/2), (255, 0, 0))
        self.all_sprites.add(_boid)
        ticker = 0
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000.0
            self.events()
            self.update()
            self.draw()
            ticker += self.dt*1000
            if ticker >= 1000:             # [Debug] Prints position, velocity and angle per second
                print(f"Pos:\t{_boid.pos}")
                print(f"Vel:\t{_boid.vel}")
                print(f"Angle:\t{_boid.angle}\n")
                ticker = 0

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                self.spawn_boid_on_click(pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.quit()
                
    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BG_COLOR)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, (sprite.rect.x, sprite.rect.y))
        pygame.display.flip()


    def spawn_boid_on_click(self, pos):
        boid = Boid(self, pos)
        self.all_sprites.add(boid)

    def spawn_boids(self, n_boids : int):
        for i in range(n_boids):
            boid = Boid(self, (rand.randint(0, SCREEN_X),
                               rand.randint(0, SCREEN_Y)))
            self.all_sprites.add(boid)

    def draw_heading_vector(self, boid : Boid, vec):
        pygame.draw.line(self.screen, (255,0,0),
                        (boid.pos.x, boid.pos.y),
                        (boid.pos.x + vec.x,
                        boid.pos.y + vec.y), 3)

    def quit(self):
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
