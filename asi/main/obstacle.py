import pygame
import random

from typing import Sequence

from engine.objects import BaseSprite
from engine.objects.sprite import SpriteTypes


class Obstacle(BaseSprite):
    def __init__(self, coords):
        self.load_image("obstacle/box.png")
        self.set_type(SpriteTypes.OBSTACLE)
        self.rect.x = coords[0]
        self.rect.y = coords[1]
