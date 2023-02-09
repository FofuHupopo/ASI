import pygame
import random

from typing import Sequence
from dataclasses import dataclass
from engine.objects import BaseSprite
from engine.core import EngineEvent, EventTypes
from engine.objects.sprite import SpriteTypes
from .projectile_enemy import Projectlie


class Boss(BaseSprite):
    def init(self, coords):
        self.set_type(SpriteTypes.BOSS)
        self.load_image("boss/boss.jpg")
        self.scale_image((100, 100))
        self.rect.x = coords[0]
        self.rect.y = coords[1]

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.health = 1000
        self.var = False
        self.direction = 1
        self.time_attack = 55
        self.time = 0

    def attack(self):
        if self.find_sprites(SpriteTypes.PLAYER)[0].rect.x > self.rect.x:
            self.load_sprite(Projectlie, coords=(self.rect.x + self.width, self.rect.y),
                             coords_player=self.find_sprites(SpriteTypes.PLAYER)[0].rect.x, damadge=25, speed=10,
                             view="fire_ball")
        else:
            self.load_sprite(Projectlie, coords=self.rect,
                             coords_player=self.find_sprites(SpriteTypes.PLAYER)[0].rect.x, damadge=25, speed=10,
                             view="fire_ball")

    def big_attack(self):
        if self.find_sprites(SpriteTypes.PLAYER)[0].rect.x > self.rect.x:
            self.load_sprite(Projectlie, coords=(self.rect.x + self.width, self.rect.y),
                             coords_player=self.find_sprites(SpriteTypes.PLAYER)[0].rect.x, damadge=50, speed=8,
                             view="ice_ball")
        else:
            self.load_sprite(Projectlie, coords=self.rect,
                             coords_player=self.find_sprites(SpriteTypes.PLAYER)[0].rect.x, damadge=50, speed=8,
                             view="ice_ball")

    def dead(self):
        self.find_sprites(SpriteTypes.PLAYER)[0].list_trigger[0].close_door()
        self.kill()

    def update(self):
        if self.checking_touch_by_type(SpriteTypes.THROWING_WEAPON):
            self.health -= self.checking_touch_by_type(SpriteTypes.THROWING_WEAPON)[0].damadge
            self.checking_touch_by_type(SpriteTypes.THROWING_WEAPON)[0].kill()
        if self.health == 0:
            self.dead()
        self.time = min(self.time + 1, self.time_attack)
        if self.var:
            if self.time_attack == self.time:
                if self.health > 750:
                    self.attack()
                    self.time = 0
                elif self.health > 500:
                    if random.randint(1, 10) < 4:
                        self.big_attack()
                        self.time = 0
                    else:
                        self.attack()
                        self.time = 0
