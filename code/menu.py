from typing import Callable

import pygame
from settings import *
from timer import Timer
from player import Player


class Menu:
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
    def __init__(self, player, toggle_inventory, items: list):
        self.player = player
        self.toggle_inventory = toggle_inventory
        self.items = items

        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('../font/LycheeSoda.ttf', 30)

        self.inventory_rows = 7
        self.inventory_cols = 5

        self.square_top_x, self.square_top_y = INVENTORY_OFFSETS[0]
        self.square_len_x, self.square_len_y = INVENTORY_OFFSETS[1]
        self.square_offset = INVENTORY_OFFSETS[2]

        # corn and tomato x2, say it's seeds
        self.item_surfs = {key: '' for key in
                           self.player.item_inventory.keys()}

        self.inventory_image = pygame.image.load('../graphics/'
                                                 'menus/extended UI'
                                                 '.png').convert_alpha()
        self.inventory_rect = self.inventory_image.get_rect(midbottom=
                                                       OVERLAY_POSITIONS
                                                       ['mini_inven'])

        self.import_surfs()

        # need to import the surface of the inventory, and put numbers on top
        # left? of each cell to indicate amount of the rss.

    def import_surfs(self):
        for item in self.item_surfs.keys():
            full_path = f'../graphics/menus/inventory/{item}.png'
            image_surf = pygame.image.load(full_path).convert()
            image_surf.set_colorkey((0, 0, 0))
            self.item_surfs[item] = image_surf

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            self.toggle_inventory()

        if keys[pygame.K_p]:
            mouse = pygame.mouse.get_pos()
            print(mouse)

    def update(self):
        self.input()
        self.display_surface.blit(self.inventory_image, self.inventory_rect)

        x_offset = -1
        for index, key in enumerate(self.item_surfs.keys()):
            x_offset += 1
            if x_offset == 5:
                x_offset = 0
            surf = self.item_surfs[key]
            location = self.inventory_rect.topleft + \
                       Vector2(40 + x_offset *
                               (surf.get_width() * 3),
                               39 + (index // 5) * (surf.get_height() * 3))

            item_rect = surf.get_rect(topleft=location)
            self.display_surface.blit(surf, item_rect)
            text_surf = self.font.render(str(self.player.item_inventory[key]),
                                         False, 'White')
            text_rect = item_rect.bottomright + Vector2(-3, -8)
            self.display_surface.blit(text_surf, text_rect)
