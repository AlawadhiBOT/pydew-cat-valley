import pygame
import sys
import importlib
import subprocess


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


def check_dependencies(dependencies):
    missing_dependencies = []
    for dependency in dependencies:
        try:
            importlib.import_module(dependency)
        except ImportError:
            missing_dependencies.append(dependency)
    return missing_dependencies


def install_dependencies(dependencies):
    for depend in dependencies:
        print(f"Installing {depend}...")
        try:
            subprocess.check_call(
                [sys.executable, '-m', 'pip', 'install', depend])
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {depend}. Error: {e}")
            sys.exit(1)


if __name__ == '__main__':
    required_dependencies = ['pygame',
                             'pytmx']  # Add other dependencies as needed

    missing_dependencies = check_dependencies(required_dependencies)
    if missing_dependencies:
        print("Error: The following dependencies are missing:")
        for dependency in missing_dependencies:
            print(f"- {dependency}")
        print("Attempting to install missing dependencies...")
        install_dependencies(missing_dependencies)
        print("Dependencies installed successfully.")
    game = Game()
    game.run()
