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
        self.weidht = self.image.get_width()
        self.load_sprite(Obstacle, coords = [250, 250])
        self.rect.x = 500
        self.rect.y = 250
        self.speed_y = 0
        self.time_y = 0
        self.direction = 1

    def update(self):
        self.rect.x += self.speed_x
        if self.speed_y:
            self.rect.y -= self.speed_y
            self.speed_y -= self.time_y
            self.time_y += 10 * 0.001

    def events_handler(self, event: pygame.event.Event):
        keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN and keys[pygame.K_SPACE]:
            self.speed_y = 7
        if event.type == pygame.KEYDOWN and keys[pygame.K_r]:
            self.load_sprite(Arms, coords=[self.rect.x + max(0, self.weidht * self.direction), self.rect.y],
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
