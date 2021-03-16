import random as rand
import pygame
from config import *
from boid import Boid

class Boids:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_RES)
        self.clock = pygame.time.Clock()

        all_sprites = pygame.sprite.Group()
        # self.spawn_boids(100, all_sprites)

        def draw_heading_vector(boid : Boid, vec : pygame.Vector2, color):
                pygame.draw.line(self.screen, color,
                                (boid.pos.x, boid.pos.y),
                                (boid.pos.x + vec.x * 50,
                                boid.pos.y + vec.y * 50), 3)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    make_boid(pos)

            def make_boid(pos):
                boid = Boid(WHITE, pos, (rand.randint(-5, 5), rand.randint(-5, 5)) )
                all_sprites.add(boid)


            self.screen.fill((12, 23, 34))

            # Game logic goes here

            boids = all_sprites.sprites()
            for boid in boids:
                draw_heading_vector(boid, boid.direction, (0,0,255))

            # Three rules of boids: Separation, Alignment, Cohesion
                # 1) separation: steer to avoid crowding local flockmates
                # 2) alignment: steer towards the average heading of local flockmates
                # 3) cohesion: steer to move towards the average position (center of mass) of local flockmates
            
            all_sprites.update()
            all_sprites.draw(self.screen)
            
            self.clock.tick(60)
            pygame.display.flip()


    def spawn_boids(self, n_boids : int, sprite_group : pygame.sprite.Group):
        for i in range(n_boids):
            boid = Boid(WHITE, (rand.randint(0, SCREEN_X),
                                rand.randint(0, SCREEN_Y)),
                               (rand.randint(-5, 5),
                                rand.randint(-5, 5)))
            sprite_group.add(boid)


if __name__ == '__main__':
    start = Boids()
