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
        self.topleft_offset = 128

        # menu image
        self.menu_image = \
            pygame.image.load('../graphics/menus/shop_2.png').convert_alpha()
        self.menu_rect = self.menu_image.get_rect(
            center=OVERLAY_POSITIONS['shop'])
        # status rects
        self.status_imgs = {
            "tools": pygame.image.load('../graphics/menus/shop/'
                                       'tools.png').convert_alpha(),
            "unplantables": pygame.image.load('../graphics/menus/shop/'
                                              'unplantables.'
                                              'png').convert_alpha(),
            "plants": pygame.image.load('../graphics/menus/shop/'
                                        'plants.png').convert_alpha()
        }
        self.status_rects = {
            "tools": self.status_imgs["tools"].get_rect(
                midright=self.menu_rect.center - Vector2(
                    self.status_imgs["unplantables"].get_width() // 2, 0)
            ),
            "unplantables": self.status_imgs["unplantables"].get_rect(
                center=self.menu_rect.center
            ),
            "plants": self.status_imgs["plants"].get_rect(
                midleft=self.menu_rect.center + Vector2(
                    self.status_imgs["unplantables"].get_width() // 2, 0)
            )
        }
        # menu arrows
        path = "../graphics/menus/shop/"
        self.shop_imgs = {
            "left": pygame.image.load(f'{path}left_arrow.png').convert_alpha(),
            "left_p": pygame.image.load(f'{path}left_arrow_pressed.png'
                                        ).convert_alpha(),
            "right": pygame.image.load(f'{path}/right_arrow.png'
                                       ).convert_alpha(),
            "right_p": pygame.image.load(f'{path}right_'
                                         'arrow_pressed.'
                                         'png').convert_alpha(),
            "plus": pygame.image.load(f'{path}/plus.png').convert_alpha(),
            "plus_p": pygame.image.load(f'{path}plus_pressed.png'
                                        ).convert_alpha(),
            "minus": pygame.image.load(f'{path}/minus.png').convert_alpha(),
            "minus_p": pygame.image.load(f'{path}minus_pressed.png'
                                         ).convert_alpha(),
            "exit": pygame.image.load(f'{path}exit_shop.png'
                                      ).convert_alpha(),
            "exit_p": pygame.image.load(f'{path}exit_shop_pressed.png'
                                        ).convert_alpha()
        }
        calc_height_diff = self.shop_imgs["left"].get_height() \
                           - self.shop_imgs["left_p"].get_height()
        height_diff_exit = self.shop_imgs["exit"].get_height() - \
                                self.shop_imgs["exit_p"].get_height()
        self.shop_imgs_rects = {
            "left": self.shop_imgs["left"].get_rect(
                bottomleft=self.menu_rect.bottomleft +
                           Vector2(64, -64)),
            "right": self.shop_imgs["right"].get_rect(
                bottomright=self.menu_rect.bottomright +
                            Vector2(-64, -64)),
            "left_p": self.shop_imgs["left"].get_rect(
                bottomleft=self.menu_rect.bottomleft +
                           Vector2(64, -64 + calc_height_diff)),
            "right_p": self.shop_imgs["right"].get_rect(
                bottomright=self.menu_rect.bottomright +
                            Vector2(-64, -64 + calc_height_diff)),
            "exit": self.shop_imgs["exit"].get_rect(
                topleft=self.menu_rect.topleft +
                        Vector2(self.topleft_offset // 2,
                                self.topleft_offset // 2)
            ),
            "exit_p": self.shop_imgs["exit_p"].get_rect(
                topleft=self.menu_rect.topleft +
                        Vector2(self.topleft_offset // 2,
                                self.topleft_offset // 2 + height_diff_exit)
            )
        }
        self.plus_minus_rects = {}
        self.left_arrow = self.shop_imgs["left"]
        self.left_arrow_rect = self.shop_imgs_rects["left"]
        self.right_arrow = self.shop_imgs["right"]
        self.right_arrow_rect = self.shop_imgs_rects["right"]
        self.exit_button = self.shop_imgs["exit"]
        self.exit_button_rect = self.shop_imgs_rects["exit"]
        self.plus_minus_lst = [[self.shop_imgs["plus"],
                                self.shop_imgs["plus_p"],
                                self.shop_imgs["minus"],
                                self.shop_imgs["minus_p"]] for _ in
                               range(len(self.player.seed_inventory.values()))]

        # imaging setup
        self.space = 5
        self.padding = 5
        self.topleft_items = self.menu_rect.topleft + \
                             Vector2(self.topleft_offset, self.topleft_offset)

        # entries
        self.tools = self.player.tools
        self.items = list(self.player.item_inventory.keys())
        self.seeds = self.player.seeds
        self.sell_border = len(self.player.item_inventory) - 1
        self.max_entries = 10

        # surfs
        self.tool_text_surfs = []
        self.item_nonplant_text_surfs = []
        self.item_text_plant_surf = []
        self.seed_text_surfs = []

        self.tool_text = self.item_text = self.seed_text = None

        self.setup()
        self.lst = self.item_nonplant_text_surfs

        # movement
        self.page_number = 0
        self.status_page = "selection screen"
        self.index = 0
        self.timer = Timer(250)

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
            text_surf = self.font.render("", False, 'Black')
            self.seed_text_surfs.append(text_surf)

    def display_selection_shop(self):
        """
        Displays the selection boxes for the player to select what they can buy.
        :return: NoneType
        """
        for key, image in self.status_imgs.items():
            self.display_surface.blit(image, self.status_rects[key])

    def display_money(self):
        """Displays the money that the player has."""
        text_surf = self.font.render(f'${self.player.money}', False, 'Black')
        text_rect = pygame.Rect(0, 0,
                                text_surf.get_width(),
                                text_surf.get_height())
        text_rect.midbottom = self.menu_rect.midbottom + \
                              Vector2(0, - self.padding * 6)

        self.display_surface.blit(text_surf, text_rect)

    def display_arrows(self):
        """Displays the arrows to change pages in the shop"""
        mousex, mousey = pygame.mouse.get_pos()
        if self.shop_imgs_rects["left"].collidepoint(mousex, mousey):
            self.left_arrow = self.shop_imgs["left_p"]
            self.left_arrow_rect = self.shop_imgs_rects["left_p"]
        else:
            self.left_arrow = self.shop_imgs["left"]
            self.left_arrow_rect = self.shop_imgs_rects["left"]

        self.display_surface.blit(self.left_arrow, self.left_arrow_rect)

        if self.shop_imgs_rects["right"].collidepoint(mousex, mousey):
            self.right_arrow = self.shop_imgs["right_p"]
            self.right_arrow_rect = self.shop_imgs_rects["right_p"]
        else:
            self.right_arrow = self.shop_imgs["right"]
            self.right_arrow_rect = self.shop_imgs_rects["right"]

        self.display_surface.blit(self.right_arrow, self.right_arrow_rect)

        if self.shop_imgs_rects["exit"].collidepoint(mousex, mousey):
            self.exit_button = self.shop_imgs["exit_p"]
            self.exit_button_rect = self.shop_imgs_rects["exit_p"]
        else:
            self.exit_button = self.shop_imgs["exit"]
            self.exit_button_rect = self.shop_imgs_rects["exit"]

        self.display_surface.blit(self.exit_button,
                                  self.exit_button_rect)

    def display_plus_minus(self, text_rect: pygame.Rect, index: int):
        """Displays the plus and minus signs to buy or sell in the shop."""
        mousex, mousey = pygame.mouse.get_pos()

        height_diff = self.plus_minus_lst[index // 2][0].get_height() - \
                      self.plus_minus_lst[index // 2][1].get_height()

        image_1 = self.plus_minus_lst[index // 2][0]  # plus (right)
        image_2 = self.plus_minus_lst[index // 2 + 1][2]  # minus (left)

        rect_1 = image_1.copy().get_rect(topleft=text_rect.topleft +
                                                 Vector2(text_rect.width +
                                                         self.padding * 3,
                                                         2))
        if rect_1.collidepoint(mousex, mousey):
            image_1 = self.plus_minus_lst[index // 2][1]
            rect_1.topleft += Vector2(0, height_diff)

        rect_2 = image_2.copy().get_rect(topleft=text_rect.topleft +
                                                 Vector2(-(image_2.get_width() +
                                                           self.padding * 3),
                                                         2))

        if rect_2.collidepoint(mousex, mousey):
            image_2 = self.plus_minus_lst[index // 2][3]
            rect_2.topleft += Vector2(0, height_diff)

        self.plus_minus_rects[(index, 1)] = rect_1
        self.plus_minus_rects[(index, -1)] = rect_2
        self.display_surface.blit(image_1, rect_1)
        self.display_surface.blit(image_2, rect_2)

    def show_entry(self, text_surf, amount: int, index: int):
        """
        This shows an entry in the shop.
        :param text_surf: Surface representing the current item
        :param amount: Number representing how much of that item there is
        :param index: Index of the item in list
        :param selected: boolean representing whether the item is selected
        :return:
        """
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
                                                    - Vector2(self.padding * 10,
                                                              0))
        self.display_plus_minus(amount_rect, index)
        self.display_surface.blit(amount_surf, amount_rect)

        # selected
        # if selected:
        #     pygame.draw.rect(self.display_surface, 'black', bg_rect, 4, 4)

    def display_unplantables_screen(self):
        """Displays the unplantables screen"""
        amount_list = [val for key, val in
                       self.player.item_inventory.items()
                       if key not in self.player.seeds]
        self.lst = self.item_nonplant_text_surfs

        for text_ind, text_surf in enumerate(self.lst):
            amount = amount_list[text_ind]
            self.show_entry(text_surf, amount, text_ind)

    def display_plants_screen(self):
        """Displays the plants screen"""
        item_amount_list = [val for key, val in
                            self.player.item_inventory.items()
                            if key in self.player.seeds]
        seed_amount_list = [val for val in
                            self.player.seed_inventory.values()]

        num_0 = self.max_entries * self.page_number
        if self.max_entries * (self.page_number + 1) > \
                len(item_amount_list):
            num_1 = len(item_amount_list)
        else:
            num_1 = self.max_entries * (self.page_number + 1)

        self.lst = item_amount_list[num_0:num_1] + \
                   seed_amount_list[num_0:num_1]

        entries = self.max_entries
        for i in range(0, len(self.lst) // 2):
            if entries > 0:
                amount = item_amount_list[i + num_0]
                text_surf = self.item_text_plant_surf[i + num_0]
                self.show_entry(text_surf, amount, 2 * i)
                amount = seed_amount_list[i + num_0]
                text_surf = self.seed_text_surfs[i + num_0]
                self.show_entry(text_surf, amount, 2 * i + 1)
                entries -= 1

    def display_tools_screen(self):
        """Displays the plants screen"""
        # for i in range
        # if index % 2 == 0:
        #     calc_x = 0
        #     calc_y = (text_surf.get_height() + self.padding * 4) * index // 2
        #     top_left_calc = self.topleft_items + Vector2(calc_x, calc_y)
        # else:
        #     calc_x = self.menu_rect.width // 2 - self.topleft_offset
        #     calc_y = (text_surf.get_height() + self.padding * 4) * \
        #              (index - 1) // 2
        #
        #     top_left_calc = self.topleft_items + Vector2(calc_x, calc_y)
        ...

    def input(self):
        # get the input and then if the player presses esc, close the menu
        keys = pygame.key.get_pressed()
        self.timer.update()

        if keys[pygame.K_ESCAPE]:
            self.toggle_menu()

        if not self.timer.active:

            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.timer.activate()
                mousex, mousey = pygame.mouse.get_pos()

                if self.status_page == "selection screen":
                    for key, rect in self.status_rects.items():
                        if rect.collidepoint(mousex, mousey):
                            self.status_page = key

                if self.status_page == "plants":

                    if self.shop_imgs_rects["left"].collidepoint(mousex,
                                                                 mousey):
                        self.page_number -= 1
                    if self.shop_imgs_rects["right"].collidepoint(mousex,
                                                                  mousey):
                        self.page_number += 1

                    for key, rect in self.plus_minus_rects.items():
                        if rect.collidepoint(mousex, mousey):
                            # this variable (index) has index in 0th place
                            # and has a number representing whether
                            # it is plus or minus
                            index = key[0]
                            #  + self.page_number*self.max_entries
                            item = list(self.player.seed_inventory.keys())[
                                index // 2 +
                                self.page_number * self.max_entries]
                            if index % 2 == 0:
                                # you are coding a function in player.py to buy
                                # and sell, you need to figure out how you will
                                # implement pricing :D hopefully you can
                                # add the input in a way that drags the logic
                                # in a good way. Good night.
                                self.player.player_add(item, key[1],
                                                       transact_shop=True)
                            else:
                                self.player.player_add_seed(item, key[1],
                                                            transact_shop=True)

                if self.status_page != "selection screen":
                    if self.exit_button_rect.collidepoint(mousex, mousey):
                        self.status_page = "selection screen"

        # clamo the values
        if self.index < 0:
            self.index = len(self.lst) // 2 - 1
        if self.index > len(self.lst) // 2 - 1:
            self.index = 0

    def update(self):
        self.input()

        self.display_surface.blit(self.menu_image, self.menu_rect)
        if self.status_page != "selection screen":
            self.display_money()
            self.display_arrows()

        if self.status_page == "selection screen":
            self.display_selection_shop()
        elif self.status_page == "unplantables":
            self.display_unplantables_screen()
        elif self.status_page == "plants":
            self.display_plants_screen()
        else:
            self.display_tools_screen()


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
            # update: figured it out slightly after, check commits, one of them
            # has it.
            if keys[pygame.K_d]:
                row_len = len(self.item_array[self.curr_ind[0]])
                if self.curr_ind[0] + 1 == row_len:
                    self.box_rect.left -= (52 + 8) * (row_len - 1)
                    self.curr_ind[0] = 0
                else:
                    self.box_rect.left += 52 + 8
                    self.curr_ind[0] += 1

                self.timer.activate()

            if keys[pygame.K_a]:
                row_len = len(self.item_array[self.curr_ind[0]])
                if self.curr_ind[0] - 1 < 0:
                    self.box_rect.left += (52 + 8) * row_len
                    self.curr_ind[0] = row_len
                else:
                    self.box_rect.left -= 52 + 8
                    self.curr_ind[0] -= 1

                self.timer.activate()

            if keys[pygame.K_w]:
                col_len = len(self.item_array)
                if self.curr_ind[1] - 1 < 0:
                    self.box_rect.top += (52 + 8) * (col_len - 1)
                    self.curr_ind[1] = col_len - 1
                else:
                    self.box_rect.top -= 52 + 8
                    self.curr_ind[1] -= 1

                self.timer.activate()

            if keys[pygame.K_s]:
                col_len = len(self.item_array)
                if self.curr_ind[1] + 1 == col_len:
                    self.box_rect.top -= (52 + 8) * (col_len - 1)
                    self.curr_ind[1] = 0
                else:
                    self.box_rect.top += 52 + 8
                    self.curr_ind[1] += 1

                self.timer.activate()

            try:
                if keys[pygame.K_1]:
                    item = self.item_array[self.curr_ind[1]][self.curr_ind[0]]
                    if self.player.get_unlocked(item):
                        self.held_items[0] = item
                if keys[pygame.K_2]:
                    item = self.item_array[self.curr_ind[1]][self.curr_ind[0]]
                    if self.player.get_unlocked(item):
                        self.held_items[1] = item
                if keys[pygame.K_3]:
                    item = self.item_array[self.curr_ind[1]][self.curr_ind[0]]
                    if self.player.get_unlocked(item):
                        self.held_items[2] = item
                if keys[pygame.K_4]:
                    item = self.item_array[self.curr_ind[1]][self.curr_ind[0]]
                    if self.player.get_unlocked(item):
                        self.held_items[3] = item
                if keys[pygame.K_5]:
                    item = self.item_array[self.curr_ind[1]][self.curr_ind[0]]
                    if self.player.get_unlocked(item):
                        self.held_items[4] = item
            except IndexError:
                print("No item here yet :D")

        if keys[pygame.K_ESCAPE]:
            # this is here to make sure the item is currently holding correctly
            # updates
            self.player.selected_hand = \
                self.held_items[self.player.held_items_index]
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
