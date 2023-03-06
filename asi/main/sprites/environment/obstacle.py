import pygame
import random

from typing import Sequence

from engine.objects import BaseSprite
from engine.objects.sprite import SpriteTypes


class Obstacle(BaseSprite):
    def init(self, coords, image="map/platforms/platform.png"):
        # self.load_im(r"map\block2.png")
        self.load_image(image)
        # self.load_image(r"map\block2.png")

        self.set_type(SpriteTypes.OBSTACLE)
        self.rect.x = coords[0]
        self.rect.y = coords[1]
        self.width = self.image.get_width()
        self.height = self.image.get_height()
