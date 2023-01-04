import pygame
import random

from engine.objects import BaseScene

from .player import PlayerObject


class MainScene(BaseScene):
    def init(self) -> None:
        # self.load_sprite(TreeSprite())
        self.load_sprite(PlayerObject)

    def update(self) -> None:
        pressed = pygame.key.get_pressed()