import pygame
import random

from typing import Sequence

from engine.objects import BaseSprite, AnimatedSprite
from engine.objects.sprite import SpriteTypes


class Trader(AnimatedSprite):
    def init(self, coords):
        # self.load_image()
        self.register_animations(
            "npc/trader.png",
            {
                "test": [
                    "npc/trader.png",
                    "npc/profile_icon.png",
                    "npc/asprite.bmp"
                ]
            }
        )
        self.scale_image((80, 100))
        self.set_type(SpriteTypes.TREADER)
        self.coords = coords
        self.rect.x = coords[0]
        self.rect.y = coords[1]
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        self.__triger_zone = 200

    def events_handler(self, event: pygame.event.Event):
        pressed = pygame.key.get_pressed()
        
        if event.type == pygame.KEYDOWN and pressed[pygame.K_g]:
            self.start_animation("test")
            
        if event.type == pygame.KEYDOWN and pressed[pygame.K_f]:
            self.stop_animation()
    
    def update(self) -> None:
        self.create_dialog("Dialog", (200, 200))

    def buy(self):
        pass
