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

    def update(self):
        self.rect.x += self.speed_x

