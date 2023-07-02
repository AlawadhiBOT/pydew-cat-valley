import random
from typing import Callable

import pygame
from settings import *
from support import *
from timer import Timer
from support import get_stats
from fishing import Fishing


class Player(pygame.sprite.Sprite):

    def __init__(self, pos, sprite_dict,
                 toggle_shop: Callable, toggle_inventory: Callable,
                 get_map_level: Callable, set_map_level: Callable,
                 play_fishing_theme: Callable):
        super().__init__(sprite_dict["group"])

        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0

        # general setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.z = LAYERS['main']

        # movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        # fishing
        self.fishing_theme = play_fishing_theme
        self.fishing = Fishing(self.player_add, False, self.fishing_theme)

        # collision
        self.hitbox = self.rect.copy().inflate((-126, -70))
        self.collision_sprites = sprite_dict["collision_sprites"]

        # text for player
        self.font = pygame.font.Font('../font/LycheeSoda.ttf', 30)
        self.display_text = []

        self.get_map_level = get_map_level
        self.set_map_level = set_map_level

        # hp
        self.hp = self.max_hp = 20

        # timers
        self.timers = {
            'tool use': Timer(600, self.use_tool),
            'swap': Timer(200),
            'seed use': Timer(350, self.use_seed),
            'seed switch': Timer(200),
            'fishing timer': Timer(450)
        }

        # tools
        self.tools = ['hoe', 'axe', 'water', 'fishing']

        # seeds
        # if you make a change here, remember that it may not reflect on the
        # csv and in settings
        self.seeds = ['wheat', 'tomato', 'corn', 'carrot', 'cabbage',
                      'overgine', 'tulip', 'lettuce', 'pumpkin', 'turnip',
                      'bell_pepper', 'beetroot', 'blue_star', 'edamame']

        # held items (in toolbox)
        self.held_items_index = 0
        self.held_items = ['hoe', 'axe', 'water', 'fishing', 'wheat']
        self.selected_hand = self.held_items[0]

        # STATS
        stats = get_stats('../data/player_info.csv')
        self.xp = stats[0][0]
        self.level = stats[0][1]
        self.max_xp = stats[0][2]
        self.stamina = stats[0][3]
        self.max_stamina = PLAYER_STAMINA_STATS['stamina']
        self.money = stats[0][4]

        # inventory
        # manually initiate these, if other things need to be added,
        # remember to adjust the csv accordingly
        self.item_inventory = {
            'wood': stats[1][0],
            'fish': stats[1][1],
            'apple': stats[1][2],
            'orange': stats[1][3],
            'pear': stats[1][4],
            'peach': stats[1][5],
        }
        # now do loop for the rest
        for ind, element in enumerate(self.seeds):
            self.item_inventory[element] = stats[1][ind + 5]

        # seed inventory
        self.seed_inventory = {}
        for ind, element in enumerate(self.seeds):
            self.seed_inventory[element] = stats[2][ind]

        # interaction
        self.tree_sprites = sprite_dict["tree_sprites"]
        self.water_sprites = sprite_dict["water_sprites"]
        self.slime_sprites = sprite_dict["slime_sprites"]
        self.interaction = sprite_dict["interaction"]
        self.sleep = False
        self.soil_layer = sprite_dict["soil_layer"]
        self.toggle_shop = toggle_shop
        self.toggle_inventory = toggle_inventory

        # sound
        self.watering = pygame.mixer.Sound('../audio/water.mp3')
        self.watering.set_volume(0.2)
        self.throw_bob = pygame.mixer.Sound('../audio/fishing.wav')
        self.throw_bob.set_volume(0.2)

    def map_swap(self, pos, sprite_dict):
        """
        Resets some core attributes which are usually set by the __init__
        method.
        Function was created in order to fix the bugs of returning to the
        forest/main map where gold/hp would be reset.
        :param pos: tmx object representing the location of the player.
        :param sprite_dict: Dictionary containing sprites.
        :return: NoneType
        """
        # re-initialize all sprites
        super().__init__(sprite_dict["group"])

        # change the player's rect, which changes the player's pos, and by
        # extension, the location of the hitbox
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.hitbox = self.rect.copy().inflate((-126, -70))

        # re-setup sprite groups individually
        self.collision_sprites = sprite_dict["collision_sprites"]
        self.tree_sprites = sprite_dict["tree_sprites"]
        self.water_sprites = sprite_dict["water_sprites"]
        self.slime_sprites = sprite_dict["slime_sprites"]
        self.interaction = sprite_dict["interaction"]
        self.soil_layer = sprite_dict["soil_layer"]

    def use_tool(self):
        if self.selected_hand == 'hoe':
            self.soil_layer.get_hit(self.target_pos)
            self.stamina -= PLAYER_STAMINA_STATS['dig']
            self.xp += PLAYER_LEVEL_STATS['dig']

        if self.selected_hand == 'axe':
            for tree in self.tree_sprites.sprites():
                if tree.rect.collidepoint(self.target_pos):
                    tree.damage()
                    if tree.health == 0:
                        self.xp += PLAYER_LEVEL_STATS['wood']
                    self.stamina -= PLAYER_STAMINA_STATS['tree']

            for slime in self.slime_sprites.sprites():
                slime.slime()
                if slime.hitbox.collidepoint(self.target_pos):
                    slime.damage()

        if self.selected_hand == 'water':
            self.soil_layer.water(self.target_pos)
            self.watering.play()
            self.xp += PLAYER_LEVEL_STATS['water']
            self.stamina -= PLAYER_STAMINA_STATS['water']

        if self.selected_hand == 'fishing':
            for water in self.water_sprites:
                if water.rect.collidepoint(self.target_pos):
                    self.throw_bob.play()
                    self.fishing.fishing_start()

    def get_target_pos(self):
        """
        Gets the point to which the player will "hit" with their tool, seed, or
        otherwise.
        :return: NoneType
        """
        self.target_pos = self.rect.center + PLAYER_TOOL_OFFSET[
            self.status.split('_')[0]]

    def get_bigger_target_pos(self):
        """
        Intended to be 3 points rather than one (in get_target_pos it is one),
        which should help in combating mobs
        :return:
        """
        self.target_pos = self.rect.center + PLAYER_TOOL_OFFSET[
            self.status.split('_')[0]]

    def use_seed(self):
        if self.selected_hand not in self.tools and \
                self.seed_inventory[self.selected_hand] > 0:
            if self.soil_layer.plant_seed(self.target_pos, self.selected_hand):
                self.seed_inventory[self.selected_hand] -= 1
                self.stamina -= PLAYER_STAMINA_STATS['plant']
                self.xp += PLAYER_LEVEL_STATS['plant']

    def import_assets(self):
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [],
                           'down_idle': [],
                           'right_hoe': [], 'left_hoe': [], 'up_hoe': [],
                           'down_hoe': [],
                           'right_axe': [], 'left_axe': [], 'up_axe': [],
                           'down_axe': [],
                           'right_water': [], 'left_water': [], 'up_water': [],
                           'down_water': [],
                           'right_fishing': [], 'left_fishing': [],
                           'up_fishing': [], 'down_fishing': []}

        for animation in self.animations.keys():
            full_path = '../graphics/character/' + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        self.frame_index += 13 * dt
        if self.frame_index >= len(self.animations[self.status]):
            if self.fishing.fishing_status:
                self.frame_index = len(self.animations[self.status]) - 1
            else:
                self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.timers['tool use'].active and not self.sleep:
            # directions
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            if keys[pygame.K_SPACE]:
                # tool use
                if self.held_items[self.held_items_index] in self.tools:
                    self.timers['tool use'].activate()
                else:
                    # seed
                    self.timers['seed use'].activate()

                self.direction = pygame.math.Vector2()
                self.frame_index = 0

            # swap to right held item
            if keys[pygame.K_e] and not self.timers['swap'].active:
                self.timers['swap'].activate()
                self.held_items_index += 1
                self.held_items_index = self.held_items_index if \
                    self.held_items_index < len(self.held_items) else 0

                if self.held_items[self.held_items_index] in self.tools:
                    self.selected_hand = self.held_items[self.held_items_index]
                else:
                    self.selected_hand = self.held_items[self.held_items_index]

                # tool_swp_surf = self.font.render(
                #     f'{GAME_MESSAGES["TEXT_CHOICES"][0]} '
                #     f'{self.selected_hand}', False, 'Black')
                # tool_swp_rect = tool_swp_surf.get_rect(topright=
                #                                        GAME_MESSAGES["TXT_BEG"])
                # tool_timer = Timer(GAME_MESSAGES["TEXT_TIMER"])
                # tool_timer.activate()
                # self.display_text = [(tool_swp_surf, tool_swp_rect, tool_timer)]

            # swap to left hand item
            if keys[pygame.K_q] and not self.timers['swap'].active:
                self.timers['swap'].activate()
                # swap to left held item
                self.held_items_index -= 1
                self.held_items_index = self.held_items_index if \
                    self.held_items_index >= 0 else len(self.held_items) - 1

                if self.held_items[self.held_items_index] in self.tools:
                    self.selected_hand = self.held_items[self.held_items_index]
                else:
                    self.selected_hand = self.held_items[self.held_items_index]

                # tool_swp_surf = self.font.render(
                #     f'{GAME_MESSAGES["TEXT_CHOICES"][0]} '
                #     f'{self.selected_hand}', False, 'Black')
                # tool_swp_rect = tool_swp_surf.get_rect(topright=
                #                                        GAME_MESSAGES["TXT_BEG"])
                # tool_timer = Timer(GAME_MESSAGES["TEXT_TIMER"])
                # tool_timer.activate()
                # self.display_text = [(tool_swp_surf, tool_swp_rect, tool_timer)]

            if keys[pygame.K_1]:
                self.held_items_index = 0
                self.selected_hand = self.held_items[self.held_items_index]
            if keys[pygame.K_2]:
                self.held_items_index = 1
                self.selected_hand = self.held_items[self.held_items_index]
            if keys[pygame.K_3]:
                self.held_items_index = 2
                self.selected_hand = self.held_items[self.held_items_index]
            if keys[pygame.K_4]:
                self.held_items_index = 3
                self.selected_hand = self.held_items[self.held_items_index]
            if keys[pygame.K_5]:
                self.held_items_index = 4
                self.selected_hand = self.held_items[self.held_items_index]

            # open inventory
            if keys[pygame.K_i]:
                self.toggle_inventory()

            # interaction with bed
            if keys[pygame.K_RETURN]:
                # self.toggle_shop()
                collided_interaction_sprites = pygame.sprite.spritecollide(
                    self, self.interaction, False)
                if collided_interaction_sprites:
                    map_no = self.get_map_level()
                    if map_no == MAP_NUMBERS["Starting"]:
                        if collided_interaction_sprites[0].name == 'Trader':
                            self.toggle_shop()
                        elif collided_interaction_sprites[0].name == 'Forest':
                            self.set_map_level(MAP_NUMBERS["Forest"])
                        else:
                            self.auto_save_night()
                    elif map_no == MAP_NUMBERS["Forest"]:
                        if collided_interaction_sprites[0].name == "Starting":
                            self.set_map_level(MAP_NUMBERS["Starting"])

    def get_status(self):
        # idle
        if self.direction.magnitude() == 0 and not self.fishing.fishing_status:
            self.status = self.status.split('_')[0] + '_idle'

        if self.fishing.fishing_status:
            self.image = self.animations[self.status][int(self.frame_index)]

        # tool use
        if self.timers['tool use'].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_hand

    def get_pos(self) -> tuple[float, float]:
        """
        Gives the position of the player.
        This function was originally created for the slime.
        :return: tuple containing x and y coordinates of player
        """

        return self.pos.x, self.pos.y

    def reduce_hp(self):
        """
        Reduces hp of the player by 1.
        This function was originally created for the slime
        """
        self.hp -= 1

    def player_add(self, item: str, sign: int = 1):
        """
        Copy of a function used in level. Added here for files such as
        fishing.py
        02-Jul-23, added sign parameter and exp.
        :param item: item to be increased in counter
        :param sign: indicates increase or decrease of item
        :return: NoneType
        """
        self.item_inventory[item] += 1 * sign

    def player_add_seed(self, seed: str, sign: int = 1):
        """
        02-Jul-23
        As in player_add function same thing. However, the purpose of this
        function is to support menu.py
        :param seed: seed to be increased in counter
        :param sign: indicates increase or decrease of seed
        :return: NoneType
        """
        self.seed_inventory[seed] += 1 * sign

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction == 'horizontal':
                        if self.direction.x > 0:  # moving right
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0:  # moving left
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx

                    if direction == 'vertical':
                        if self.direction.y > 0:  # moving down
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0:  # moving up
                            self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery

    def move(self, dt):

        # Normalizing a vector
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # Horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')

        # Vertical Movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')

    def check_level_stamina(self):
        if self.xp >= self.max_xp:
            self.xp = self.max_xp - self.xp
            self.max_xp = round(1.2 * self.max_xp)
            self.level += 1
        if self.stamina <= 0:
            self.speed = 50

    def auto_save_night(self):
        self.status = 'left_idle'
        self.sleep = True
        self.stamina = self.max_stamina
        self.speed = 200
        f = open('../data/player_info.csv', 'w')
        f.write('xp,level,max_xp,stamina,max_stamina,money\n')

        items = "".join([f'{key},' for key in self.item_inventory.keys()])
        f.write(items[:-1] + "\n")
        seeds = "".join([f'{key} seed,' for key in self.seed_inventory.keys()])
        f.write(seeds[:-1] + "\n")

        f.write(f'{self.xp},{self.level},{self.max_xp},'
                f'{self.stamina},{self.max_stamina},'
                f'{self.money}\n')

        item_vals = "".join([f'{val},' for val in self.item_inventory.values()])
        f.write(item_vals[:-1] + "\n")
        seed_vals = "".join([f'{val},' for val in self.seed_inventory.values()])
        f.write(seed_vals[:-1] + "\n")

        f.close()

    def update(self, dt):
        if self.fishing.fishing_status:
            self.fishing.update()
        else:
            self.input()
        self.get_status()
        self.update_timers()
        self.get_target_pos()
        self.move(dt)
        self.animate(dt)
        self.check_level_stamina()
