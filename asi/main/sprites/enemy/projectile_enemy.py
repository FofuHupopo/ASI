import pygame
import random

from typing import Sequence
from dataclasses import dataclass
from engine.objects import AnimatedSprite
from engine.core import EngineEvent, EventTypes, EngineSettings
from engine.objects.sprite import SpriteTypes
from math import sqrt

from asi import settings


class Projectlie(AnimatedSprite):
    def init(self, coords, coords_player, damadge, speed, view):
        if view == "fire_ball":
            self.load_image("enemy/gunner/bullet/bullet.png")
            self.scale_image((40, 20))
        elif view == "arms":
            self.load_image("projectly/arm_projectile.png")
            self.scale_image((50, 50))
        else:
            if EngineSettings.get_var("PLAY_SOUNDS"):
                pygame.mixer.Channel(13).play(pygame.mixer.Sound("asi/main/resources/sound/pusk_lazer.mp3"))
            self.load_image("projectly/ice_ball.png")
            self.scale_image((50, 50))
        self.damadge = damadge

        self.rect.x = coords[0]
        self.rect.y = coords[1]

        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.view = view

        if self.rect.x < coords_player:
            self.speed_x = speed
        else:
            self.speed_x = -speed
            self.rect.x -= self.width
        self.time = 0

    def update(self):
        self.time += 1
        if self.time == 100:
            self.kill()
        self.rect.x += self.speed_x
        if self.checking_touch_by_type(SpriteTypes.PLAYER):
            self.find_sprites(SpriteTypes.PLAYER)[0].change_health(
                -self.damadge * self.find_sprites(SpriteTypes.PLAYER)[0].arms)
            if EngineSettings.get_var("PLAY_SOUNDS") and self.view == "arms":
                pygame.mixer.Channel(13).play(pygame.mixer.Sound("asi/main/resources/sound/arms_kill.mp3"))
            self.kill()
        if self.checking_touch_by_type(SpriteTypes.OBSTACLE) or self.checking_touch_by_type(
                SpriteTypes.NPC) or self.checking_touch_by_type(SpriteTypes.STORAGE):
            self.kill()
