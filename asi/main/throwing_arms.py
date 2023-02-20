import pygame
import random

from typing import Sequence

from engine.objects import BaseSprite
from engine.objects.sprite import SpriteTypes
from engine.core import EngineSettings

from .obstacle import Obstacle
from .storage import Storage
from .trader import Trader

from asi import settings


class Arms(BaseSprite):
    def init(self, coords, direction):
        self.load_image("player/weapons/shuriken.png")
        self.set_type(SpriteTypes.THROWING_WEAPON)
        self.direction = direction
        self.width = 50
        self.height = 50
        self.scale_image((50, 50))
        if self.direction == -1:
            self.rect.x = coords[0] - self.image.get_width()
        else:
            self.rect.x = coords[0]
        self.rect.y = coords[1]
        self.time_fly = 0
        self.damadge = 100
        self.heat = False
        self.speed_y = 0.05
        self.time_fall = 0
        
        if EngineSettings.get_var("PLAY_SOUNDS"):
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("asi/main/resources/sound/arms_in_fly.mp3"))

    def contact_x(self):
        contact = self.checking_touch_by_type(SpriteTypes.OBSTACLE) + self.checking_touch_by_type(SpriteTypes.STORAGE) \
                  + self.checking_touch_by_type(SpriteTypes.NPC)
        if self.direction == 1:
            for i in contact:
                self.rect.x = min(self.rect.x, i.rect.x - self.width)
        else:
            for i in contact:
                self.rect.x = max(self.rect.x, i.rect.x + i.width)

    def contact_y(self):
        contact = self.checking_touch_by_type(SpriteTypes.OBSTACLE) + self.checking_touch_by_type(SpriteTypes.STORAGE) \
                  + self.checking_touch_by_type(SpriteTypes.NPC)
        for i in contact:
            self.rect.y = min(self.rect.y, i.rect.y - self.height)

    def update(self):
        self.time_fly += 1
        if self.heat:
            self.rect.y += self.time_fly * self.speed_y * 10
            if self.checking_touch_by_type(SpriteTypes.OBSTACLE) or self.checking_touch_by_type(SpriteTypes.STORAGE) \
                    or self.checking_touch_by_type(SpriteTypes.NPC):

                self.contact_y()
                self.time_fall += 1
                if self.time_fall == 20:
                    self.kill()
        else:
            self.rotate_image(20)
            
            self.rect.x += 10 * self.direction
            if self.checking_touch_by_type(SpriteTypes.OBSTACLE) or self.checking_touch_by_type(SpriteTypes.STORAGE) \
                    or self.checking_touch_by_type(SpriteTypes.NPC):
                if EngineSettings.get_var("PLAY_SOUNDS"):
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("asi/main/resources/sound/arms_in_floor.mp3"))
                self.contact_x()
                self.heat = True
                self.damadge = 0
                self.time_fly = 10
            elif self.time_fly > 25:
                self.rect.y += (self.time_fly - 25) * self.speed_y * 10
                self.damadge = max(0, self.damadge - 2)
                if self.checking_touch_by_type(SpriteTypes.OBSTACLE) or self.checking_touch_by_type(SpriteTypes.STORAGE) \
                        or self.checking_touch_by_type(SpriteTypes.NPC):
                    if EngineSettings.get_var("PLAY_SOUNDS"):
                        pygame.mixer.Channel(1).play(pygame.mixer.Sound("asi/main/resources/sound/arms_in_floor.mp3"))
                    self.contact_y()
                    self.heat = True
                    self.damadge = 0
                    self.time_fly = 10
            if self.time_fly == 40:
                self.damadge = 0
