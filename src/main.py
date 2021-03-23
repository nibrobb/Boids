import random as rand
import pygame
from config import *
from boid import Boid


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_RES)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.load_boid()


    def initialize(self):
        self.load_boid()
        self.all_sprites = pygame.sprite.Group()

    def load_boid(self):
        self.boid_img = pygame.Surface([BOID_WIDTH, BOID_HEIGHT])
        self.boid_img.fill(BLACK)
        self.boid_img.set_colorkey(BLACK)
        pygame.draw.polygon(self.boid_img, WHITE, BOID_SHAPE)

    def run(self):
        self.running = True
        while self.running:
            # self.spawn_boids(100, all_sprites)

            # Game logic goes here


            # Three rules of boids: Separation, Alignment, Cohesion
                # 1) separation: steer to avoid crowding local flockmates
                # 2) alignment: steer towards the average heading of local flockmates
                # 3) cohesion: steer to move towards the average position (center of mass) of local flockmates
            self.dt = self.clock.tick(FPS) / 1000.0
            self.events()
            self.update()
            self.draw()
    
    def events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    self.spawn_boid_on_click(pos)
                
    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BG_COLOR)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, sprite.pos)
        pygame.display.flip()


    def spawn_boid_on_click(self, pos):
        boid = Boid(self, pos)
        self.all_sprites.add(boid)

    def spawn_boids(self, n_boids : int):
        for i in range(n_boids):
            boid = Boid(self, (RNG_not_zero(0, SCREEN_X),
                                RNG_not_zero(0, SCREEN_Y)))
            self.all_sprites.add(boid)

    def draw_heading_vector(self, boid : Boid, vec : pygame.Vector2, color : (int, int, int)):
        pygame.draw.line(self.screen, color,
                        (boid.pos.x, boid.pos.y),
                        (boid.pos.x + vec.x * 50,
                        boid.pos.y + vec.y * 50), 3)

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
