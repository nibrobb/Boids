import pygame
from config import *
from boid import Boid

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_RES)
        self.clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            
            self.screen.fill((12, 23, 34))

            # Game logic goes here
            all_sprites = pygame.sprite.Group()

            boid = Boid((WHITE), 5)
            boid.rect.x, boid.rect.y = (SCREEN_RES[0] / 2) - boid.width/2, (SCREEN_RES[1] / 2) - boid.height / 2
            pygame.draw.line(self.screen, (255, 255, 255), (SCREEN_RES[0]/2, 0), (SCREEN_RES[0]/2, SCREEN_RES[1]), 1)

            all_sprites.add(boid)
            all_sprites.update()

            all_sprites.draw(self.screen)
            self.clock.tick(60)
            pygame.display.flip()


if __name__ == '__main__':
    Game = Game()
