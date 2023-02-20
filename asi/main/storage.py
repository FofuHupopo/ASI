import pygame
import random

from typing import Sequence

from engine.objects import BaseSprite
from engine.objects.sprite import SpriteTypes
from engine.core import EngineEvent, EngineSettings
from asi.main.money import Money

from asi import settings


class Storage(BaseSprite):
    def init(self, coords):
        self.load_image("storage/chest-1.png")
        self.scale_image((50, 50))
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

            for i in range(random.randint(3, 6)):
                t = self.load_sprite(Money, coords=(random.randint(self.rect.x - 100, self.rect.x - 25),
                                                    random.randint(self.rect.y, self.rect.y + self.height - 25)))
                t = self.load_sprite(Money,
                                     coords=(random.randint(self.rect.x + self.width, self.rect.x + self.width + 75),
                                             random.randint(self.rect.y, self.rect.y + self.height - 25)))
            
            if EngineSettings.get_var("PLAY_SOUNDS"):
                pygame.mixer.Channel(5).play(pygame.mixer.Sound("asi/main/resources/sound/open_storage.mp3"))
            self.kill()

    def update(self) -> None:
        if self.checking_touch_by_type(SpriteTypes.PLAYER):
            pressed = pygame.key.get_pressed()
            print(self.__storage)
