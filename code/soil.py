from typing import Callable

import pygame
from settings import *
from pytmx.util_pygame import load_pygame
from support import *
from random import choice


class SoilTile(pygame.sprite.Sprite):

    def __init__(self, pos, surf: pygame.surface,
                 groups: list[pygame.sprite.Group]):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['soil']


class WaterTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf: pygame.surface, groups: pygame.sprite.Group):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['soil water']


class Plant(pygame.sprite.Sprite):
    def __init__(self, plant_type, groups: list[pygame.sprite.Group],
                 soil, check_watered: Callable):
        super().__init__(groups)

        # setup
        self.plant_type = plant_type
        self.frames = import_folder(f'../graphics/fruit/{plant_type}')
        self.soil = soil
        self.check_watered = check_watered

        # plant growth
        self.age = 0
        self.max_age = len(self.frames) - 1
        self.grow_speed = GROW_SPEED[plant_type]
        self.harvestable = False

        # sprite setup
        self.image = self.frames[self.age]
        self.y_offset = -16 if plant_type == "corn" else -8
        self.rect = self.image.get_rect(midbottom=soil.rect.midbottom +
                                                  pygame.math.Vector2(0, self.y_offset))
        self.z = LAYERS['ground plant']

    def grow(self):
        if self.check_watered(self.rect.center):
            self.age += self.grow_speed

            if int(self.age) > 0:
                self.z = LAYERS['main']
                self.hitbox = self.rect.copy().inflate(-26,
                                                       -self.rect.height * 0.4)

            if self.age >= self.max_age:
                self.age = self.max_age
                self.harvestable = True

            self.image = self.frames[int(self.age)]
            self.rect = self.image.get_rect(midbottom=self.soil.rect.midbottom +
                                                      pygame.math.Vector2
                                                      (0, self.y_offset))


