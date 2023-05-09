# added because I am not sure how complicated fishing can get
import pygame.key

from timer import Timer
from random import randint


class Fishing:

    def __init__(self, player, fishing_status):
        # check that you are not making a new object each time
        self.player = player
        self.fishing_status = fishing_status

        # timer for fish to plop
        self.fishing_timer = Timer(randint(1000, 2000), self.play_plop)

        # timer for reeling on time
        self.reel_on_time = Timer(500)

        # extra timer that reels for me
        self.extra_time = Timer(500)

        self.splash = pygame.mixer.Sound('../audio/fish flap.wav')

    def input(self):
        keys = pygame.key.get_pressed()

        # we are already fishing
        if keys[pygame.K_SPACE]:

            # pulled reel on time or not
            if self.fishing_timer.complete and self.reel_on_time.active:
                self.player.item_inventory['fish'] += 1
                # cancel the reel timer and complete it
                self.end_fishing()

                # self.fishing_timer = Timer(randint(400, 800), self.play_plop)
            else:
                self.end_fishing()

        if keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or \
                keys[pygame.K_RIGHT]:  # to cancel fishing
            self.end_fishing()

    def fishing_start(self):
        self.fishing_timer.activate()
        self.fishing_status = True

    def play_plop(self):
        self.splash.play()

    def end_fishing(self):
        """
        Resets all timers for fishing and makes the player exit fishing mode
        """
        self.fishing_timer.complete = False
        self.reel_on_time.complete = False
        self.extra_time.complete = False
        self.fishing_status = False

    def update(self):
        self.fishing_timer.update()
        self.input()
        # if the fishing timer is complete, do check for reeling, otherwise
        # set the status to complete
        if self.fishing_timer.complete:
            if self.reel_on_time.active:
                # update timer for reeling
                self.reel_on_time.update()
            elif not self.reel_on_time.complete:
                # reeling timer did not start so start it now
                self.reel_on_time.activate()
            else:
                # Both fishing and on time reeling are done, so start a new
                # timer that reels for the player
                if self.extra_time.active:
                    self.extra_time.update()
                elif not self.extra_time.complete:
                    self.extra_time.activate()  # not complete, activate
                else:
                    self.end_fishing()

