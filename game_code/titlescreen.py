# Copyright (c) 2025 Your Name
# Licensed under the AGPLv3 License. See LICENSE file for details.
#
# This project is based on a tutorial (link: https://www.youtube.com/watch?v=T4IX36sP_0c).
# You can redistribute and/or modify it under the terms of the AGPLv3.
#
# This software comes with no warranty. See the LICENSE file for more information.

from game_code.settings import *
from game_code.support import *


class TitleScreen:
    def __init__(self):
        """
        Class to handle title screen, and possibly logins.
        """
        norm = os.path.normpath
        self.display_surface = pygame.display.get_surface()

        self.title_path = CURR_PATH + "/graphics/title"
        self.background_image = pygame.image.load(norm(f"{self.title_path}/"
                                                       f"screens/"
                                                       "background-for-"
                                                       "title-screen.png")
                                                  ).convert_alpha()
        self.background_image_login = (
            pygame.image.load(norm(f"{self.title_path}/screens/background-for-"
                                   "title-screen.png")
                              ).convert_alpha())
        infoObject = pygame.display.Info()
        width, height = infoObject.current_w, infoObject.current_h
        self.background_image = pygame.transform.scale(self.background_image,
                                                       (width, height))
        self.background_image_rect = self.background_image.get_rect()

        self.buttons = import_folder_dict(norm(f"{self.title_path}/buttons/"))
        self.buttons_rects = {key: value.get_rect() for key, value in
                              self.buttons.items()}
        self.active_buttons = {"play": "play_button",
                               "login": "login_button"}
        self.setup()

        self.status = "title"

    def setup(self):
        """Fixes position of some things"""
        self.buttons_rects["login_button"].midbottom = \
            OVERLAY_POSITIONS["inven"]
        self.buttons_rects["login_button_pressed"].midbottom = \
            self.buttons_rects["login_button"].midbottom

        self.buttons_rects["play_button"].midbottom = \
            self.buttons_rects["login_button"].midtop - Vector2(0, 10)
        self.buttons_rects["play_button_pressed"].midbottom = \
            self.buttons_rects["play_button"].midbottom

    def display_buttons(self):
        for val in self.active_buttons.values():
            self.display_surface.blit(self.buttons[val],
                                      self.buttons_rects[val])

    def input(self):
        keys = pygame.key.get_pressed()

        mousex, mousey = pygame.mouse.get_pos()

        for key, button in self.active_buttons.items():
            if pygame.mouse.get_pressed(num_buttons=3)[0] and \
                    self.buttons_rects[button].collidepoint(mousex, mousey):
                if "pressed" not in button:
                    self.status = "".join(button.split("_")[:-1])
                    print(self.status)
                    self.active_buttons[key] = button + "_pressed"
            else:
                if "_pressed" in button:
                    new_button = button[0:button.rfind("_pressed")]
                else:
                    new_button = button
                self.active_buttons[key] = new_button

    def run(self, dt):
        """
        Runs the title page
        """
        self.display_surface.fill("black")

        if self.status == "title":
            self.display_surface.blit(self.background_image,
                                      self.background_image_rect)
        if self.status == "play":
            pass

        self.display_buttons()
        self.input()
