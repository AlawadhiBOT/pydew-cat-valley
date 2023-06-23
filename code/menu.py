from typing import Callable

import pygame
from settings import *
from timer import Timer
from player import Player


class Menu:
    """
    This class is used for the shop, accessed by pressing "ENTER" near the
    trader, which is the brown cat sprite.
    """

    def __init__(self, player: Player, toggle_menu: Callable):

        # general setup
        self.player = player
        self.toggle_menu = toggle_menu
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('../font/LycheeSoda.ttf', 30)

        # menu image
        self.menu_image = \
            pygame.image.load('../graphics/menus/shop.png').convert()

        # imaging setup
        self.sample_rect = pygame.Rect(INVENTORY_OFFSETS[3],
                                       (self.menu_image.get_width() // 2 - 37,
                                        20))
        self.space = 5
        self.width = self.menu_image.get_width()
        self.height = self.menu_image.get_height()
        self.padding = 8.5
        self.topleft_x = SCREEN_HEIGHT / 2 - self.width / 2
        self.topleft_y = SCREEN_HEIGHT / 2 - self.height / 2

        # entries
        self.options = list(self.player.item_inventory.keys()) + \
                       list(self.player.seed_inventory.keys())
        self.sell_border = len(self.player.item_inventory) - 1
        self.setup()

        # movement
        self.index = 0
        self.timer = Timer(200)

    def display_money(self):
        # put on topleft of image
        text_surf = self.font.render(f'${self.player.money}', False, 'Black')
        text_rect = pygame.Rect(self.topleft_x + SCREEN_WIDTH / 2,
                                self.topleft_y + self.space * 3,
                                text_surf.get_width() + self.space,
                                text_surf.get_height() + self.space)

        self.display_surface.blit(text_surf, text_rect)

    def setup(self):

        # create text surfaces
        self.text_surfs = []

        for index, item in enumerate(self.options):
            if index > len(self.player.item_inventory.keys()) - 1:
                text_surf = self.font.render(item + ' seed(s)', False, 'Black')
            else:
                text_surf = self.font.render(item, False, 'Black')
            self.text_surfs.append(text_surf)

        self.menu_top = SCREEN_HEIGHT / 2 - self.height / 2 + \
                        self.sample_rect.y
        self.main_rect = pygame.Rect(SCREEN_WIDTH / 2 - self.width / 2 +
                                     self.sample_rect.x,
                                     self.menu_top, self.width,
                                     self.height)

        # buy/sell text surface
        self.buy_text = self.font.render(' ' * 6 + 'buy', False, 'Black')
        self.sell_text = self.font.render(' ' * 7 + 'sell', False, 'Black')

    def input(self):
        # get the input and then if the player presses esc, close the menu
        keys = pygame.key.get_pressed()
        self.timer.update()

        if keys[pygame.K_ESCAPE]:
            self.toggle_menu()

        if not self.timer.active:
            if keys[pygame.K_UP]:
                self.index -= 1
                self.timer.activate()

            if keys[pygame.K_DOWN]:
                self.index += 1
                self.timer.activate()

            if keys[pygame.K_SPACE]:
                self.timer.activate()

                # get item
                current_item = self.options[self.index]

                # sell
                if self.index <= self.sell_border:
                    if self.player.item_inventory[current_item] > 0:
                        self.player.item_inventory[current_item] -= 1
                        self.player.money += SALE_PRICES[current_item]
                        self.player.xp += PLAYER_LEVEL_STATS['sell']
                        self.player.stamina -= PLAYER_STAMINA_STATS['sell']
                else:  # buy
                    seed_price = PURCHASE_PRICES[current_item]
                    if self.player.money >= seed_price:
                        self.player.seed_inventory[current_item] += 1
                        self.player.money -= PURCHASE_PRICES[current_item]
                        self.player.xp += PLAYER_LEVEL_STATS['buy']
                        self.player.stamina -= PLAYER_STAMINA_STATS['buy']

        # clamo the values
        if self.index < 0:
            self.index = len(self.options) - 1
        if self.index > len(self.options) - 1:
            self.index = 0

    def show_entry(self, text_surf, amount, top, selected):
        # background
        bg_rect = pygame.Rect(self.main_rect.left, top, self.sample_rect.width,
                              text_surf.get_height() + (self.padding * 2))

        # text
        text_rect = text_surf.get_rect(midleft=
                                       (self.main_rect.left + 20,
                                        bg_rect.centery))
        self.display_surface.blit(text_surf, text_rect)

        # amount
        amount_surf = self.font.render(str(amount), False, 'Black')
        amount_rect = amount_surf.get_rect(midright=(bg_rect.right -
                                                     15,
                                                     bg_rect.centery))
        self.display_surface.blit(amount_surf, amount_rect)

        # selected
        if selected:
            pygame.draw.rect(self.display_surface, 'black', bg_rect, 4, 4)
            if self.index <= self.sell_border:  # sell
                pos_rect = self.sell_text.get_rect(midleft=(
                    self.main_rect.left + 150, bg_rect.centery))
                self.display_surface.blit(self.sell_text, pos_rect)
            else:  # buy
                pos_rect = self.buy_text.get_rect(midleft=(
                    self.main_rect.left + 150, bg_rect.centery))
                self.display_surface.blit(self.buy_text, pos_rect)

    def update(self):
        self.input()
        posx = (SCREEN_WIDTH / 2 - self.width / 2)
        posy = (SCREEN_HEIGHT / 2 - self.height / 2)
        self.display_surface.blit(self.menu_image, (posx, posy))
        self.display_money()
        for text_index, text_surf in enumerate(self.text_surfs):
            top = self.main_rect.top + text_index * (text_surf.get_height() +
                                                     (self.padding * 2) +
                                                     self.space)
            amount_list = list(self.player.item_inventory.values()) + \
                          list(self.player.seed_inventory.values())
            amount = amount_list[text_index]
            self.show_entry(text_surf, amount, top, self.index == text_index)


