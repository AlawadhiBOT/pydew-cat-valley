from typing import Callable
import pygame


class PlayerSettings:
    """
    This file is intended for the player to access the ingame settings, such as
    - Logging out
    - Increasing/Decreasing volume
    - Or any similar things...
    """

    def __init__(self, player: Player, toggle_settings: Callable):

        # general setup
        self.player = player
        self.toggle_menu = toggle_menu
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(path.join(CURR_PATH, 'font',
                                               'LycheeSoda.ttf'), 30)

        self.topleft_offset = 128