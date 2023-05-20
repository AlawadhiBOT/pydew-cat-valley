import pygame
import sys
from settings import *
from level import Level
import time


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Sprout land')
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_x]:
                    self.level.music.set_volume(0)
                if keys[pygame.K_c]:
                    self.level.music.set_volume(0.3)

                if keys[pygame.K_p]:
                    print(self.level.player.seed_inventory)

            dt = self.clock.tick(60) / 1000
            self.level.run(dt)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
