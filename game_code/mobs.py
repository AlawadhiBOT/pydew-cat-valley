from  os import path
from typing import Callable

import pygame
from code.timer import Timer
from random import choice, randint, choices
from code.settings import CURR_PATH


class NeutralMob(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups: pygame.sprite.Group, z,
                 player_pos: Callable = None):
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
        self.axe_sound = pygame.mixer.Sound(path.join(CURR_PATH, 'audio',
                                                      'axe.mp3'))

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
        Added this function in order for it to be easier for the player to hit
        the slime.
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

    def __init__(self, pos, frames, groups: pygame.sprite.Group, z):
        super().__init__(pos, frames, groups, z)

        self.detection_area = ((self.rect.x - 250, self.rect.y - 250),
                               (self.rect.x + 250, self.rect.y + 250))

        self.speed = self.default_speed = 50
        self.target_path = pos
        # need to make attribute multiplier so that I can more accurately
        # calculate delta time for each action

        self.current_time = None
        self.important_positions = {
            "CowOrigin": pos, "CowInside": None,
            "CowAreaMarker": None,
        }
        self.routine_checklist = {
            "pathing_origin": True,
            "pathing_cow_inside": False,
            "pathing_cow_area": False,
            "pathing_inside_cow_area": False,
        }
        self.current_job = "pathing_origin"
        self.times_complete = 3
        self.collision_tiles = pygame.sprite.Group()

    def setup_time(self, curr_time: list[int, int]):
        """
        Sets the current time to the game time
        """
        self.current_time = curr_time

    def setup_important_positions(self, key: str, value):
        """
        Sets the position for an important place
        :param key: key in important positions dict
        :param value: location of that position
        """
        self.important_positions[key] = value

    def setup_cow_collision_tiles(self, collision_tiles):
        """
        Sets up valid locations for the cow target path to be in.
        :param collision_tiles: valid location tiles
        """
        self.collision_tiles = collision_tiles

    def collision_checker(self, position):
        """
        Checks if a certain position is colliding with another
        :param position:
        :return: bool indicating if there was a point of collision
        """
        for tile in self.collision_tiles.sprites():
            if tile.rect.collidepoint(position):
                return True

        return False

    def target_pathfind_morning(self):
        """
        Function to know where the cow is currently pathfinding to 
        (morning routine)
        """
        if self.routine_checklist["pathing_origin"]:
            self.current_job = "pathing_origin"
            return self.important_positions["CowOrigin"]

        if self.routine_checklist["pathing_cow_inside"]:
            self.current_job = "pathing_cow_inside"
            return self.important_positions["CowInside"]

        if self.routine_checklist["pathing_cow_area"]:
            self.current_job = "pathing_cow_area"
            return self.important_positions["CowAreaMarker"]

        if self.routine_checklist["pathing_inside_cow_area"]:
            target_pos = self.action_picker()
            return target_pos

    def target_pathfind_night(self):
        """
        Function to know where the cow is currently pathfinding to
        (night routine)
        """
        if self.routine_checklist["pathing_cow_area"]:
            self.current_job = "pathing_cow_area"
            return self.important_positions["CowAreaMarker"]

        if self.routine_checklist["pathing_cow_inside"]:
            self.current_job = "pathing_cow_inside"
            return self.important_positions["CowInside"]

        if self.routine_checklist["pathing_origin"]:
            self.current_job = "pathing_origin"
            return self.important_positions["CowOrigin"]

        else:
            self.current_job = "pathing_cow_area"
            return self.important_positions["CowAreaMarker"]

    def routine_action(self):
        """
        Function to know at what point the cow does what exactly, so the cow
        should:
        Path to the "inside" check point if the day just began.
        From 08 to 10, the cow should move around, and search for grass
        From 10 to 12, the cow should idle or munch grass
        From 12 to 15, the cow should be on the ground (sleeping/idling)
        From 15 to 18, the cow moves around, and if it searches, it should
        occasionally munch grass.
        From 17 to 18, the cow idles. (ignored currently)
        After 18, the cow paths to the barn and stays there.
        At 21, the cow sleeps.
        """
        if self.current_time[0] < 18:
            if not self.routine_checklist["pathing_inside_cow_area"]:
                # path to cow area.
                self.routine_checklist[self.current_job] = False
                if self.current_job == "pathing_origin":
                    self.current_job = "pathing_cow_inside"
                elif self.current_job == "pathing_cow_inside":
                    self.current_job = "pathing_cow_area"
                else:
                    self.current_job = "pathing_inside_cow_area"

                self.routine_checklist[self.current_job] = True
                self.target_path = self.target_pathfind_morning()
            else:
                self.target_path = self.target_pathfind_morning()
        else:
            if not self.routine_checklist["pathing_origin"]:
                self.routine_checklist[self.current_job] = False
                if self.current_job == "pathing_inside_cow_area":
                    self.current_job = "pathing_cow_area"
                elif self.current_job == "pathing_cow_area":
                    self.current_job = "pathing_cow_inside"
                else:
                    self.current_job = "pathing_origin"

                self.routine_checklist[self.current_job] = True
                self.target_path = self.target_pathfind_night()
            else:
                self.action_picker()

    def animate(self, dt: float):
        """
        Animates the cow
        :param dt: delta time
        """
        self.frame_index += 0.75 * len(self.frames[self.status]) * dt
        if self.frame_index >= len(self.frames[self.status]):
            self.frame_index = 0
            self.times_complete += 1
            if (self.routine_checklist["pathing_inside_cow_area"] or
                self.routine_checklist["pathing_origin"]) \
                    and "move" not in self.status:
                self.action_picker()

        self.image = self.frames[self.status][int(self.frame_index)]

        # Horizontal
        self.rect.x += self.direction.x * self.speed * dt

        # Vertical Movement
        self.rect.y += self.direction.y * self.speed * dt

    def action_picker(self):
        """
        Picks the next action for the cow to perform
        """
        if self.times_complete < 3:
            self.times_complete += 1
            return self.target_path
        else:
            if self.current_time[0] < 10:  # earlier than 10
                if self.status != "grass_find":
                    self.status = choices(["move_left", "move_right",
                                           "grass_find"],
                                          [10, 10, 5])[0]
                else:
                    self.status = choices(["move_left", "move_right",
                                           "grass_find"],
                                          [10, 10, 1])[0]

                if "move" in self.status:
                    num = ((randint(-500, 500) + self.rect.centerx,
                            randint(-500, 500) + self.rect.centery))
                    while not self.collision_checker(num):
                        num = ((randint(-500, 500) + self.rect.centerx,
                                randint(-500, 500) + self.rect.centery))
                    return num

            elif self.current_time[0] < 12:  # earlier than 12
                self.status = choice(["idle", "munch"])
            elif self.current_time[0] < 15:  # earlier than 15
                if self.status not in ["sit_idle", "sleep", "sit"]:
                    self.status = "sit"
                else:
                    self.status = choice(["sit_idle", "sleep"])

            elif self.current_time[0] < 18:
                if self.status in ["sit_idle", "sleep", "sit"]:
                    self.status = "stand_up"
                elif self.status == "grass_find":
                    self.status = choices(["move_left", "move_right",
                                           "grass_find", "munch"],
                                          [9, 9, 2, 1])[0]
                else:  # cow finished munching
                    self.status = choices(["move_left", "move_right",
                                           "grass_find"],
                                          [1, 3, 1])[0]

                if "move" in self.status:
                    num = ((randint(-125, 125) + self.rect.centerx,
                            randint(-125, 125) + self.rect.centery))
                    while not self.collision_checker(num):
                        num = ((randint(-125, 125) + self.rect.centerx,
                                randint(-125, 125) + self.rect.centery))
                    return num

            elif self.current_time[0] >= 18:
                if self.status not in ["sit", "sleep"]:
                    self.status = "sit"
                else:
                    self.status = "sleep"
            return self.target_path

    def move(self):
        """
        When the player approaches the cow, the cow begins pathing towards the
        player
        """
        x = self.rect.centerx
        y = self.rect.centery
        margin = 30
        if x - margin < self.target_path[0] < x + margin \
                and y - margin < self.target_path[1] < y + margin and \
                "move" in self.status:
            self.routine_action()

        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        if x - margin < self.target_path[0] < x + margin:
            # cow inside margin of "error"
            self.direction.x = 0
        elif self.target_path[0] > x:
            # cow is to the left of target
            self.direction.x = 1
            self.status = "move_right"
        elif self.target_path[0] < x:
            # cow is to the right of target
            self.direction.x = -1
            self.status = "move_left"

        if y - margin < self.target_path[1] < y + margin:
            # cow inside margin of "error"
            self.direction.y = 0
        if self.target_path[1] > self.rect.centery:
            # cow is below the target
            self.direction.y = 1
        else:  # cow is above the target
            self.direction.y = -1

        if "move" not in self.status:
            self.direction.x = 0
            self.direction.y = 0

    def cow(self):
        """
        Added this function in order to see hitbox of cow
        :return: pygame rect which has the hitbox of the Cow
        """
        self.hitbox = self.rect.copy().inflate(self.rect.width * 0.2,
                                               self.rect.height * 0.75)
        return self.hitbox

    def update(self, dt: float):
        """
        Update method, which happens every frame
        :param dt: delta time
        """
        # self.player_dmg_timer.update()
        self.move()
        self.animate(dt)
