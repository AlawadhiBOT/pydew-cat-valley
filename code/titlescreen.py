from code.settings import *
from support import *


class TitleScreen:
    def __init__(self):
        """
        Class to handle title screen, and possibly logins.
        """
        norm = os.path.normpath
        self.title_path = "graphics/title"
        self.background_image = pygame.image.load(norm(CURR_PATH +
                                                       f"{self.title_path}/"
                                                       f"screens"
                                                       "background-for-"
                                                       "title-screen.png")
                                                  ).convert_alpha()
        self.buttons = import_folder_dict2(f"{self.title_path}/buttons/")


