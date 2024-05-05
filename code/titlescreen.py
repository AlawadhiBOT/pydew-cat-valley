from code.settings import *
from support import *
from os import path


class TitleScreen:
    def __init__(self):
        """
        Class to handle title screen, and possibly logins.
        """
        self.title_path = path.join("graphics", "title")
        self.background_image = pygame.image.load(path.join(
            CURR_PATH, self.title_path, "screens",
                                        "background-for-title-screen.png")
        ).convert_alpha()
        self.buttons = import_folder_dict2(f"{self.title_path}/buttons/")
