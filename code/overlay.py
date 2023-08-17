import pygame
from code.support import import_folder_dict2
from code.settings import *
from code.player import Player
from code.timer import Timer


class Overlay:
    """
    This function is used to display the overlay, which includes the following:
    - Seeds and tool used on the bottom left
    - Levels, xp, stamina, and hp
    - Displays the selected tool in text on the bottom right
    """

    def __init__(self, player: Player, items: list):
        # general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.items = items

        # imports
        norm = os.path.normpath
        overlay_path = CURR_PATH + '/graphics/overlay/'
        self.tools_surf = {tool: pygame.image.load(norm(f'{overlay_path}tools/'
                                                   f'{tool}.png')
                                                   ).convert_alpha()
                           for tool in player.tools}
        self.seeds_surf = {seed: pygame.image.load(norm(f'{overlay_path}{seed}'
                                                   f'.png')).convert_alpha()
                           for seed in player.seeds}

        self.font = pygame.font.Font(norm(CURR_PATH +
                                          '/font/LycheeSoda.ttf'), 30)

        # toolbox overlay
        self.overlay_surf = pygame.image.load(norm(CURR_PATH +
                                                   '/graphics/overlay/tools/'
                                              'tools.png')).convert_alpha()
        self.overlay_rect = self.overlay_surf.get_rect(midbottom=
                                                       OVERLAY_POSITIONS
                                                       ['inven'])

        self.box_img = pygame.image.load(norm(CURR_PATH + '/graphics/overlay/'
                                                          'tools/selector.png')
                                         ).convert_alpha()
        self.box_rect = self.box_img.get_rect(topleft=
                                              self.overlay_rect.topleft +
                                              Vector2(26, 25))

        # xp and level and held item overlay
        self.xp_bar_surf = pygame.image.load(norm(CURR_PATH + '/graphics/'
                                                              'overlay/stats/'
                                                              'xp_bar.png')
                                             ).convert_alpha()
        self.xp_bar_rect = self.xp_bar_surf.get_rect(midbottom=
                                                     self.overlay_rect.midtop)
        self.xp_no_surf = self.font.render(
            f'{self.player.player_stats["level"]}', False, 'Green')
        self.xp_no_rect = self.xp_no_surf.get_rect(midbottom=
                                                   self.xp_bar_rect.midtop)
        self.item_held = self.font.render(f'{items[0]}', False, 'Green')
        self.display_item_held_timer = Timer(500)

        # health and gold section overlay
        self.stats_overlay_surf = pygame.image.load(norm(CURR_PATH +
                                                         '/graphics/overlay/'
                                                         'stats/hp_gold.png')
                                                    ).convert_alpha()
        self.stats_overlay_rect = self.stats_overlay_surf.get_rect(topleft=
                                                                   (0, 0))
        # heart surf
        self.f_heart_surfs = [pygame.image.load(norm(CURR_PATH +
                                                     '/graphics/overlay/stats/'
                                                     'heart.png')
                                                ).convert_alpha()
                              for _ in range(self.player.max_hp)]
        self.f_heart_rects = [heart.get_rect() for heart in self.f_heart_surfs]
        self.h_heart_surfs = [pygame.image.load(norm(CURR_PATH +
                                                     '/graphics/overlay/stats/'
                                                     'half_heart.png')
                                                ).convert_alpha()
                              for _ in range(self.player.max_hp)]
        self.h_heart_rects = [heart.get_rect() for heart in self.h_heart_surfs]
        self.e_heart_surfs = [pygame.image.load(norm(CURR_PATH +
                                                     '/graphics/overlay/stats/'
                                                     'empty_heart.png')
                                                ).convert_alpha()
                              for _ in range(self.player.max_hp)]
        self.e_heart_rects = [heart.get_rect() for heart in self.e_heart_surfs]
        # gold overlay
        self.gold_img = pygame.image.load(norm(CURR_PATH +
                                               '/graphics/overlay/stats/'
                                               'gold.png')
                                          ).convert_alpha()
        self.gold_rect = self.gold_img.get_rect(bottomleft=
                                                self.stats_overlay_rect.
                                                bottomleft + Vector2(13, -11))
        self.gold_txt_surf = self.font.render(
            f'{self.player.player_stats["money"]}',
            False,
            (182, 137, 98))
        self.gold_txt_rect = self.gold_txt_surf.get_rect(midleft=
                                                         self.gold_rect.midright
                                                         + Vector2(5, 0))

        # stamina bar overlay
        self.stamina_bar_img = pygame.image.load(norm(CURR_PATH +
                                                      '/graphics/overlay/'
                                                      'stats/stamina_bar.png')
                                                 ).convert_alpha()
        self.stamina_bar_rect = self.stamina_bar_img.get_rect(bottomright=
                                                              OVERLAY_POSITIONS
                                                              ['stamina'])

        # character box
        self.chara_box_surf = pygame.image.load(norm(CURR_PATH +
                                                     '/graphics/overlay/stats/'
                                                     'character_box.png')
                                                ).convert_alpha()
        self.chara_box_rect = self.chara_box_surf.get_rect(bottomleft=
                                                           OVERLAY_POSITIONS
                                                           ['character_box'])
        # character emote imports
        path = CURR_PATH + "/graphics/overlay/teemo_emotes"
        self.teemo_emotes = import_folder_dict2(path)
        self.frame_index = 0
        self.actions_index = 0
        self.actions_list = []
        for key in self.teemo_emotes.keys():
            if "sleep" not in key:
                self.actions_list += ["idle" for _ in range(3)] + [key]
        self.status = self.actions_list[self.actions_index]
        self.image = self.teemo_emotes[self.status][self.frame_index]
        self.image_rect = None

    def toolbox_display(self):
        """
        Handles the display of the toolbox
        :return: NoneType
        """
        # inventory
        self.display_surface.blit(self.overlay_surf, self.overlay_rect)

        # held items rendering
        for index, item in enumerate(self.items):
            if item in self.player.tools:
                # for the calculation, perhaps it may be best to use the size of
                # each box (52x52)
                surf = self.tools_surf[item]

                location = self.overlay_rect.topleft + \
                           Vector2(30 + index * (surf.get_width() * 1.5),
                                   29)
                item_rect = surf.get_rect(topleft=location)
                self.display_surface.blit(surf, item_rect)

            elif item in self.player.seeds:
                surf = self.seeds_surf[item]

                location = self.overlay_rect.topleft + \
                           Vector2(30 + index * (surf.get_width() * 1.5),
                                   29)
                item_rect = surf.get_rect(topleft=location)
                self.display_surface.blit(surf, item_rect)

                text_surf = self.font.render(
                    str(self.player.seed_inventory[item]),
                    False, 'Green')
                text_rect = item_rect.bottomright + Vector2(-12, -24)
                self.display_surface.blit(text_surf, text_rect)

        # selector
        self.move_box(self.player.held_items_index)
        self.display_surface.blit(self.box_img, self.box_rect)

        # stamina bar
        self.display_surface.blit(self.stats_overlay_surf,
                                  self.stats_overlay_rect)

    def xp_level_item_display(self):
        """
        Handles the display of the xp bar and the level of the player.
        :return: NoneType
        """
        self.display_surface.blit(self.xp_bar_surf, self.xp_bar_rect)
        num = 4
        topleft = self.xp_bar_rect.topleft + Vector2(num, num)
        percent = self.player.player_stats["xp"] / \
                  self.player.player_stats["max_xp"]
        Rect = pygame.Rect(topleft, ((self.xp_bar_rect.width - num * 2) *
                                     percent,
                                     self.xp_bar_rect.height - num * 2))
        pygame.draw.rect(self.display_surface, 'Green',
                         Rect, 0, 0)
        self.xp_no_surf = self.font.render(
            f'{self.player.player_stats["level"]}',  False, 'Green')
        self.display_surface.blit(self.xp_no_surf, self.xp_no_rect)

    def heart_gold_display(self):
        """
        Handles the display of the hearts and gold on the top left
        :return: NoneType
        """
        # heart top left is 6, 6 and 27, 6
        # heart width is 18, height is 20, so second heart comes 3 px after
        # heart to make look good.
        last_tl = OVERLAY_POSITIONS['heart']

        adder = 0
        for i in range(self.player.hp // 2):
            calc = last_tl + Vector2((self.f_heart_surfs[i].get_width() + 3) *
                                     (i % 9),
                                     (self.f_heart_surfs[i].get_height() + 3)
                                     * (i // 9))
            self.f_heart_rects[i].topleft = calc
            self.display_surface.blit(self.f_heart_surfs[i],
                                      self.f_heart_rects[i])
        adder += self.player.hp // 2
        for i in range(self.player.hp % 2):
            calc = last_tl + Vector2((self.h_heart_surfs[i].get_width() + 3)
                                     * ((i + adder) % 9),
                                     (self.h_heart_surfs[0].get_height() + 3)
                                     * ((i + adder) // 9))
            self.h_heart_rects[i].topleft = calc
            self.display_surface.blit(self.h_heart_surfs[i],
                                      self.h_heart_rects[i])

        adder += self.player.hp % 2
        for i in range((self.player.max_hp - self.player.hp) // 2):
            calc = last_tl + Vector2((self.e_heart_surfs[i].get_width() + 3)
                                     * ((i + adder) % 9),
                                     (self.e_heart_surfs[i].get_height() + 3)
                                     * ((i + adder) // 9))
            self.e_heart_rects[i].topleft = calc
            self.display_surface.blit(self.e_heart_surfs[i],
                                      self.e_heart_rects[i])

        self.display_surface.blit(self.gold_img, self.gold_rect)
        self.gold_txt_surf = self.font.render(
            f'{self.player.player_stats["money"]}',
            False,
            (182, 137, 98))
        self.display_surface.blit(self.gold_txt_surf, self.gold_txt_rect)

    def stamina_bar_display(self):
        """
        Function to display the stamina bar
        :return: NoneType
        """
        self.display_surface.blit(self.stamina_bar_img, self.stamina_bar_rect)

        # stamina top left 4, 12
        top_left = self.stamina_bar_rect.topleft + Vector2(4, 12)

        Rect = pygame.Rect(top_left, (self.stamina_bar_img.get_width() // 2,
                                      self.stamina_bar_img.get_height() - 24))
        percent_stamina = self.player.player_stats["xp"] / \
                          self.player.player_stats["max_stamina"]
        Rect = Rect.inflate(0, -(Rect.height - Rect.height * percent_stamina))
        result = self.threshold_marker(percent_stamina)
        pygame.draw.rect(self.display_surface,
                         result, Rect, 0, 0)

    @staticmethod
    def threshold_marker(percentage: float) -> tuple[int, int, int]:
        """
        Function serves as a way to get the color which represents the stamina the player is
        at.
        :param percentage: float representing the percentage stamina
        :return: tuple containing 3 ints representing RGB colors
        """
        if percentage == 1:
            return STAMINA_COLORS["very happy"]
        if percentage >= .75:
            return STAMINA_COLORS["happy"]
        if percentage >= .50:
            return STAMINA_COLORS["normal"]
        if percentage >= .25:
            return STAMINA_COLORS["unhappy"]
        if percentage >= 0:
            return STAMINA_COLORS["sad"]

        return STAMINA_COLORS["dead"]

    def character_box_display(self, dt):
        """
        Function to display character
        :return: NoneType
        """
        self.display_surface.blit(self.chara_box_surf, self.chara_box_rect)

        self.frame_index += len(self.teemo_emotes[self.status]) ** 2 * dt
        if self.frame_index >= len(self.teemo_emotes[self.status]):
            self.frame_index = 0

            self.actions_index += 1
            if self.actions_index >= len(self.actions_list):
                self.actions_index = 0

            self.status = self.actions_list[self.actions_index]

        self.image = self.teemo_emotes[self.status][int(self.frame_index)]
        # 33, 30 is top left for character after checking on paint.net
        self.image_rect = self.image.get_rect(topleft=
                                              self.chara_box_rect.topleft +
                                              Vector2(27, 30))

        self.display_surface.blit(self.image, self.image_rect)

    def held_item_display(self):
        """
        Displays held item briefly
        :return: NoneType
        """
        item = self.player.held_items[self.player.held_items_index]
        if item != "cat":
            self.item_held = self.font.render(item, False, 'Green')
            rect = self.item_held.get_rect(midbottom=self.xp_no_rect.midtop)
            self.display_surface.blit(self.item_held, rect)

    def move_box(self, num):
        """
        Calculates the correct location of the box selector box.
        :param num: int
        :return: NoneType
        """
        num = num % len(self.player.held_items)
        self.box_rect.topleft = self.overlay_rect.topleft + \
                                Vector2(26, 25) + \
                                Vector2((52 + 8) * num, 0)

    def display(self, dt: float):
        self.toolbox_display()
        self.xp_level_item_display()
        self.heart_gold_display()
        self.stamina_bar_display()
        self.character_box_display(dt)
        if self.player.timers['swap'].active:
            if not self.display_item_held_timer.active:
                self.display_item_held_timer.activate()
        self.display_item_held_timer.update()
        if self.display_item_held_timer.active:
            self.held_item_display()
