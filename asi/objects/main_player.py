import pygame
import random

from typing import Sequence

from engine.objects import BaseSprite


class PlayerObject(BaseSprite):
    def init(self):
        self.load_image("player/creature.png")
        self.rect.x = 500
        self.rect.y = 250
        self.speed_x = 0
        self.speed_y = 0
        self.time_y = 0
        self.fly = False

    def update(self):
        self.rect.x -= self.speed_x
        if self.fly:
            self.rect.y -= self.speed_y
            self.speed_y -= self.time_y
            self.time_y += 10 * 0.0003

    def events_handler(self, event: pygame.event.Event):
        keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN and keys[pygame.K_SPACE] and not self.fly:
            self.speed_y = 5
            self.fly = True

    def key_pressed_handler(self, pressed: Sequence[bool]):
        if pressed[pygame.K_a]:
            self.speed_x = 3
        elif pressed[pygame.K_d]:
            self.speed_x = -3
        else:
            self.speed_x = 0
