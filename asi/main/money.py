import pygame
import random

from engine.objects import BaseSprite
from engine.objects.sprite import SpriteTypes
from engine.core import EngineEvent, EventTypes


class Money(BaseSprite):
    def init(self, coords):
        self.load_image("money/money.png")
        self.scale_image((25, 25))
        self.rect.x = coords[0]
        self.rect.y = coords[1]

        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.fly = True

    def update(self):
        if self.fly:
            self.rect.y += 3
            if self.checking_touch_by_type(SpriteTypes.OBSTACLE):
                for i in self.checking_touch_by_type(SpriteTypes.OBSTACLE):
                    self.rect.y = min(i.rect.y - self.height, self.rect.y)
                self.fly = False
        if self.checking_touch_by_type(SpriteTypes.PLAYER):
            self.find_sprites(SpriteTypes.PLAYER)[0].money += 1
            self.kill()


