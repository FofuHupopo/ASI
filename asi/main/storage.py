import pygame
import random

from typing import Sequence

from engine.objects import BaseSprite
from engine.objects.sprite import SpriteTypes


class Storage(BaseSprite):
    def init(self, coords):
        self.load_image("storage/close_chect.jpg")
        self.set_type(SpriteTypes.STORAGE)
        self.coords = coords
        self.rect.x = coords[0]
        self.rect.y = coords[1]
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.flag = False


    def open(self):
        if not self.flag:
            self.flag = True
            self.load_image("storage/open_chest.jpg")
            self.rect.x = self.coords[0]
            self.rect.y = self.coords[1]