import pygame
import random

from typing import Sequence

from engine.objects import BaseSprite
from engine.objects.sprite import SpriteTypes


class Arms(BaseSprite):
    def init(self, coords, direction):
        self.load_image("player/shuriken.png")
        self.direction = direction
        self.scale_image((50, 50))
        if self.direction == -1:
            self.rect.x = coords[0] - self.image.get_width()
        else:
            self.rect.x = coords[0]
        self.rect.y = coords[1]
        self.time_fly = 0
        self.damadge = 100

    def update(self):
        self.time_fly += 1
        self.rect.x += 10 * self.direction
        if self.time_fly > 25:
            self.rect.y += (self.time_fly - 25) * 0.05 * 10
            self.damadge = max(0, self.damadge - 2)
        if self.time_fly == 40:
            self.scale_image((10, 10))
            self.damadge = 0
