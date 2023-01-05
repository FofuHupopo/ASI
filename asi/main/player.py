import pygame
import random

from typing import Sequence

from engine.objects import BaseSprite
from .throwing_arms import Arms
from .obstacle import Obstacle
from engine.objects.sprite import SpriteTypes


class PlayerObject(BaseSprite):
    def init(self):
        self.load_image("player/creature.png")
        self.set_type(SpriteTypes.PLAYER)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.load_sprite(Obstacle, coords=[600, 300])
        self.load_sprite(Obstacle, coords=[500, 50])
        self.load_sprite(Obstacle, coords=[275, 260])
        self.load_sprite(Obstacle, coords=[275, 260])
        self.load_sprite(Obstacle, coords=[500, 340])
        self.load_sprite(Obstacle, coords=[450, 340])
        self.rect.x = 500
        self.rect.y = 220
        self.speed_y = 0
        self.time_y = 0
        self.direction = 1
        self.health = 100

    def is_fly(self):
        self.rect.y += 1
        if self.checking_touch_by_type(SpriteTypes.OBSTACLE):
            self.rect.y -= 1
            return False
        else:
            self.rect.y -= 1
            return True

    def update(self):
        self.rect.x += self.speed_x
        if self.direction == 1:
            for i in self.checking_touch_by_type(SpriteTypes.OBSTACLE):
                self.rect.x = min(self.rect.x, i.rect.x - self.width)
        else:
            for i in self.checking_touch_by_type(SpriteTypes.OBSTACLE):
                self.rect.x = max(self.rect.x, i.rect.x + i.width)
        if self.is_fly() or self.speed_y != 0:
            if self.speed_y == 0:
                self.time_y = 0.5
            self.rect.y -= self.speed_y
            if self.checking_touch_by_type(SpriteTypes.OBSTACLE):
                if self.speed_y > 0:
                    for i in self.checking_touch_by_type(SpriteTypes.OBSTACLE):
                        self.rect.y = max(self.rect.y, i.rect.y + i.height)
                    self.time_y = 0.5

                else:
                    for i in self.checking_touch_by_type(SpriteTypes.OBSTACLE):
                        self.rect.y = min(self.rect.y, i.rect.y - self.height)
                    self.time_y = 0
                    self.health -= max(0, (-25 - self.speed_y) * 4)
                    print(self.health)
                self.speed_y = 0
            else:
                self.speed_y -= self.time_y
                self.time_y += 10 * 0.002

    def events_handler(self, event: pygame.event.Event):
        keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN and keys[pygame.K_SPACE]:
            if not self.is_fly():
                self.speed_y = 10

        if event.type == pygame.KEYDOWN and keys[pygame.K_r]:
            self.load_sprite(Arms, coords=[self.rect.x + max(0, self.width * self.direction), self.rect.y],
                             direction=self.direction)

    def key_pressed_handler(self, pressed: Sequence[bool]):
        if pressed[pygame.K_a]:
            self.direction = -1
            self.speed_x = 5 * self.direction
        elif pressed[pygame.K_d]:
            self.direction = 1
            self.speed_x = 5 * self.direction
        else:
            self.speed_x = 0
