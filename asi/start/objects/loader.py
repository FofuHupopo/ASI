import pygame

from typing import Sequence

from engine.objects import BaseSprite


class LoaderSprite(BaseSprite):
    def init(self, coords):
        self.load_image("loader/loader.png")
        self.scale_image((100, 100))

        self.__coords = coords
        self.rect.x, self.rect.y = self.__coords[0] - 150, self.__coords[1] - 150

    def update(self):
        self.rotate_image(-1)
        self.rect.x, self.rect.y = self.__coords[0] - 150, self.__coords[1] - 150
        # self.rect.center = (self.rect.x + 50, self.rect.y + 50)

    def events_handler(self, event: pygame.event.Event):
        ...

    def key_pressed_handler(self, pressed: Sequence[bool]):
        ...
