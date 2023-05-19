import pygame
from settings import LAYERS


class Slime(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, z, player_pos, detection_area):
        self.frames = frames
        self.frame_index = 0

        self.image = self.frames["idle"][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2,
                                               -self.rect.height * 0.75)

        super().__init__(groups)

        self.health = 5
        self.alive = True
        self.speed = 50
        self.direction = pygame.math.Vector2()
        self.player_pos_func = player_pos
        self.status = "idle"

        self.detection_area = detection_area

    def animate(self, dt):
        self.frame_index += 5 * dt
        if self.frame_index >= len(self.frames[self.status]):
            self.frame_index = 0

        self.image = self.frames[self.status][int(self.frame_index)]

        self.rect.x += self.direction.x * self.speed * dt
        # self.hitbox.centerx = round(self.pos.x)
        # self.rect.centerx = self.hitbox.centerx
        # self.collision('horizontal')

        # Vertical Movement
        self.rect.y += self.direction.y * self.speed * dt
        # self.hitbox.centery = round(self.pos.y)
        # self.rect.centery = self.hitbox.centery
        # self.collision('vertical')

    def move(self):

        player_pos = self.player_pos_func()
        if self.detection_area[0][0] < \
                player_pos[0] < self.detection_area[1][0] and \
                self.detection_area[0][1] < \
                player_pos[1] < self.detection_area[1][1]:
            self.status = "move"

            if player_pos[0] > self.rect.x:  # slime is to the left of player
                self.direction.x = 1
            else:                            # slime is the right of player
                self.direction.x = -1

            if player_pos[1] > self.rect.y:  # slime is below the player
                self.direction.y = 1
            else:                            # slime is the above the player
                self.direction.y = -1

        else:
            self.status = "idle"
            self.direction.x = 0
            self.direction.y = 0

    def update(self, dt):
        self.move()
        self.animate(dt)

