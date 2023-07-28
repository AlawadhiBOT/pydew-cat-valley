import pygame
import sys
from time import sleep


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0),
                                              pygame.FULLSCREEN)
        pygame.display.set_caption('PyDew Cat Valley')

        self.clock = pygame.time.Clock()

        from code.level import Level
        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_x]:
                    self.level.active_music.set_volume(0)
                if keys[pygame.K_c]:
                    self.level.active_music.set_volume(0.3)

                if keys[pygame.K_o]:
                    self.level.soil_layer.save_soil_state()
                if keys[pygame.K_r]:
                    self.level.soil_layer.read_soil_state()

            dt = self.clock.tick(60) / 1000
            self.level.run(dt)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
