import pygame
from timer import Timer


class Slime(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, z, player_pos, detection_area,
                 reduce_player_hp):
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
        self.default_speed = self.speed = 50

        self.direction = pygame.math.Vector2()
        self.player_pos_func = player_pos
        self.status = "idle"

        self.detection_area = detection_area
        self.reduce_player_hp = reduce_player_hp
        self.player_dmg_timer = Timer(1000)
        self.animation_lock = False

        # sounds
        self.axe_sound = pygame.mixer.Sound('../audio/axe.mp3')

    def animate(self, dt):
        self.frame_index += 5 * dt
        if self.frame_index >= len(self.frames[self.status]):
            if self.health <= 0:
                return None
            self.frame_index = 0
            self.animation_lock = False

        self.image = self.frames[self.status][int(self.frame_index)]

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

    def update(self, dt):
        self.player_dmg_timer.update()
        self.move()
        self.animate(dt)
