import pygame
import random

from typing import Sequence
from dataclasses import dataclass
from engine.objects import BaseSprite
from engine.core import EngineEvent, EventTypes
from engine.objects.sprite import SpriteTypes
from .enemy import BaseEnemy
from .projectile_enemy import Projectlie


class Gunner(BaseEnemy):
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

        self.chance_heal = 2
        self.health = 250
        self.max_prize = 4

        self.attack_radius_x = 400
        self.attack_radius_y = 400

        self.speed = 3
        self.speed_agra = 4
        self.time_attack = 50
        self.time = 0

    def attack(self):
        if self.find_sprites(SpriteTypes.PLAYER)[0].rect.x > self.rect.x:
            self.load_sprite(Projectlie, coords=(self.rect.x + self.width, self.rect.y),
                             coords_player=self.find_sprites(SpriteTypes.PLAYER)[
                                 0].rect.x, damadge=25, speed=10, view="fire_ball")
        else:
            self.load_sprite(Projectlie, coords=self.rect,
                             coords_player=self.find_sprites(SpriteTypes.PLAYER)[0].rect.x, damadge=25, speed=10,
                             view="fire_ball")
