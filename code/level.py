import pygame
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic, Water, WildFlower, Tree, Interaction, Particle
from mobs import Slime, Cow
from pytmx.util_pygame import load_pygame
from support import *
from transition import Transition
from soil import SoilLayer
from sky import Rain, Sky
from random import randint
from menu import Menu, Inventory


class Level:
    def __init__(self):
        # Get display surface
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.tree_sprites = pygame.sprite.Group()
        self.water_sprites = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group()
        self.slime_sprites = pygame.sprite.Group()  # used in forest, for now
        self.cow_sprites = pygame.sprite.Group()

        self.soil_layer = None
        self.level_no = 0

        # inventory
        self.inventory = None
        self.overlay = None
        self.held_items = ['hoe', 'axe', 'water', 'fishing', 'wheat']

        # music
        self.success = pygame.mixer.Sound('../audio/success.wav')
        self.success.set_volume(0.3)
        self.music = pygame.mixer.Sound('../audio/music.mp3')
        self.music.set_volume(0.3)
        self.music.play(loops=-1)
        self.night_music = pygame.mixer.Sound('../audio/nighttime.wav')
        self.fishing_theme = pygame.mixer.Sound('../audio/fishing theme.mp3')
        self.forest_theme = pygame.mixer.Sound('../audio/bg.mp3')
        self.active_music = self.music
        self.fishing_theme_on = False

        # mobs stuff
        self.mob_area = {}

        # setup
        self.setup()

    def setup(self):
        """
        Sets up the world using TMX
        :param level_no: This refers to the current location, by default is 0
        1 will be used for forest map
        """
        if self.level_no == MAP_NUMBERS["Starting"]:
            self.all_sprites = CameraGroup()
            self.collision_sprites.empty()
            self.tree_sprites.empty()
            self.water_sprites.empty()
            self.interaction_sprites.empty()
            self.slime_sprites.empty()  # used in forest, for now
            self.cow_sprites.empty()

            self.soil_layer = SoilLayer(self.all_sprites,
                                        self.collision_sprites)

            tmx_data = load_pygame('../data/map.tmx')

            # house
            for layer in ['HouseFloor', 'HouseFurnitureBottom']:
                for x, y, surf in tmx_data.get_layer_by_name(layer) \
                        .tiles():
                    Generic((x * TILE_SIZE, y * TILE_SIZE), surf,
                            self.all_sprites,
                            LAYERS['house bottom'])

            for layer in ['HouseWalls', 'HouseFurnitureTop']:
                for x, y, surf in tmx_data.get_layer_by_name(layer) \
                        .tiles():
                    Generic((x * TILE_SIZE, y * TILE_SIZE), surf,
                            self.all_sprites)

            # Fence
            for x, y, surf in tmx_data.get_layer_by_name('Fence').tiles():
                Generic((x * TILE_SIZE, y * TILE_SIZE), surf,
                        [self.all_sprites, self.collision_sprites])

            # Water
            water_frames = import_folder('../graphics/water')
            for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
                Water((x * TILE_SIZE, y * TILE_SIZE), water_frames,
                      [self.all_sprites, self.water_sprites])

            # # Port
            # for x,y, surf in tmx_data.get_layer_by_name('Port').tiles():
            #     Port((x * TILE_SIZE, y * TILE_SIZE), self.all_sprites)

            # Trees
            for obj in tmx_data.get_layer_by_name('Trees'):
                Tree(
                    pos=(obj.x, obj.y),
                    surf=obj.image,
                    groups=[self.all_sprites, self.collision_sprites,
                            self.tree_sprites],
                    name=obj.name,
                    player_add=self.player_add)

            # WildFlowers
            for obj in tmx_data.get_layer_by_name('Decoration'):
                WildFlower((obj.x, obj.y), obj.image,
                           [self.all_sprites, self.collision_sprites])

            # collision tiles
            for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():
                Generic((x * TILE_SIZE, y * TILE_SIZE), pygame.Surface(
                    (TILE_SIZE, TILE_SIZE)), self.collision_sprites)

            # Player
            sprite_dict = {"group": self.all_sprites,
                           "collision_sprites": self.collision_sprites,
                           "tree_sprites": self.tree_sprites,
                           "water_sprites": self.water_sprites,
                           "interaction": self.interaction_sprites,
                           "soil_layer": self.soil_layer,
                           "slime_sprites": self.slime_sprites,
                           "cow_sprites": self.cow_sprites}
            for obj in tmx_data.get_layer_by_name('Player'):
                if obj.name == 'Start':
                    self.player = Player(pos=(obj.x, obj.y),
                                         sprite_dict=sprite_dict,
                                         toggle_shop=self.toggle_shop,
                                         toggle_inventory=self.toggle_inventory,
                                         get_map_level=self.get_map_number,
                                         set_map_level=self.set_map_number,
                                         play_fishing_theme=
                                         self.play_fishing_theme)
                elif obj.name == 'Bed':
                    Interaction((obj.x, obj.y), (obj.width, obj.height),
                                self.interaction_sprites, obj.name)

                elif obj.name == 'Trader':
                    Interaction((obj.x, obj.y), (obj.width, obj.height),
                                self.interaction_sprites, obj.name)

                elif obj.name == 'Forest':
                    Interaction((obj.x, obj.y), (obj.width, obj.height),
                                self.interaction_sprites, obj.name)

                elif obj.name == 'Cow':
                    cow_frames = {"idle": import_folder('../graphics/big_cow/'
                                                        'idle'),
                                  "move_left": import_folder(
                                      '../graphics/big_cow/'
                                      'move_left'),
                                  "move_right": import_folder(
                                      '../graphics/big_cow/'
                                      'move_right'),
                                  "sit": import_folder(
                                      '../graphics/big_cow/'
                                      'sit'),
                                  "sit_idle": import_folder(
                                      '../graphics/big_cow/'
                                      'sit_idle'),
                                  "sleep": import_folder(
                                      '../graphics/big_cow/'
                                      'sleep'),
                                  "stand_up": import_folder(
                                      '../graphics/big_cow/'
                                      'stand_up'),
                                  "grass_find": import_folder(
                                      '../graphics/big_cow/'
                                      'grass_find'),
                                  "munch": import_folder(
                                      '../graphics/big_cow/'
                                      'munch'),
                                  }

                    Cow(pos=(obj.x + TILE_SIZE // 4, obj.y + TILE_SIZE // 4),
                        frames=cow_frames,
                        groups=[self.all_sprites, self.cow_sprites],
                        z=LAYERS['main'],
                        player_pos=self.player.get_pos)

            Generic(
                pos=(0, 0),
                surf=pygame.image.load(
                    '../graphics/world/ground 2.png').convert_alpha(),
                groups=self.all_sprites, z=LAYERS['ground'])

            self.active_music.stop()
            self.active_music = self.music
            self.active_music.set_volume(0.3)
            self.active_music.play()

            self.overlay = Overlay(self.player, self.held_items)
            self.transition = Transition(self.reset, self.player)

            # sky
            self.rain = Rain(self.all_sprites)
            self.raining = randint(0, 10) > -1
            self.soil_layer.raining = self.raining
            self.sky = Sky()

            # shop
            self.shop_active = False
            self.menu = Menu(self.player, self.toggle_shop)

            # inventory
            self.inventory_active = False
            self.inventory = Inventory(self.player, self.toggle_inventory,
                                       self.held_items)

        else:
            tmx_data = load_pygame('../data/Tilesets/Forest.tmx')

            self.all_sprites = CameraGroup()
            self.collision_sprites.empty()
            self.tree_sprites.empty()
            self.water_sprites.empty()
            self.interaction_sprites.empty()
            self.slime_sprites.empty()  # used in forest, for now
            self.cow_sprites.empty()

            # fences
            for x, y, surf in tmx_data.get_layer_by_name('Fence').tiles():
                Generic((x * TILE_SIZE, y * TILE_SIZE), surf,
                        [self.all_sprites, self.collision_sprites])

            # Trees
            for obj in tmx_data.get_layer_by_name('Trees'):
                Tree(
                    pos=(obj.x, obj.y),
                    surf=obj.image,
                    groups=[self.all_sprites, self.collision_sprites,
                            self.tree_sprites],
                    name=obj.name,
                    player_add=self.player_add)

            # collision tiles
            for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():
                Generic((x * TILE_SIZE, y * TILE_SIZE), pygame.Surface(
                    (TILE_SIZE, TILE_SIZE)), self.collision_sprites)

            # slime area
            self.mob_area["slime"] = [[], []]
            # I swapped these for h, and I commented a block of code
            max_area = [0, 0]
            min_area = [5000, 5000]
            max_area, min_area = min_area, max_area
            # for obj in tmx_data.get_layer_by_name('Slime_detect'):
            #     if obj.x > max_area[0]:
            #         max_area[0] = obj.x
            #     if obj.x < min_area[0]:
            #         min_area[0] = obj.x
            #     if obj.y > max_area[1]:
            #         max_area[1] = obj.y
            #     if obj.y < min_area[1]:
            #         min_area[1] = obj.y

            self.mob_area["slime"] = [min_area, max_area]

            # Player
            sprite_dict = {"group": self.all_sprites,
                           "collision_sprites": self.collision_sprites,
                           "tree_sprites": self.tree_sprites,
                           "water_sprites": self.water_sprites,
                           "interaction": self.interaction_sprites,
                           "soil_layer": self.soil_layer,
                           "slime_sprites": self.slime_sprites}
            for obj in tmx_data.get_layer_by_name('Player'):
                if obj.name == 'Start':
                    # TODO make a new function for the player so that it is
                    # not re-initialized every time
                    self.player = Player(pos=(obj.x, obj.y),
                                         sprite_dict=sprite_dict,
                                         toggle_shop=self.toggle_shop,
                                         toggle_inventory=self.toggle_inventory,
                                         get_map_level=self.get_map_number,
                                         set_map_level=self.set_map_number,
                                         play_fishing_theme=
                                         self.play_fishing_theme)

                elif obj.name == 'Slime':
                    slime_frames = {"death": import_folder('../graphics/slime/'
                                                           'death'),
                                    "hit": import_folder('../graphics/slime/'
                                                         'hit'),
                                    "hit_p": import_folder('../graphics/slime/'
                                                           'hit-landing'),
                                    "idle": import_folder('../graphics/slime'
                                                          '/idle'),
                                    "jump": import_folder('../graphics/slime/'
                                                          '/jump'),
                                    "move": import_folder('../graphics/slime/'
                                                          '/move')}

                    Slime(pos=(obj.x + TILE_SIZE // 4, obj.y + TILE_SIZE // 4),
                          frames=slime_frames,
                          groups=[self.all_sprites, self.slime_sprites],
                          z=LAYERS['main'],
                          player_pos=self.player.get_pos,
                          detection_area=self.mob_area["slime"],
                          reduce_player_hp=self.player.reduce_hp)

                if obj.name == 'Starting':
                    Interaction((obj.x, obj.y), (obj.width, obj.height),
                                self.interaction_sprites, obj.name)

            # world
            Generic(
                pos=(0, 0),
                surf=pygame.image.load(
                    '../graphics/world/Forest.png').convert_alpha(),
                groups=self.all_sprites, z=LAYERS['ground'])

            self.active_music.stop()
            self.active_music = self.forest_theme
            self.active_music.set_volume(0.5)
            self.active_music.play()

            self.overlay = Overlay(self.player, self.held_items)
            self.transition = Transition(self.reset, self.player)

            # sky
            self.rain = Rain(self.all_sprites)
            self.raining = randint(0, 10) > -7
            self.soil_layer.raining = self.raining
            self.sky = Sky()

            # shop
            self.shop_active = False
            self.menu = Menu(self.player, self.toggle_shop)

            # inventory
            self.inventory_active = False
            # self.inventory = Inventory(self.player, self.toggle_inventory)

    def play_fishing_theme(self):
        """
        Plays the fishing theme, this function is passed as an argument
        to the player
        """
        if self.player.fishing.fishing_status and \
                not self.fishing_theme_on:
            self.fishing_theme_on = True
            self.active_music.stop()
            self.active_music = self.fishing_theme
            self.active_music.play()
        elif self.sky.night and not self.sky.music_swap and \
                not self.fishing_theme_on:
            self.active_music.stop()
            self.active_music = self.night_music
        elif not self.sky.night and not self.fishing_theme_on:
            self.active_music.stop()
            self.active_music.play()

    def get_map_number(self):
        """
        :return: int representing current map number
        """
        return self.level_no

    def set_map_number(self, level_no):
        """
        Sets the map number
        :return: None
        """
        self.level_no = level_no
        self.setup()

    def player_add(self, item: str):
        """
        Adds an item to the player's inventory
        :param item: string containing relevant item
        :return: None
        """
        self.player.item_inventory[item] += 1
        self.success.play()

    def toggle_shop(self):
        """
        Changes the bool value for the shop being active
        :return: None
        """

        self.shop_active = not self.shop_active

    def toggle_inventory(self):
        """
        Changes the bool value for the inventory being active
        :return: None
        """
        self.inventory_active = not self.inventory_active

    def reset(self):
        """
        This function is used to reset the day-night transition
        :return: None
        """
        # plants
        self.soil_layer.update_plants()

        # soil
        self.soil_layer.remove_water()
        self.raining = randint(0, 10) > 7
        self.soil_layer.raining = self.raining
        if self.raining:
            self.soil_layer.water_all()

        # apples on trees
        for tree in self.tree_sprites.sprites():
            try:
                for apple in tree.apple_sprites.sprites():
                    apple.kill()
                    # TODO Fix bug
            except AttributeError:
                print(tree)
                print(tree.pos)
            if tree.alive:
                tree.create_fruit()
            else:
                tree.tree_reset()

        # sky
        self.sky.start_color = [255, 255, 255]
        # night to day
        self.active_music.stop()
        self.active_music = self.music
        self.active_music.play()
        self.sky.night = False
        self.fishing_theme_on = False

    def plant_collision(self):
        """
        Code to change a land to being plowed
        :return: None
        """
        if self.soil_layer.plant_sprites:
            for plant in self.soil_layer.plant_sprites.sprites():
                if plant.harvestable and \
                        plant.rect.colliderect(self.player.hitbox):
                    self.player_add(plant.plant_type)
                    plant.kill()
                    Particle(plant.rect.topleft, plant.image, self.all_sprites,
                             LAYERS['main'])
                    x = plant.rect.centery // TILE_SIZE
                    y = plant.rect.centerx // TILE_SIZE
                    self.soil_layer.grid[x][y].remove('P')

    def run(self, dt: float):
        """
        Run part of the level
        :param dt: float for delta time
        :return: None
        """

        # drawing logic
        self.display_surface.fill("black")
        self.all_sprites.custom_draw(self.player)

        # updates
        if self.shop_active:
            self.menu.update()
        elif self.inventory_active:
            self.inventory.update()
        else:
            self.all_sprites.update(dt)
            self.plant_collision()
            self.overlay.display()

        # weather
        if self.raining and not self.shop_active and not self.inventory_active:
            self.rain.update()

        # daytime
        self.sky.display(dt)
        # nighttime
        if self.sky.night and not self.sky.music_swap:
            self.active_music.stop()
            self.active_music = self.night_music
            self.active_music.play()
            self.fishing_theme_on = False
            self.sky.music_swap = True

        # transition
        if self.player.sleep:
            self.transition.play()


class CameraGroup(pygame.sprite.Group):
    """
    This class is used to show the area in the players immediate vicinity
    """

    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2
        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(),
                                 key=lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)

                    # analytics
                    # slime = getattr(sprite, "slime", None)
                    # if callable(slime):
                    #     offset_rect = slime()
                    #     offset_rect.center -= self.offset
                    #     pygame.draw.rect(self.display_surface, 'red',
                    #                      offset_rect, 5)
                    # cow = getattr(sprite, "cow", None)
                    # if callable(cow):
                    #     offset_rect = cow()
                    #     offset_rect.center -= self.offset
                    #     pygame.draw.rect(self.display_surface, 'red',
                    #                      offset_rect, 5)
                    #
                    # if sprite == player:
                    #     pygame.draw.rect(self.display_surface, 'red',
                    #                      offset_rect, 5)
                    #     hitbox_rect = player.hitbox.copy()
                    #     hitbox_rect.center = offset_rect.center
                    #     pygame.draw.rect(self.display_surface, 'green',
                    #                      hitbox_rect, 5)
                    #     target_pos = offset_rect.center + PLAYER_TOOL_OFFSET[
                    #         player.status.split('_')[0]]
                    #     pygame.draw.circle(self.display_surface, 'blue',
                    #                        target_pos, 5)
