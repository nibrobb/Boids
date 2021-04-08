""" Simple boid simulation made by Robin Kristiansen (c) 2021 """
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random as rand
import pygame
from config import *
from boid import Boid
from hoik import Hoik


class Game:
    """ A simple flocking simulator """
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_RES)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.delta_time = 0
        # weights index 0, 1 and 2 are respectivly alignment, cohesion and separation
        self.weights = [ALIGNMENT, COHESION, SEPARATION]


    def initialize(self):
        """ Initializes boids and hoiks """
        self.load_boid()
        self.load_hoik()
        self.all_sprites = pygame.sprite.Group()
        self.all_boids = pygame.sprite.Group()
        self.all_hoiks = pygame.sprite.Group()


    def load_boid(self):
        """
        Loads a predefined set of coordinates and draws a polygon (boid) on a surface
        """

        # Creates a surface to draw the boid on and sets the background color to transparent
        boid_original = pygame.Surface([BOID_WIDTH, BOID_HEIGHT], pygame.SRCALPHA)
        # Draws a polygon from predefined points in config.py with solid fill
        pygame.draw.polygon(boid_original, WHITE, BOID_SHAPE, 0)
        # Scales down the size of the boid by 40%
        self.boid_img = pygame.transform.rotozoom(boid_original, 0, 0.6)


    def load_hoik(self):
        """ Loads the same shape as the boid, only this one with a color of red """
        hoik_original = pygame.Surface([BOID_WIDTH, BOID_HEIGHT], pygame.SRCALPHA)
        pygame.draw.polygon(hoik_original, RED, BOID_SHAPE, 0)
        self.hoik_img = pygame.transform.rotozoom(hoik_original, 0, 0.6)


    def run(self):
        """ Runs the simulation """
        self.running = True
        self.spawn_boids(BOIDS_TO_SPAWN)
        self.spawn_hoik(HOIKS_TO_SPAWN)

        while self.running:
            self.delta_time = self.clock.tick(FPS) / 1000.0
            self.events()
            self.update()
            self.draw()


    def events(self):
        """ Event handler """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:       # Handle quit event
                self.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.spawn_boid_on_click()      # Mouse button click spawns boid
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:     # Press Q to quit
                    self.quit()
                elif event.key == pygame.K_r:   # Press R to restart
                    self.reset()

        # --------------- Weight adjustment --------------- #
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:            #
            self.weights[0] -= 0.01     # Decrease alignment
        if keys[pygame.K_2]:            #
            self.weights[0] += 0.01     # Increase alignment
        if keys[pygame.K_3]:            #
            self.weights[1] -= 0.01     # Decrease cohesion
        if keys[pygame.K_4]:            #
            self.weights[1] += 0.01     # Increase cohesion
        if keys[pygame.K_5]:            #
            self.weights[2] -= 0.01     # Decrease separation
        if keys[pygame.K_6]:            #
            self.weights[2] += 0.01     # Increase separation


    def update(self):
        """ Updates sprites """
        self.all_sprites.update()


    def draw(self):
        """ Draws all sprites on screen """
        self.screen.fill(BG_COLOR)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, (sprite.rect.x, sprite.rect.y))

        # Print info like fps, number of boids and hoiks, and weights
        self.print_info((0,0))
        
        pygame.display.flip()


    def print_info(self, pos):
        """ Prints info """
        text_size = 20
        font_family = "Comic Sans MS"

        info_text = []

        fps_text = self.setup_font("Frame rate: {:.0f}".format(self.clock.get_fps()), font_family, text_size, WHITE)
        info_text.append(fps_text)

        amount_of_boids = self.setup_font("Boids: {}".format(len(self.all_boids)), font_family, text_size, WHITE)
        info_text.append(amount_of_boids)

        amount_of_hoiks = self.setup_font("Hoiks: {}".format(len(self.all_hoiks)), font_family, text_size, WHITE)
        info_text.append(amount_of_hoiks)

        alignment_text = self.setup_font("Alignment weight: {:.2f}".format(self.weights[0]), font_family, text_size, WHITE)
        info_text.append(alignment_text)

        cohesion_text = self.setup_font("Cohesion weight: {:.2f}".format(self.weights[1]), font_family, text_size, WHITE)
        info_text.append(cohesion_text)

        separation_text = self.setup_font("Separation weight: {:.2f}".format(self.weights[2]), font_family, text_size, WHITE)
        info_text.append(separation_text)
        
        self.blit_text(info_text, pos)


    def setup_font(self, text, font, size, color) -> pygame.Surface:
        """ Returns a surface with the chosen text """
        text_font = pygame.font.SysFont(font, size)
        text_surface = text_font.render(text, True, color)
        return text_surface

    def blit_text(self, text_list, pos):
        """ Prints all the text in text_list to the screen """
        offset = 0
        background_width = 0
        background_height = 0

        for surface in text_list:
            background_width = max(background_width, surface.get_width())
            background_height += surface.get_height()

        background = pygame.Surface((background_width + 8, background_height + 8))
        background.fill(BLACK)
        self.screen.blit(background, pos)

        for text in text_list:
            self.screen.blit(text, (pos[0] + 4, pos[1] + offset))
            offset += text.get_height()

    def spawn_boid_on_click(self):
        """ Spawn a single boid at mouse position """
        pos = pygame.mouse.get_pos()
        boid = Boid(self, pos)
        self.all_boids.add(boid)
        self.all_sprites.add(boid)

    def spawn_boids(self, n_boids : int):
        """ Spawn `n' amount of boids at random positions """
        for i in range(n_boids):
            boid = Boid(self, (rand.randint(0, SCREEN_X),
                               rand.randint(0, SCREEN_Y)))
            self.all_boids.add(boid)
            self.all_sprites.add(boid)
        
    def spawn_hoik(self, n_hoiks : int):
        """ Spawn a n hoiks """
        for i in range(n_hoiks):
            hoik = Hoik(self, (rand.randint(0, SCREEN_X),
                            rand.randint(0, SCREEN_Y) ) )
            self.all_hoiks.add(hoik)
            self.all_sprites.add(hoik)



    def reset(self):
        """ Reset game state """
        self.empty_sprite_gropus()                          # Empties sprite groups
        self.weights = [ALIGNMENT, COHESION, SEPARATION]    # Resets weights
        self.spawn_boids(BOIDS_TO_SPAWN)                    # Spawns new boid(s)
        self.spawn_hoik(HOIKS_TO_SPAWN)                     # Spawns new hoik(s)

    def empty_sprite_gropus(self):
        """ Empties sprite groups """
        self.all_boids.empty()
        self.all_hoiks.empty()
        self.all_sprites.empty()

    def quit(self):
        """ Quit """
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    while True:
        game.initialize()
        game.run()
