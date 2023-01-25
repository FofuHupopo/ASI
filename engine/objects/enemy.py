import pygame
import random

from typing import Sequence
from dataclasses import dataclass
from engine.objects import BaseSprite
from engine.core import EngineEvent, EventTypes
from engine.objects.sprite import SpriteTypes


class BaseEnemy(BaseSprite):
    def init(self):
        self.set_type(SpriteTypes.ENEMY)

    def find_zone(self):
        self.flag_zone = True
        self.rect.y += 50
        for i in range(10):
            if self.checking_touch_by_type(SpriteTypes.OBSTACLE):
                self.rect.y -= 50
                if self.checking_touch_by_type(SpriteTypes.OBSTACLE):
                    self.rect.y += 50
                    self.zone_x1 += 50
                    self.rect.x = self.main_coordsx
                    break
                self.rect.y -= 50
                self.zone_x1 -= 50
                self.rect.x -= 50

                self.rect.y -= 50
                for j in range(1, 6):
                    self.rect.y -= 50
                    if self.checking_touch_by_type(SpriteTypes.OBSTACLE):
                        self.zone_y = max(self.zone_y, self.rect.y + 50)
                        break
                self.rect.y = self.main_coordsy + 50
            else:
                self.rect.x = self.main_coordsx
                break
        for i in range(10):
            if self.checking_touch_by_type(SpriteTypes.OBSTACLE):
                self.rect.y -= 50
                if self.checking_touch_by_type(SpriteTypes.OBSTACLE):
                    self.zone_x2 -= 50
                    break
                self.rect.y -= 50
                self.zone_x2 += 50
                self.rect.x += 50

                self.rect.y -= 50
                for j in range(1, 6):
                    self.rect.y -= 50
                    if self.checking_touch_by_type(SpriteTypes.OBSTACLE):
                        self.zone_y = max(self.zone_y, self.rect.y + 50)
                        break
                self.rect.y = self.main_coordsy + 50
            else:
                break
        self.rect.y = self.main_coordsy
        self.rect.x = self.main_coordsx
        self.zone_x1 = self.zone_x1 - self.rect.x
        self.zone_x2 = self.zone_x2 - self.rect.x
        self.zone_y = self.rect.y - self.zone_y

    def update(self):
        self.coords_player = self.find_sprites(SpriteTypes.PLAYER)[0].rect
        self.time = min(self.time + 1, self.time_attack)
        if not self.flag_zone:
            self.find_zone()
        elif self.coords_player.x >= self.zone_x1 + self.rect.x - self.relacetion_x and \
                self.coords_player.x <= self.zone_x2 + self.rect.x - self.relacetion_x \
                and self.coords_player.y >= - self.zone_y + self.rect.y and self.coords_player.y <= self.rect.y:
            if abs(self.coords_player.x - self.rect.x) < self.attack_radius_x and \
                    abs(self.coords_player.y - self.rect.y < self.attack_radius_y):
                if self.time_attack == self.time:
                    self.time = 0
                    self.attack()

            elif self.coords_player.x > self.rect.x:
                self.rect.x += self.speed_agra
                self.relacetion_x += self.speed_agra
                self.direction = 1
            else:
                self.rect.x -= self.speed_agra
                self.relacetion_x -= self.speed_agra
                self.direction = -1
        elif self.direction == 1:
            if self.relacetion_x < self.zone_x2 - self.width:
                self.rect.x += self.speed
                self.relacetion_x += self.speed
            else:
                self.direction = -1
        else:
            if self.relacetion_x > self.zone_x1 + self.width:
                self.rect.x -= self.speed
                self.relacetion_x -= self.speed
            else:
                self.direction = 1
