import pygame
import random

from engine.objects import BaseScene

from .sprite_example import TreeSprite


class MainScene1(BaseScene):
    def init(self) -> None:
        # self.load_sprite(TreeSprite())
        self.load_sprite(TreeSprite)

    def update(self) -> None:
        if random.randint(0, 10000) == 10000:
            self.stop()
            print("сцена закончила свою работу")

        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_f]:
            self.pause("main2")


class MainScene2(BaseScene):
    def init(self) -> None:
        self.load_sprite(TreeSprite)
        self.load_sprite(TreeSprite)

    def update(self) -> None:
        if random.randint(0, 10000) == 10000:
            self.stop()
            print("сцена закончила свою работу")

        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_j]:
            self.pause("main1")
