import pygame
import random

from engine.objects import BaseSprite
from engine.core import EngineEvent, EventTypes
from engine.objects.sprite import SpriteTypes

class Heal(BaseSprite):
    def init(self, coords, view = "big"):
        if view == "big":
            self.load_image("heal/big_heal.jfif")
        else:
            self.load_image("heal/little_heal.png")
        self.scale_image((50, 50))

        self.rect.x = coords[0]
        self.rect.y = coords[1]

