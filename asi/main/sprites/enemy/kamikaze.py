import pygame
import random

from typing import Sequence
from dataclasses import dataclass
from engine.objects import BaseSprite
from engine.core import EngineEvent, EventTypes, EngineSettings
from engine.objects.sprite import SpriteTypes
from .enemy import BaseEnemy

from ..environment.obstacle import Obstacle


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

        self.chance_heal = 5
        self.health = 200
        self.max_prize = 6

        self.attack_radius_x = 100
        self.attack_radius_y = 100

        self.speed = 3
        self.speed_agra = 7
        self.time = 0
        self.time_attack = 0
        
        super().init()

    def attack(self):
        self.find_sprites(SpriteTypes.PLAYER)[0].change_health(-50 * self.find_sprites(SpriteTypes.PLAYER)[0].arms)
        
        if EngineSettings.get_var("PLAY_SOUNDS"):
            pygame.mixer.Channel(9).play(pygame.mixer.Sound("asi/main/resources/sound/bomb.mp3"))

        self.kill()
