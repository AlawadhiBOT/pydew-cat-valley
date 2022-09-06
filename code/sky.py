import time

import pygame
from settings import *
from support import import_folder
from sprites import Generic
from random import randint, choice


class Sky:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.full_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.start_color = [255, 255, 255]
        self.end_color = (38, 101, 189)
        self.time = time.time()
        self.night = False
        self.music_swap = False

    def display(self, dt):
        for index, value in enumerate(self.end_color):
            if self.start_color[index] > value:
                self.start_color[index] -= 2 * dt

        if time.time() - self.time >= 45:
            self.night = True

        self.full_surf.fill(self.start_color)
        self.display_surface.blit(self.full_surf, (0, 0),
                                  special_flags=pygame.BLEND_RGBA_MULT)


class Drop(Generic):
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

    def update(self, dt):
        # movement
        if self.moving:
            self.pos += self.direction * self.speed * dt
            self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        # timer
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()


class Rain:

    def __init__(self, all_sprites):
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
