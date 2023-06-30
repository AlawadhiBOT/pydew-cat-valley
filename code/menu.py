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
            pygame.image.load('../graphics/menus/shop_2.png').convert()
        self.menu_rect = self.menu_image.get_rect(
            center=OVERLAY_POSITIONS['shop'])

        # imaging setup
        self.space = 5
        self.width = self.menu_image.get_width()
        self.height = self.menu_image.get_height()
        self.padding = 5
        self.topleft_offset = 128
        self.topleft_items = self.menu_rect.topleft + \
                             Vector2(self.topleft_offset, self.topleft_offset)

        # entries
        self.tools = self.player.tools
        self.items = list(self.player.item_inventory.keys())
        self.seeds = self.player.seeds
        self.sell_border = len(self.player.item_inventory) - 1

        # surfs
        self.tool_text_surfs = []
        self.item_nonplant_text_surfs = []
        self.item_text_plant_surf = []
        self.seed_text_surfs = []

        self.tool_text = self.item_text = self.seed_text = None

        self.setup()

        # movement
        self.page_number = 0
        self.status_page = "Unplantable"
        self.index = 0
        self.timer = Timer(150)

    def display_money(self):
        text_surf = self.font.render(f'${self.player.money}', False, 'Black')
        text_rect = pygame.Rect(0, 0,
                                text_surf.get_width(),
                                text_surf.get_height())
        text_rect.midbottom = self.menu_rect.midbottom + \
                              Vector2(0, - self.padding * 6)

        self.display_surface.blit(text_surf, text_rect)

    def setup(self):
        """
        Gets texts for each function item type.
        """
        self.tool_text = self.font.render("TOOLS", False, 'Black')
        for item in self.tools:
            text_surf = self.font.render(item, False, 'Black')
            self.tool_text_surfs.append(text_surf)

        self.item_text = self.font.render("NON PLANT-ABLE ITEMS",
                                          False, 'Black')
        for item in self.items:
            if item not in self.seeds:
                text_surf = self.font.render(item, False, 'Black')
                self.item_nonplant_text_surfs.append(text_surf)
            else:
                text_surf = self.font.render(item, False, 'Black')
                self.item_text_plant_surf.append(text_surf)

        self.seed_text = self.font.render("PLANT-ABLES", False, 'Black')
        for item in self.seeds:
            text_surf = self.font.render(item, False, 'Black')
            self.seed_text_surfs.append(text_surf)
            text_surf = self.font.render(item + "seeds", False, 'Black')
            self.seed_text_surfs.append(text_surf)

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
            self.index = len(self.item_nonplant_text_surfs) - 1
        if self.index > len(self.item_nonplant_text_surfs) - 1:
            self.index = 0

    def show_entry(self, text_surf, amount, index, selected):
        # background
        if index % 2 == 0:
            calc_x = 0
            calc_y = (text_surf.get_height() + self.padding * 4) * index // 2
            top_left_calc = self.topleft_items + Vector2(calc_x, calc_y)
        else:
            calc_x = self.menu_rect.width // 2 - self.topleft_offset
            calc_y = (text_surf.get_height() + self.padding * 4) * \
                     (index - 1) // 2

            top_left_calc = self.topleft_items + Vector2(calc_x, calc_y)

        bg_rect = pygame.Rect(top_left_calc.x - self.padding,
                              top_left_calc.y - self.padding,
                              self.menu_rect.width // 2 - self.topleft_offset,
                              text_surf.get_height() + self.padding * 2)

        # text
        text_rect = text_surf.get_rect(midleft=top_left_calc +
                                               Vector2(self.padding,
                                                       self.padding * 3)
                                       )
        self.display_surface.blit(text_surf, text_rect)

        # amount
        amount_surf = self.font.render(str(amount), False, 'Black')
        amount_rect = amount_surf.get_rect(midright=bg_rect.midright
                                                    - Vector2(self.padding, 0))
        self.display_surface.blit(amount_surf, amount_rect)

        # selected
        if selected:
            pygame.draw.rect(self.display_surface, 'black', bg_rect, 4, 4)
            # if self.index <= self.sell_border:  # sell
            #     pos_rect = self.sell_text.get_rect(midleft=(
            #         self.main_rect.left + 150, bg_rect.centery))
            #     self.display_surface.blit(self.sell_text, pos_rect)
            # else:  # buy
            #     pos_rect = self.buy_text.get_rect(midleft=(
            #         self.main_rect.left + 150, bg_rect.centery))
            #     self.display_surface.blit(self.buy_text, pos_rect)

    def update(self):
        self.input()

        self.display_surface.blit(self.menu_image, self.menu_rect)
        self.display_money()

        if self.status_page == "Unplantable":
            amount_list = [val for key, val in
                           self.player.item_inventory.items()
                           if key not in self.player.seeds]
            lst = self.item_nonplant_text_surfs
        # else:
            # TODO finish this for plantables
            # amount_lst = []
            # for item in self.seeds:
            #
            # lst = self.item_nonplant_text_surfs

        for text_index, text_surf in enumerate(self.item_nonplant_text_surfs):
            amount = amount_list[text_index]
            self.show_entry(text_surf, amount, text_index,
                            self.index == text_index)


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
                                                            ['inven'])
        # selection rectangle
        self.box_img = pygame.image.load('../graphics/menus'
                                         '/selector.png')
        self.box_rect = self.box_img.get_rect(topleft=
                                              self.inventory_rect.topleft +
                                              Vector2(26, 25))

        # timer
        self.timer = Timer(150)

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
            if keys[pygame.K_RIGHT]:
                row_len = len(self.item_array[self.curr_ind[0]])
                if self.curr_ind[0] + 1 == row_len:
                    self.box_rect.left -= (52 + 8) * (row_len - 1)
                    self.curr_ind[0] = 0
                else:
                    self.box_rect.left += 52 + 8
                    self.curr_ind[0] += 1

                self.timer.activate()

            if keys[pygame.K_LEFT]:
                row_len = len(self.item_array[self.curr_ind[0]])
                if self.curr_ind[0] - 1 < 0:
                    self.box_rect.left += (52 + 8) * row_len
                    self.curr_ind[0] = row_len
                else:
                    self.box_rect.left -= 52 + 8
                    self.curr_ind[0] -= 1

                self.timer.activate()

            if keys[pygame.K_UP]:
                col_len = len(self.item_array)
                if self.curr_ind[1] - 1 < 0:
                    self.box_rect.top += (52 + 8) * (col_len - 1)
                    self.curr_ind[1] = col_len - 1
                else:
                    self.box_rect.top -= 52 + 8
                    self.curr_ind[1] -= 1

                self.timer.activate()

            if keys[pygame.K_DOWN]:
                col_len = len(self.item_array)
                if self.curr_ind[1] + 1 == col_len:
                    self.box_rect.top -= (52 + 8) * (col_len - 1)
                    self.curr_ind[1] = 0
                else:
                    self.box_rect.top += 52 + 8
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
