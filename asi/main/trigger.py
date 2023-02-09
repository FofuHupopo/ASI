import pygame
import random

from typing import Sequence

from engine.objects import BaseSprite
from engine.objects.sprite import SpriteTypes
from engine.core import EngineEvent, EventTypes
from .obstacle import Obstacle


class Trigger(Obstacle):
    def init(self, coords):
        super(Trigger, self).init(coords)
        self.flag = True
        self.set_type(SpriteTypes.TRIGGER)

    def update(self):
        if self.find_sprites(SpriteTypes.PLAYER)[0].rect.x >= self.rect.x and 0 <= self.rect.y - \
                self.find_sprites(SpriteTypes.PLAYER)[0].rect.y <= 120:
            if self.flag:
                self.flag = False
                for i in self.find_sprites(SpriteTypes.PLAYER)[0].list_door:
                    i.open()
                self.find_sprites(SpriteTypes.BOSS)[0].var = True

    def close_door(self):
        for i in self.find_sprites(SpriteTypes.PLAYER)[0].list_door:
            i.kill()
