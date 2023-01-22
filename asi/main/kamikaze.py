import pygame
import random

from typing import Sequence
from dataclasses import dataclass
from engine.objects import BaseSprite
from engine.core import EngineEvent, EventTypes
from engine.objects.sprite import SpriteTypes
from engine.objects.enemy import BaseEnemy

from .obstacle import Obstacle


class Kamikaze(BaseEnemy):
    def init(self, coords):
        self.load_image("enemy/kamikadze.jpg")
        self.scale_image((100, 100))

        self.main_coordsx = coords[0]
        self.main_coordsy = coords[1]
        self.relacetion_x = 0

        self.rect.x = coords[0]
        self.rect.y = coords[1]

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.flag_zone = False
        self.zone_x1 = self.rect.x
        self.zone_x2 = self.rect.x
        self.zone_y = self.rect.y - 250
        self.direction = 1

        self.attack_radius_x = 100
        self.attack_radius_x = 100

        self.speed = 3
        self.speed_agra = 5

    def attack(self):
        self.kill()


