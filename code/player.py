import random

import pygame
from settings import *
from support import *
from timer import Timer
from support import get_stats
from fishing import Fishing


class Player(pygame.sprite.Sprite):

    def __init__(self, pos, group, collision_sprites, tree_sprites,
                 water_sprites,  interaction, soil_layer, toggle_shop,
                 toggle_inventory, map_lvl):
        super().__init__(group)

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
        self.fishing = Fishing(self, False)

        # collision
        self.hitbox = self.rect.copy().inflate((-126, -70))
        self.collision_sprites = collision_sprites

        # text for player
        self.font = pygame.font.Font('../font/LycheeSoda.ttf', 30)
        self.display_text = []
        
        self.map_lvl = map_lvl

        # timers
        self.timers = {
            'tool use': Timer(350, self.use_tool),
            'tool switch': Timer(200),
            'seed use': Timer(350, self.use_seed),
            'seed switch': Timer(200),
            'fishing timer': Timer(450)
        }

        # tools
        self.tools = ['hoe', 'axe', 'water', 'fishing']
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]

        # seeds
        self.seeds = ['corn', 'tomato']
        self.seed_index = 0
        self.selected_seed = self.seeds[self.seed_index]

        # STATS
        stats = get_stats('../data/player_info.csv')
        self.xp = stats[0][0]
        self.level = stats[0][1]
        self.max_xp = stats[0][2]
        self.stamina = stats[0][3]
        self.max_stamina = PLAYER_STAMINA_STATS['stamina']
        self.money = stats[0][4]

        # inventory
        self.item_inventory = {
            'wood':   stats[1][0],
            'apple':  stats[1][1],
            'corn':   stats[1][2],
            'tomato': stats[1][3],
            'fish': stats[1][4]
        }
        # seed inventory
        self.seed_inventory = {
            'corn':   stats[2][0],
            'tomato': stats[2][1]
        }

        # interaction
        self.tree_sprites = tree_sprites
        self.water_sprites = water_sprites
        self.interaction = interaction
        self.sleep = False
        self.soil_layer = soil_layer
        self.toggle_shop = toggle_shop
        self.toggle_inventory = toggle_inventory

        # sound
        self.watering = pygame.mixer.Sound('../audio/water.mp3')
        self.watering.set_volume(0.2)
        self.throw_bob = pygame.mixer.Sound('../audio/fishing.wav')
        self.throw_bob.set_volume(0.2)

    def use_tool(self):
        if self.selected_tool == 'hoe':
            self.soil_layer.get_hit(self.target_pos)
            self.stamina -= PLAYER_STAMINA_STATS['dig']
            self.xp += PLAYER_LEVEL_STATS['dig']

        if self.selected_tool == 'axe':
            for tree in self.tree_sprites.sprites():
                if tree.rect.collidepoint(self.target_pos):
                    tree.damage()
                    if tree.health == 0:
                        self.xp += PLAYER_LEVEL_STATS['wood']
                    self.stamina -= PLAYER_STAMINA_STATS['tree']

        if self.selected_tool == 'water':
            self.soil_layer.water(self.target_pos)
            self.watering.play()
            self.xp += PLAYER_LEVEL_STATS['water']
            self.stamina -= PLAYER_STAMINA_STATS['water']

        if self.selected_tool == 'fishing':
            for water in self.water_sprites:
                if water.rect.collidepoint(self.target_pos):
                    self.throw_bob.play()
                    self.fishing.fishing_start()

    def get_target_pos(self):

        self.target_pos = self.rect.center + PLAYER_TOOL_OFFSET[
            self.status.split('_')[0]]

    def use_seed(self):
        if self.seed_inventory[self.selected_seed] > 0:
            if self.soil_layer.plant_seed(self.target_pos, self.selected_seed):
                self.seed_inventory[self.selected_seed] -= 1
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
        self.frame_index += 4 * dt
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

            # tool use
            if keys[pygame.K_SPACE]:
                self.timers['tool use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

            # change tool
            if keys[pygame.K_q] and not self.timers['tool switch'].active:
                self.timers['tool switch'].activate()
                self.tool_index += 1
                self.tool_index = self.tool_index if \
                    self.tool_index < len(self.tools) else 0
                self.selected_tool = self.tools[self.tool_index]
                tool_swp_surf = self.font.render(
                                 f'{GAME_MESSAGES["TEXT_CHOICES"][0]} '
                                 f'{self.selected_tool}', False, 'Black')
                tool_swp_rect = tool_swp_surf.get_rect(topright=
                                                       GAME_MESSAGES["TXT_BEG"])
                tool_timer = Timer(GAME_MESSAGES["TEXT_TIMER"])
                tool_timer.activate()
                self.display_text = [(tool_swp_surf, tool_swp_rect, tool_timer)]

            # seed
            if keys[pygame.K_LCTRL]:
                self.timers['seed use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

            # change seed
            if keys[pygame.K_e] and not self.timers['seed switch'].active:
                self.timers['seed switch'].activate()
                self.seed_index += 1
                self.seed_index = self.seed_index if \
                    self.seed_index < len(self.seeds) else 0
                self.selected_seed = self.seeds[self.seed_index]

            # open inventory
            if keys[pygame.K_i]:
                self.toggle_inventory()

            # interaction with bed
            if keys[pygame.K_RETURN]:
                # self.toggle_shop()
                collided_interaction_sprites = pygame.sprite.spritecollide(
                    self, self.interaction, False)
                if collided_interaction_sprites:
                    if collided_interaction_sprites[0].name == 'Trader':
                        self.toggle_shop()
                    elif collided_interaction_sprites[0].name == 'Forest':
                        self.map_lvl[0][0][0] = 1
                        self.map_lvl[1]()
                    else:
                        self.auto_save_night()

    def get_status(self):
        # idle
        if self.direction.magnitude() == 0 and not self.fishing.fishing_status:
            self.status = self.status.split('_')[0] + '_idle'

        if self.fishing.fishing_status:
            self.image = self.animations[self.status][int(self.frame_index)]

        # tool use
        if self.timers['tool use'].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool

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
        f.write('inventory\nseed inventory\n')
        f.write(f'{self.xp},{self.level},{self.max_xp},'
                f'{self.stamina},{self.max_stamina},'
                f'{self.money}\n')
        f.write(f'{str(self.item_inventory.values())[13:-2]}\n')
        f.write(f'{str(self.seed_inventory.values())[13:-2]}')
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
