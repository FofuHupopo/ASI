import pygame
import random

from typing import Sequence
from dataclasses import dataclass
from engine.objects import BaseSprite
from engine.core import EngineEvent, EventTypes
from engine.objects.sprite import SpriteTypes

from .obstacle import Obstacle


class Kamikaze(BaseSprite):
    def init(self, coords):
        self.set_type(SpriteTypes.ENEMY)
        self.load_image("enemy/kamikadze.jpg")
        self.scale_image((100, 100))

        self.main_coordsx = coords[0]
        self.main_coordsy = coords[1]

        self.rect.x = coords[0]
        self.rect.y = coords[1]

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.flag_zone = False
        self.zone_x1 = self.rect.x
        self.zone_x2 = self.rect.x
        self.zone_y = self.rect.y - 250

    def find_zone(self):
        self.flag_zone = True
        self.rect.y += 50
        for i in range(10):
            if self.checking_touch_by_type(SpriteTypes.OBSTACLE):
                self.zone_x1 -= 50
                self.rect.x -= 50

                self.rect.y -= 50
                for j in range(1, 6):
                    self.rect.y -= 50
                    if self.checking_touch_by_type(SpriteTypes.OBSTACLE):
                        self.zone_y = max(self.zone_y, self.rect.y + 50)
                        break
                self.rect.y = self.main_coordsy + 50
            else:
                self.rect.x = self.main_coordsx
                break
        for i in range(10):
            if self.checking_touch_by_type(SpriteTypes.OBSTACLE):
                self.zone_x2 += 50
                self.rect.x += 50

                self.rect.y -= 50
                for j in range(1, 6):
                    self.rect.y -= 50
                    if self.checking_touch_by_type(SpriteTypes.OBSTACLE):
                        self.zone_y = max(self.zone_y, self.rect.y + 50)
                        break
                self.rect.y = self.main_coordsy + 50
            else:
                break
        self.rect.y = self.main_coordsy
        self.rect.x = self.main_coordsx

    def update(self):
        if not self.flag_zone:
            self.find_zone()
