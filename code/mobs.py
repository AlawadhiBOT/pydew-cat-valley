from typing import Callable

import pygame
from timer import Timer
from random import choice, randint, random

class NeutralMob(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups: pygame.sprite.Group, z,
                 player_pos: Callable):
        self.frames = frames
        self.frame_index = 0

        self.image = self.frames["idle"][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate(self.rect.width * 0.2,
                                               self.rect.height * 0.75)

        super().__init__(groups)

        self.health = 5
        self.alive = True
        self.default_speed = self.speed = 50

        self.direction = pygame.math.Vector2()
        self.player_pos_func = player_pos
        self.status = "idle"
        self.player_dmg_timer = Timer(1000)
        self.animation_lock = False


class Slime(NeutralMob):
    """
    This is the Slime class, originally developed for the forest area
    """
    def __init__(self, pos, frames, groups: pygame.sprite.Group, z,
                 player_pos: Callable, detection_area: list,
                 reduce_player_hp: Callable):
        super().__init__(pos=pos, frames=frames, z=z, groups=groups,
                         player_pos=player_pos)

        self.detection_area = detection_area
        self.reduce_player_hp = reduce_player_hp

        # sounds
        self.axe_sound = pygame.mixer.Sound('../audio/axe.mp3')

    def animate(self, dt: float):
        self.frame_index += 5 * dt
        if self.frame_index >= len(self.frames[self.status]):
            if self.health <= 0:
                return None
            self.frame_index = 0
            self.animation_lock = False

        self.image = self.frames[self.status][int(self.frame_index)]

        # Horizontal
        self.rect.x += self.direction.x * self.speed * dt

        # Vertical Movement
        self.rect.y += self.direction.y * self.speed * dt

    def move(self):

        player_pos = self.player_pos_func()
        if self.detection_area[0][0] < \
                player_pos[0] < self.detection_area[1][0] and \
                self.detection_area[0][1] < \
                player_pos[1] < self.detection_area[1][1] and \
                self.health > 0:

            if self.rect.x - 20 < player_pos[0] < self.rect.x + 20 and \
                    self.rect.y - 20 < player_pos[1] < self.rect.y + 20 and \
                    not self.animation_lock:
                self.status = "jump"
                if not self.player_dmg_timer.active:
                    self.player_dmg_timer.activate()
                    self.reduce_player_hp()
            elif not self.animation_lock:
                self.status = "move"

            if player_pos[0] > self.rect.x:  # slime is to the left of player
                self.direction.x = 1
            else:  # slime is the right of player
                self.direction.x = -1

            if player_pos[1] > self.rect.y:  # slime is below the player
                self.direction.y = 1
            else:  # slime is the above the player
                self.direction.y = -1

        elif self.health > 0:
            if not self.animation_lock:
                self.status = "idle"
            self.direction.x = 0
            self.direction.y = 0
        else:
            self.status = "death"

    def damage(self):
        if self.health > 0:

            self.health -= 1

            self.status = "hit"
            self.animation_lock = True
            self.axe_sound.play()
        else:
            self.status = "death"

    def slime(self):
        """
        Added this function in order for it to be easier for the player to hit the slime.
        :return: pygame rect which has the hitbox of the slime
        """
        self.hitbox = self.rect.copy().inflate(self.rect.width * 0.2,
                                               self.rect.height * 0.75)
        return self.hitbox

    def update(self, dt):
        self.player_dmg_timer.update()
        self.move()
        self.animate(dt)


class Cow(NeutralMob):

    def __init__(self, pos, frames, groups: pygame.sprite.Group, z,
                 player_pos: Callable):
        super().__init__(pos, frames, groups, z, player_pos)

        self.detection_area = ((self.rect.x - 500, self.rect.y - 500),
                               (self.rect.x + 500, self.rect.y + 500))

        self.speed = self.default_speed = 40
        self.pathing = False

        # need to make attribute multiplier so that I can more accurately
        # calculate delta time for each action

        # Also need some precomputed randomizer of actions
        # maybe randint is a good choice for what actions I can do, but
        # obviously need to account for the fact that I need to stand up if
        # the cow is sleeping before starting to move.
        self.action_indices = {"idle": 0, "move_left": 1, "move_right": 2,
                               "sit": 3, "sit_idle": 4, "sleep": 5,
                               "stand_up": 6, "grass_find": 7, "munch": 8}


    def animate(self, dt):
        self.frame_index += 0.5 * dt * len(self.frames[self.status])
        if self.frame_index >= len(self.frames[self.status]):
            self.frame_index = 0
            if not self.pathing:
                self.action_picker()

        self.image = self.frames[self.status][int(self.frame_index)]

        # Horizontal
        self.rect.x += self.direction.x * self.speed * dt

        # Vertical Movement
        self.rect.y += self.direction.y * self.speed * dt

    def action_picker(self):
        if self.action_indices[self.status] <= 2 or \
                self.action_indices[self.status] == 6:
            # random.choice
            self.status = choice(["idle", "move_left", "move_right",
                                  "sit"])
            if self.status == "move_left":
                self.direction.x = randint(-1, 0)
                self.direction.y = randint(-1, 1)
            elif self.status == "move_right":
                self.direction.x = randint(0, 1)
                self.direction.y = randint(-1, 1)
            else:
                self.direction.x = self.direction.y = 0

        elif 3 <= self.action_indices[self.status] <= 5:
            self.status = choice(["sit_idle", "sleep", "stand_up"])

    def move(self):
        player_pos = self.player_pos_func()
        if self.detection_area[0][0] < \
                player_pos[0] < self.detection_area[1][0] and \
                self.detection_area[0][1] < \
                player_pos[1] < self.detection_area[1][1] and \
                self.health > 0:
            self.pathing = True

            if player_pos[0] > self.rect.x:  # slime is to the left of player
                self.direction.x = 1
                self.status = "move_right"
            else:  # slime is the right of player
                self.direction.x = -1
                self.status = "move_left"

            if player_pos[1] > self.rect.y:  # slime is below the player
                self.direction.y = 1
            else:  # slime is the above the player
                self.direction.y = -1
        else:
            self.pathing = False

    def cow(self):
        """
        Added this function in order to see hitbox of cow
        :return: pygame rect which has the hitbox of the Cow
        """
        self.hitbox = self.rect.copy().inflate(self.rect.width * 0.2,
                                               self.rect.height * 0.75)
        return self.hitbox

    def update(self, dt):
        # self.player_dmg_timer.update()
        self.move()
        self.animate(dt)


