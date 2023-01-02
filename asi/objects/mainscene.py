import pygame
import random

from engine.objects import BaseScene

from .tree import TreeSprite
from .main_player import PlayerObject


class MainScene(BaseScene):
    def init(self) -> None:
        # self.load_sprite(TreeSprite())
        self.load_sprite(PlayerObject)
        self.load_sprite(TreeSprite)

    def update(self) -> None:
        if random.randint(0, 10000) == 10000:
            self.stop()
            print("сцена закончила свою работу")

        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_f]:
            self.stop()
