import pygame
import random

from typing import Tuple

from engine.objects import BaseSprite, AnimatedSprite
from engine.objects.sprite import SpriteTypes


class DecorationSprite(BaseSprite):
    def init(self, coords: Tuple[int, int], image_path: str, size: Tuple[int, int]):
        self.load_image(image_path)
        self.set_type(SpriteTypes.DECORATION)

        self.scale_image(size)
        self.rect.x, self.rect.y = coords
