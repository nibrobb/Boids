import pygame
from config import *
from boid import Boid

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(screen_res)
        self.clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            
            self.screen.fill((12, 23, 34))

            # Game logic goes here
            all_sprites = pygame.sprite.Group()

            boid = Boid((255, 255, 255), 5)
            boid.rect.x, boid.rect.y = screen_res[0] // 2, screen_res[1] // 2

            all_sprites.add(boid)
            all_sprites.update()

            all_sprites.draw(self.screen)
            self.clock.tick(60)
            pygame.display.flip()


if __name__ == '__main__':
    Game = Game()
