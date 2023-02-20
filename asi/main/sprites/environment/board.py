import pygame
import random

from typing import Sequence

from engine.objects import BaseSprite
from engine.shortcuts.dialog import StartDialogObject
from engine.objects.sprite import SpriteTypes


class BoardSprite(BaseSprite):
    def init(self, coords, text="Какой-то текст"):
        self.load_image("map/board.png")
        self.set_type(SpriteTypes.BOARD)
        self.scale_image((100, 100))
        
        self.rect.x, self.rect.y = coords
        self.__text = text
    
    def update(self) -> None:
        self.create_dialog(self.__text, (400, 200))
