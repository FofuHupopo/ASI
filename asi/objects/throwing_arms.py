import pygame
import random

from typing import Sequence

from engine.objects import BaseSprite


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
        self.rect.x += 6 * self.direction
        if self.time_fly > 50:
            self.rect.y += (self.time_fly - 50) * 0.02 * 10
            self.damadge = max(0, self.damadge - 2)
        if self.time_fly == 80:
            self.scale_image((10, 10))
            self.damadge = 0