class SoilLayer:
    grid: list[list[str]]

    def __init__(self, all_sprites: pygame.sprite.Group,
                 collision_sprites: pygame.sprite.Group):
        # sprite groups
        self.all_sprites = all_sprites
        self.collision_sprites = collision_sprites
        self.soil_sprites = pygame.sprite.Group()
        self.water_sprites = pygame.sprite.Group()
        self.plant_sprites = pygame.sprite.Group()

        # graphics
        self.soil_surfs = import_folder_dict('../graphics/soil')
        self.water_surfs = import_folder('../graphics/soil_water')

        self.create_soil_grid()
        self.create_hit_rects()


        # sounds
        self.hoe_sound = pygame.mixer.Sound('../audio/hoe.wav')
        self.hoe_sound.set_volume(0.1)
        self.plant_sound = pygame.mixer.Sound('../audio/plant.wav')
        self.plant_sound.set_volume(0.2)

    def create_soil_grid(self):
        ground = pygame.image.load('../graphics/world/ground 2.png')
        h_tiles = ground.get_width() // TILE_SIZE
        v_tiles = ground.get_height() // TILE_SIZE

        self.grid = [[[] for col in range(h_tiles)] for row in range(v_tiles)]
        for x, y, _ in load_pygame('../data/map.tmx').get_layer_by_name(
                'Farmable').tiles():
            self.grid[y][x].append('F')
        # for row in self.grid:
        #     print(row)

    def create_hit_rects(self):
        self.hit_rects = []
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'F' in cell:
                    x = index_col * TILE_SIZE
                    y = index_row * TILE_SIZE
                    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    self.hit_rects.append(rect)

    def get_hit(self, point):
        for rect in self.hit_rects:
            if rect.collidepoint(point):
                self.hoe_sound.play()
                x = rect.x // TILE_SIZE
                y = rect.y // TILE_SIZE

                if 'F' in self.grid[y][x]:
                    self.grid[y][x].append('X')
                    self.create_soil_tiles()
                    if self.raining:
                        self.water_all()

    def water(self, target_pos):
        for soil_sprite in self.soil_sprites:
            if soil_sprite.rect.collidepoint(target_pos):
                # add tree to soil grid
                x = soil_sprite.rect.x // TILE_SIZE
                y = soil_sprite.rect.y // TILE_SIZE
                self.grid[y][x].append('W')

                # water sprite
                pos = soil_sprite.rect.topleft
                surf = choice(self.water_surfs)
                WaterTile(pos, surf, [self.all_sprites, self.water_sprites])

    def water_all(self):
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'X' in cell and 'W' not in cell:
                    cell.append('W')

                    x = index_col * TILE_SIZE
                    y = index_row * TILE_SIZE
                    surf = choice(self.water_surfs)
                    WaterTile((x, y), surf,
                              [self.all_sprites, self.water_sprites])

    def remove_water(self):

        # destroy all water sprites
        for sprite in self.water_sprites.sprites():
            sprite.kill()
        # clean grid
        for row in self.grid:
            for cell in row:
                if 'W' in cell:
                    cell.remove('W')

    def check_watered(self, pos):
        x = pos[0] // TILE_SIZE
        y = pos[1] // TILE_SIZE
        cell = self.grid[y][x]
        is_watered = 'W' in cell
        return is_watered

    def plant_seed(self, target_pos, selected_seed: str):
        """
        Plants a seed in the relevant soil tile
        :param target_pos: target location of seed planting
        :param selected_seed: the seed type which will be planted
        :return: None
        """
        for soil_sprite in self.soil_sprites:
            if soil_sprite.rect.collidepoint(target_pos):
                self.plant_sound.play()

                x = soil_sprite.rect.x // TILE_SIZE
                y = soil_sprite.rect.y // TILE_SIZE

                if 'P' not in self.grid[y][x]:
                    self.grid[y][x].append('P')
                    Plant(selected_seed,
                          [self.all_sprites, self.plant_sprites,
                           self.collision_sprites], soil_sprite,
                          self.check_watered)
                    return True

        return False

    def update_plants(self):
        """
        Grows the plants, originally used for night cycle
        :return: None
        """
        for plant in self.plant_sprites.sprites():
            plant.grow()

    def create_soil_tiles(self):
        """
        Sets the tile of soil based on what other soil tiles there are beside it
        :return: None
        """
        self.soil_sprites.empty()
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'X' in cell:

                    # tile options
                    t = 'X' in self.grid[index_row - 1][index_col]
                    b = 'X' in self.grid[index_row + 1][index_col]
                    r = 'X' in row[index_col + 1]
                    l = 'X' in row[index_col - 1]

                    tile_type = 'o'

                    # switch case rather than if statement (added 27-05-2023)
                    match (t, l, b, r):
                        # all sides
                        case (True, True, True, True):
                            tile_type = 'x'

                        # horizontal tiles only
                        case (False, True, False, False):
                            tile_type = 'r'

                        case (False, False, False, True):
                            tile_type = 'l'

                        case (False, True, False, True):
                            tile_type = 'lr'

                        # vertical tiles only
                        case (True, False, False, False):
                            tile_type = 'b'
                        case (False, False, True, False):
                            tile_type = 't'
                        case (True, False, True, False):
                            tile_type = 'tb'

                        # corners
                        case (False, True, True, False):
                            tile_type = 'tr'
                        case (False, False, True, True):
                            tile_type = 'tl'
                        case (True, True, False, False):
                            tile_type = 'br'
                        case (True, False, False, True):
                            tile_type = 'bl'

                        # T shapes
                        case (True, False, True, True):
                            tile_type = 'tbr'
                        case (True, True, True, False):
                            tile_type = 'tbl'
                        case (True, True, False, True):
                            tile_type = 'lrb'
                        case (False, True, True, True):
                            tile_type = 'lrt'

                    SoilTile(pos=(index_col * TILE_SIZE, index_row * TILE_SIZE),
                             surf=self.soil_surfs[tile_type],
                             groups=[self.all_sprites, self.soil_sprites])
