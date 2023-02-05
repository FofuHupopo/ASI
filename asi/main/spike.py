import pygame
import random

from typing import Sequence

from engine.objects import BaseSprite
from engine.objects.sprite import SpriteTypes
from engine.core import EngineEvent, EventTypes


class Spike(BaseSprite):
    def init(self, coords):
        self.load_image("spike/spike.jpg")
        self.scale_image((50, 50))
        self.rect.x = coords[0]
        self.rect.y = coords[1]
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        if self.checking_touch_by_type(SpriteTypes.PLAYER):
            self.find_sprites(SpriteTypes.PLAYER)[0].dead()
