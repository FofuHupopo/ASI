import pygame
import random

from typing import Sequence

from engine.objects import BaseSprite
from engine.objects.sprite import SpriteTypes
from engine.core import EngineEvent, EventTypes
from .platforms.platform_vertically import PlatformVertically
from .obstacle import Obstacle


class Door(PlatformVertically):
    def init(self, coords):
        super(Door, self).init(coords)
        self.rect.x = -1e9
        self.rect.y = -1e9
        self.set_type(SpriteTypes.DOOR)
        self.main_coords = coords

    def open(self):
        self.set_type(SpriteTypes.OBSTACLE, )
        self.rect.x = self.main_coords[0] - (-self.rect.x - 1e9)
        self.rect.y = self.main_coords[1] - (-self.rect.y - 1e9)
        
        self._BaseSprite__scene.set_auto_save(False)
