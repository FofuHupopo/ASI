import pygame

from typing import Sequence
from engine.objects import AnimatedSprite
from engine.core import EngineEvent, EventTypes, EngineSettings
from engine.objects.sprite import SpriteTypes

from asi import settings


class Grad(AnimatedSprite):
    def init(self, coords, speed):
        self.load_image("projectly/grad.png")

        self.scale_image((50, 50))
        self.rect.x = coords[0]
        self.rect.y = coords[1]
        self.speed = speed

        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.rect.y += self.speed
        if self.checking_touch_by_type(SpriteTypes.PLAYER):
            self.find_sprites(SpriteTypes.PLAYER)[0].change_health(-30 * self.find_sprites(SpriteTypes.PLAYER)[0].arms)
            
            if EngineSettings.get_var("PLAY_SOUNDS"):
                pygame.mixer.Channel(9).play(pygame.mixer.Sound("asi/main/resources/sound/arms_kill.mp3"))

            self.kill()

        if self.checking_touch_by_type(SpriteTypes.OBSTACLE):
            self.kill()

