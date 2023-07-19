import time

import pygame
from settings import *
from support import import_folder
from sprites import Generic
from random import randint, choice


class Sky:
    """
    This class is used to darken the map when it becomes dark
    """

    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.full_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.start_color = [255, 255, 255]
        self.end_color = (38, 101, 189)
        self.time = time.time()
        self.usable_time = [77, 777]
        self.font = pygame.font.Font('../font/LycheeSoda.ttf', 30)
        self.text = self.font.render(f"{self.usable_time[0]}"
                                     f":{self.usable_time[1]}", False,
                                     "Black")
        self.text_rect = self.text.get_rect(topright=
                                            (self.full_surf.get_width(), 0))
        self.night = False
        self.music_swap = False

        # TODO add parameter to handle calculation of days since start

    def calculate_time(self, curr_time: float, seconds_in_day, starting_hour,
                       seconds_per_hour):
        """
        Calculates the time of the user, and displays it.
        """
        # this means that in every day 5 seconds will equal to one-hour
        # day starts at 6am, so 120 - 6 * 5 = 90
        # at 12am (00,   time does not update)
        # first cell in usable is hour, second is seconds. Day starts at 6, 0

        self.usable_time[0] = int((((curr_time - self.time) // seconds_per_hour)
                                   + starting_hour))

        self.usable_time[1] = int(((curr_time - self.time) % seconds_per_hour
                                   ) * 60 // seconds_per_hour)

        if self.usable_time[0] >= 24:
            self.usable_time[0] = 23
            self.usable_time[1] = 59

    def reset_time(self):
        """Resets the time of the day"""
        self.time = time.time()
    def display(self, dt: float):
        curr_time = time.time()
        seconds_in_day = 90
        starting_hour = 6
        seconds_per_hour = 5

        self.calculate_time(curr_time, seconds_in_day, starting_hour,
                            seconds_per_hour)

        for index, value in enumerate(self.end_color):
            if self.start_color[index] > value and self.usable_time[0] > 18:
                self.start_color[index] -= 2 * dt * 10

        if curr_time - self.time >= seconds_in_day:
            self.night = True

        self.full_surf.fill(self.start_color)
        self.text = self.font.render(f"{self.usable_time[0]}"
                                     f":{self.usable_time[1]}", False,
                                     "Black")
        self.display_surface.blit(self.text, self.text_rect)
        self.display_surface.blit(self.full_surf, (0, 0),
                                  special_flags=pygame.BLEND_RGBA_MULT)


class Drop(Generic):
    """
    This class is used to simulate rain in the air
    """

    def __init__(self, surf, pos, moving, groups, z):

        # general setup
        super().__init__(pos, surf, groups, z)
        self.lifetime = randint(400, 500)
        self.start_time = pygame.time.get_ticks()

        # moving
        self.moving = moving
        if self.moving:
            self.pos = pygame.math.Vector2(self.rect.topleft)
            self.direction = pygame.math.Vector2(-2, 4)
            self.speed = randint(200, 250)

    def update(self, dt: float):
        # movement
        if self.moving:
            self.pos += self.direction * self.speed * dt
            self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        # timer
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()


class Rain:
    """
    This class is used to simulate rain drops (on the ground)
    """

    def __init__(self, all_sprites: pygame.sprite.Group):
        self.all_sprites = all_sprites
        self.rain_drops = import_folder('../graphics/rain/drops/')
        self.rain = import_folder('../graphics/rain/floor/')
        self.floor_w, self.floor_h = pygame.image.load(
            '../graphics/world/ground.png').get_size()

    def create_floor(self):
        Drop(surf=choice(self.rain),
             pos=(randint(0, self.floor_w), randint(0, self.floor_h)),
             moving=False,
             groups=self.all_sprites,
             z=LAYERS['rain floor'])

    def create_drops(self):
        Drop(surf=choice(self.rain_drops),
             pos=(randint(0, self.floor_w), randint(0, self.floor_h)),
             moving=True,
             groups=self.all_sprites,
             z=LAYERS['rain drops'])

    def update(self):
        self.create_floor()
        self.create_drops()
