import pygame
import random

from engine.objects import BaseSprite
from engine.core import EngineEvent, EventTypes
from engine.objects.sprite import SpriteTypes


class Heal(BaseSprite):
    def init(self, coords, view="big"):
        self.set_type(SpriteTypes.HEAL)
        self.view = view
        if self.view == "big":
            self.load_image("heal/big_heal.jfif")
        else:
            self.load_image("heal/little_heal.png")
        self.scale_image((50, 50))

        self.rect.x = coords[0]
        self.rect.y = coords[1]

        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.fly = True

    def update(self):
        if self.fly:
            self.rect.y += 5
            if self.checking_touch_by_type(SpriteTypes.OBSTACLE):
                for i in self.checking_touch_by_type(SpriteTypes.OBSTACLE):
                    self.rect.y = min(i.rect.y - self.height, self.rect.y)
                self.fly = False
        if self.checking_touch_by_type(SpriteTypes.PLAYER):
            if self.view == 'big':
                self.find_sprites(SpriteTypes.PLAYER)[0].count_big_heal += 1
            else:
                self.find_sprites(SpriteTypes.PLAYER)[0].count_heal += 1
            self.kill()