class Inventory:
    """
    This class is used for the inventory, accessed by pressing "i" and exited
    by pressing "ESCAPE".
    """

    def __init__(self, player, toggle_inventory, held_items: list):
        self.player = player
        self.toggle_inventory = toggle_inventory
        self.held_items = held_items

        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('../font/LycheeSoda.ttf', 30)

        # imports
        self.item_surfs = {item: pygame.image.load(f'../graphics/menus/'
                                                   f'inventory/{item}.png')
                           for item in player.item_inventory}

        overlay_path = '../graphics/overlay/'

        self.tools_surf = {tool: pygame.image.load(f'{overlay_path}/tools/'
                                                   f'{tool}.png'
                                                   ).convert_alpha()
                           for tool in player.tools}
        self.seeds_surf = {seed: pygame.image.load(f'{overlay_path}{seed}'
                                                   f'.png').convert_alpha()
                           for seed in player.seeds}

        self.inventory_image = pygame.image.load('../graphics/'
                                                 'menus/extended UI'
                                                 '.png').convert_alpha()
        self.inventory_rect = self.inventory_image.get_rect(midbottom=
                                                            OVERLAY_POSITIONS
                                                            ['mini_inven'])
        # selection rectangle
        self.box_img = pygame.image.load('../graphics/menus'
                                         '/selector.png')
        self.box_rect = self.box_img.get_rect(topleft=
                                              self.inventory_rect.topleft +
                                              Vector2(26, 25))

        # timer
        self.timer = Timer(250)

        self.item_array = [[] for _ in range((len(self.item_surfs) +
                                              len(self.tools_surf)) // 5 + 1)]
        for i, key in enumerate(self.tools_surf):
            self.item_array[i // 5].append(key)
        for i, key in enumerate(self.item_surfs):
            self.item_array[(i + len(self.tools_surf) + 1) // 5].append(key)
        self.curr_ind = [0, 0]

    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()

        if not self.timer.active:
            # the -=1 is a bug that happens I could not figure out why it
            # happened, the inventory would shift in a direction equal to
            # the change by 1 pixel, so if I moved the box right, the inventory
            # would move right by one pixel.
            if keys[pygame.K_d]:
                self.inventory_rect[0] += 1
                self.box_rect.left += 52 + 8
                self.inventory_rect.left -= 1
                self.curr_ind[0] += 1

                self.timer.activate()

            if keys[pygame.K_a]:
                self.inventory_rect[0] -= 1
                self.box_rect.left -= 52 + 8
                self.inventory_rect.left += 1
                self.curr_ind[0] -= 1

                self.timer.activate()

            if keys[pygame.K_w]:
                self.inventory_rect[1] -= 1
                self.box_rect.top -= 52 + 8
                self.inventory_rect.top += 1
                self.curr_ind[1] -= 1

                self.timer.activate()

            if keys[pygame.K_s]:
                self.inventory_rect[1] += 1
                self.box_rect.top += 52 + 8
                self.inventory_rect.top -= 1
                self.curr_ind[1] += 1

                self.timer.activate()

        if keys[pygame.K_1]:
            self.held_items[0] = self.item_array[
                self.curr_ind[1]][self.curr_ind[0]]
        if keys[pygame.K_2]:
            self.held_items[1] = self.item_array[
                self.curr_ind[1]][self.curr_ind[0]]
        if keys[pygame.K_3]:
            self.held_items[2] = self.item_array[
                self.curr_ind[1]][self.curr_ind[0]]
        if keys[pygame.K_4]:
            self.held_items[3] = self.item_array[
                self.curr_ind[1]][self.curr_ind[0]]
        if keys[pygame.K_5]:
            self.held_items[4] = self.item_array[
                self.curr_ind[1]][self.curr_ind[0]]

        if keys[pygame.K_ESCAPE]:
            self.toggle_inventory()

        if keys[pygame.K_p]:
            mouse = pygame.mouse.get_pos()
            print(mouse)

    def update(self):
        self.input()

        self.display_surface.blit(self.inventory_image,
                                  self.inventory_rect)

        # draws the tools in the inventory
        for index, key in enumerate(self.tools_surf.keys()):
            if key not in self.held_items:
                surf = self.tools_surf[key]
                location = self.inventory_rect.topleft + \
                           Vector2(30 + index * (surf.get_width() * 1.5),
                                   29)
                item_rect = surf.get_rect(topleft=location)
                self.display_surface.blit(surf, item_rect)

        # draws the items in the inventory.
        for index, key in enumerate(self.item_surfs.keys()):
            surf = self.item_surfs[key]
            location = self.inventory_rect.topleft + \
                       Vector2(40 + (index % 5) *
                               (surf.get_width() * 3),
                               35 + (index // 5 + 1) *
                               (surf.get_height() * 2.6))

            item_rect = surf.get_rect(topleft=location)
            self.display_surface.blit(surf, item_rect)
            text_surf = self.font.render(str(self.player.item_inventory[key]),
                                         False, 'White')
            text_rect = item_rect.bottomright + Vector2(-3, -8)
            self.display_surface.blit(text_surf, text_rect)

        # draws the bottom of the inventory, which is what is by the player
        # on hand.
        for index, item in enumerate(self.held_items):
            num = -71
            if item in self.player.tools:
                # for the calculation, perhaps it may be best to use the size of
                # each box (52x52)
                surf = self.tools_surf[item]
                location = self.inventory_rect.bottomleft + \
                           Vector2(30 + index * (20 + surf.get_width()),
                                   num)
                item_rect = surf.get_rect(topleft=location)
                self.display_surface.blit(surf, item_rect)

            elif item in self.player.seeds:
                surf = self.seeds_surf[item]
                location = self.inventory_rect.bottomleft + \
                           Vector2(30 + index * (20 + surf.get_width()),
                                   num)
                item_rect = surf.get_rect(topleft=location)
                self.display_surface.blit(surf, item_rect)

                text_surf = self.font.render(
                    str(self.player.seed_inventory[item]),
                    False, 'Green')
                text_rect = item_rect.bottomright + Vector2(-12, -24)
                self.display_surface.blit(text_surf, text_rect)

        self.display_surface.blit(self.box_img, self.box_rect)
