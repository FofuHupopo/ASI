import pygame

from typing import Sequence

from engine.objects import BaseSprite


class LoaderSprite(BaseSprite):
    def init(self, **kwargs):
        self.load_image("loader/loader.png")
        self.scale_image((100, 100), False, coords=(400, 400))

    def update(self):
        self.rotate_image(-1)

    def events_handler(self, event: pygame.event.Event):
        ...

    def key_pressed_handler(self, pressed: Sequence[bool]):
        ...
