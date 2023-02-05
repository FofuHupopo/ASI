import pygame
import random

from typing import Sequence
from dataclasses import dataclass
from engine.objects import BaseSprite
from engine.core import EngineEvent, EventTypes
from engine.objects.sprite import SpriteTypes
from math import sqrt


class Projectlie(BaseSprite):
    def init(self, coords, coords_player):
        self.set_type(SpriteTypes.ENEMY)
        self.load_image("projectly/fire_ball.jpg")
        self.scale_image((50, 50))

        self.rect.x = coords[0]
        self.rect.y = coords[1]

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        if self.rect.x < coords_player:
            self.speed_x = 10
        else:
            self.speed_x = -10
            self.rect.x -= self.width
        self.time = 0

    def update(self):
        self.time += 1
        if self.time == 100:
            self.kill()
        self.rect.x += self.speed_x
        if self.checking_touch_by_type(SpriteTypes.PLAYER):
            self.find_sprites(SpriteTypes.PLAYER)[0].change_health(-25)
            self.kill()
        if self.checking_touch_by_type(SpriteTypes.OBSTACLE) or self.checking_touch_by_type(
                SpriteTypes.NPC) or self.checking_touch_by_type(SpriteTypes.STORAGE):
            self.kill()
