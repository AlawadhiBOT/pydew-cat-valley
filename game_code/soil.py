from typing import Callable

from game_code.settings import *
from pytmx.util_pygame import load_pygame
from game_code.support import *
from random import choice
import json
from pygame.math import Vector2
from os import path


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
                 soil, check_watered: Callable, age):
        super().__init__(groups)

        # setup
        self.plant_type = plant_type
        self.frames = import_folder(path.join(CURR_PATH, 'graphics', 'fruit',
                                              plant_type)
                                    )
        self.soil = soil
        self.check_watered = check_watered

        # plant growth
        self.age = 0 if age is None else age
        self.max_age = len(self.frames) - 1
        self.grow_speed = GROW_SPEED[plant_type]
        self.harvestable = False

        # sprite setup
        self.image = self.frames[self.age]
        self.y_offset = PLANT_OFFSET[self.plant_type]
        self.rect = self.image.get_rect(midbottom=soil.rect.midbottom +
                                                  Vector2(0, self.y_offset))
        self.z = LAYERS['ground plant']

    def __str__(self):
        return f'{self.plant_type},{self.age},' \
               f'{self.rect.left},{self.rect.top}'

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
            if self.age > 2:
                self.rect = self.image.get_rect(midbottom=
                                                self.soil.rect.midbottom +
                                                Vector2
                                                (0, self.y_offset))
            else:
                self.rect = self.image.get_rect(midbottom=
                                                self.soil.rect.midbottom +
                                                Vector2
                                                (0, self.y_offset +
                                                 BIG_PLANT_OFFSET
                                                 [self.plant_type]))


# noinspection PyCompatibility
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
        self.soil_surfs = import_folder_dict(path.join(CURR_PATH, 'graphics',
                                                       'soil'))
        self.water_surfs = import_folder(path.join(CURR_PATH, 'graphics',
                                                   'soil_water'))

        self.create_soil_grid()
        self.create_hit_rects()

        # bools
        self.raining = False

        # sounds
        self.hoe_sound = pygame.mixer.Sound(path.join(CURR_PATH, 'audio',
                                                      'hoe.wav'))
        self.hoe_sound.set_volume(0.1)
        self.plant_sound = pygame.mixer.Sound(path.join(CURR_PATH, 'audio',
                                                        'plant.wav'))
        self.plant_sound.set_volume(0.2)

        # read saved data
        self.read_soil_state()

    def create_soil_grid(self):
        ground = pygame.image.load(path.join(CURR_PATH, 'graphics',
                                             'world', 'ground 2.png')
                                   ).convert_alpha()
        h_tiles = ground.get_width() // TILE_SIZE
        v_tiles = ground.get_height() // TILE_SIZE

        self.grid = [[[] for col in range(h_tiles)] for row in range(v_tiles)]
        for x, y, _ in load_pygame(path.join(CURR_PATH, 'data',
                                             'map.tmx')).get_layer_by_name(
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

    def save_soil_state(self):
        """
        Function written to save state of soil tiles
        :return: NoneType
        """
        with open(path.join(CURR_PATH, 'data', 'farmed_land.txt'), "w") as file:
            for row in self.grid:
                ln = ""
                for cell in row:
                    mini_ln = ""
                    for item in cell:
                        if item not in "WP":
                            mini_ln += str(item)
                    ln += mini_ln + "|"
                ln += '\n'
                file.write(ln)

        lst = [[str(plant)] for plant in self.plant_sprites]
        jason_file = json.dumps(lst, indent=4)

        with open(path.join(CURR_PATH, 'data', 'plant_in_soil.json'), "w") as f:
            f.write(jason_file)

    def read_soil_state(self):
        """
        Function written to read save state of soil tiles
        :return: NoneType
        """
        with open(path.join(CURR_PATH, 'data', 'farmed_land.txt'), "r") as file:
            ctr = 0
            for line in file:
                arr_line = line.split("|")[:-1]
                self.grid[ctr] = [[state for state in item] for
                                  item in arr_line]
                ctr += 1
        self.create_soil_tiles()

        with open(path.join(CURR_PATH, 'data', 'plant_in_soil.json'), "r") as f:
            lst = []
            for entry in json.load(f):
                lst.append(entry[0].split(','))

        for item in lst:
            selected_seed = item[0]
            age = int(item[1])
            target_pos = (int(item[2]) + TILE_SIZE // 2,
                          int(item[3]) + TILE_SIZE // 2)
            self.plant_seed(target_pos, selected_seed, age)

        if self.raining:
            self.water_all()

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

    def plant_seed(self, target_pos, selected_seed: str, age: int = None):
        """
        Plants a seed in the relevant soil tile
        :param target_pos: target location of seed planting
        :param selected_seed: the seed type which will be planted
        :param age: int indicating age of plant
        :return: boolean indicating success or fail in planting
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
                          self.check_watered, age)
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
