import pygame
from config import *

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
            self.clock.tick(60)
            pygame.display.flip()


if __name__ == '__main__':
    Game = Game()
