import pygame
from settings import *


class Overlay:
    """
    This function is used to display the overlay, which includes the following:
    - Seeds and tool used on the bottom left
    - Levels, xp, stamina, and hp
    - Displays the selected tool in text on the bottom right
    """
    def __init__(self, player):
        # general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player

        # imports
        overlay_path = '../graphics/overlay/'
        self.tools_surf = {tool: pygame.image.load(f'{overlay_path}{tool}'
                                                   f'.png').convert_alpha()
                           for tool in player.tools}
        self.seeds_surf = {seed: pygame.image.load(f'{overlay_path}{seed}'
                                                   f'.png').convert_alpha()
                           for seed in player.seeds}

        self.font = pygame.font.Font('../font/LycheeSoda.ttf', 30)
        # options
        self.width = 400
        self.space = 10
        self.padding = 8

    def display(self):
        # tools
        tools_surf = self.tools_surf[self.player.selected_tool]
        tool_rect = tools_surf.get_rect(midbottom=OVERLAY_POSITIONS['tool'])
        self.display_surface.blit(tools_surf, tool_rect)

        # seeds
        seed_surf = self.seeds_surf[self.player.selected_seed]
        seed_rect = seed_surf.get_rect(midbottom=OVERLAY_POSITIONS['seed'])
        self.display_surface.blit(seed_surf, seed_rect)

        # stamina bar
        sta_surf = self.font.render(f'LVL:{self.player.level}\n'
                                    f'STA:{self.player.stamina}/'
                                    f'{self.player.max_stamina}\n'
                                    f'XP:{self.player.xp}/'
                                    f'{self.player.max_xp}\n'
                                    f'HP:{self.player.hp}/'
                                    f'{self.player.max_hp}',
                                    False, 'Black')
        sta_rect = sta_surf.get_rect(
            topleft=OVERLAY_POSITIONS['stamina'])

        pygame.draw.rect(self.display_surface, 'White',
                         sta_rect.inflate(10, 10), 0, 6)
        self.display_surface.blit(sta_surf, sta_rect)
        for text in self.player.display_text:
            text[2].update()
            if text[2].active:
                self.display_surface.blit(text[0], text[1])
