import pygame
import random

from typing import Sequence

from engine.objects import BaseSprite
from engine.objects.sprite import SpriteTypes


class Storage(BaseSprite):
    def init(self, coords):
        self.load_image("storage/close_chect.jpg")
        self.scale_image((100, 100))
        self.set_type(SpriteTypes.STORAGE)

        self.coords = coords
        self.rect.x = coords[0]
        self.rect.y = coords[1]
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.flag = False
        
        self.__storage = []

    def open(self):
        if not self.flag:
            self.flag = True
            old_coords = (self.rect.x, self.rect.y)

            self.load_image("storage/open_chest.jpg")
            self.scale_image((100, 100))

            self.rect.x, self.rect.y = old_coords

            
    def update(self) -> None:
        if self.checking_touch_by_type(SpriteTypes.PLAYER):
            pressed = pygame.key.get_pressed()
            print(self.__storage)
