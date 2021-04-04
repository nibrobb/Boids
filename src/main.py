#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import get_cache_token
import random as rand
from typing import Tuple, Optional
import pygame
from pygame.constants import K_BACKSLASH
from config import *
from boid import Boid


class Game:
    """ A simple flocking simulator """
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_RES)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.delta_time = 0
        self.weights = [1, 1, 1]

    def initialize(self):
        """ Denne metoden setter opp alt som trengs for å kjøre simulasjonen """
        self.load_boid()
        self.all_sprites = pygame.sprite.Group()

    def load_boid(self):
        """ Laster inn en egendefinert boid polygon """
        # Lager en overflate for å tegne boiden på og setter bakgrunnsfargen gjennomsiktig.
        boid_original = pygame.Surface([BOID_WIDTH, BOID_HEIGHT], pygame.SRCALPHA)
        # Tegner en polygon fra punktene definert i config.py med heldekkende fyll
        pygame.draw.polygon(boid_original, WHITE, BOID_SHAPE, 0)

        # self.boid_img = pygame.transform.scale(self.boid_img, [int(0.9*BOID_WIDTH), int(0.9*BOID_HEIGHT)])
        # Reduserer størrelsen på boidsa med 40% (dermed skala på 0.6).
        self.boid_img = pygame.transform.rotozoom(boid_original, 0, 0.6)



    def run(self):
        """ Kjøres ved start, holdes kjørende til brukeren avslutter """
        self.running = True
        self.spawn_boids(100)

        while self.running:
            self.delta_time = self.clock.tick(FPS) / 1000.0
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
        keys = pygame.key.get_pressed()
        # if keys[pygame.K_KP_PLUS]:
            # self.master_coh_weight += 0.01
        # elif keys[pygame.K_KP_MINUS]:
            # self.master_coh_weight -= 0.01


    def update(self):
        """ Updates sprites """
        self.all_sprites.update()


    def draw(self):
        """ Draws all boids on the screen """
        self.screen.fill(BG_COLOR)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, (sprite.rect.x, sprite.rect.y))


        # Print all the weights
        self.print_weights()
        self.print_weights((600,600))
        
        
        pygame.display.flip()

    def print_weights(self, pos : Tuple[int, int] = (8, 8)):
        """ Prints all three weights in the upper left hand corner """
        text_size = 20
        font_family = "Comic Sans MS"

        align_font = pygame.font.SysFont(font_family, text_size)
        align_surface = align_font.render(f"Alignment weight: {self.weights[0]}", True, WHITE)

        coh_font = pygame.font.SysFont(font_family, text_size)
        coh_surface = coh_font.render(f"Cohesion weight: {self.weights[1]}", True, WHITE)

        sep_font = pygame.font.SysFont(font_family, text_size)
        sep_surface = sep_font.render(f"Separation weight: {self.weights[2]}", True, WHITE)

        background = pygame.Surface((max(align_surface.get_width(),
                                        coh_surface.get_width(),
                                        sep_surface.get_width()),
                                        (align_surface.get_height() +
                                        coh_surface.get_height() +
                                        sep_surface.get_height())))
        background.fill((0,0,0))

        self.screen.blit(background, pos)

        self.screen.blit(align_surface, (pos[0], pos[1]) )
        self.screen.blit(coh_surface,   (pos[0], pos[1] + align_surface.get_height() ) )
        self.screen.blit(sep_surface,   (pos[0], pos[1] + align_surface.get_height() + coh_surface.get_height() ) )


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

    def draw_heading_vector(self, boid : Boid, vec : pygame.Vector2):
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

def RNG_not_zero(a : int, b : int):
    rng = rand.randint(a, b)
    if rng == 0:
        rng = 1
    return rng

if __name__ == '__main__':
    game = Game()
    while True:
        game.initialize()
        game.run()
