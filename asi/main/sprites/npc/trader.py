import pygame
import random

from typing import Sequence

from engine.objects import BaseSprite, AnimatedSprite
from engine.objects.sprite import SpriteTypes
from engine.core import EngineEvent


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
            print('YES')

        if self.checking_touch_by_type(SpriteTypes.PLAYER) and event.type == pygame.KEYDOWN and pressed[pygame.K_5] and\
                self.find_sprites(SpriteTypes.PLAYER)[0].money >= 10:
            self.find_sprites(SpriteTypes.PLAYER)[0].money -= 10
            self.find_sprites(SpriteTypes.PLAYER)[0].count_heal += 1
        if self.checking_touch_by_type(SpriteTypes.PLAYER) and event.type == pygame.KEYDOWN and pressed[pygame.K_6] and\
                self.find_sprites(SpriteTypes.PLAYER)[0].money >= 18:
            self.find_sprites(SpriteTypes.PLAYER)[0].money -= 18
            self.find_sprites(SpriteTypes.PLAYER)[0].count_big_heal += 1
        if self.checking_touch_by_type(SpriteTypes.PLAYER) and event.type == pygame.KEYDOWN and pressed[pygame.K_t] and\
            self.find_sprites(SpriteTypes.PLAYER)[0].money >= 12 and self.find_sprites(SpriteTypes.PLAYER)[0].arms >= 1:
            self.find_sprites(SpriteTypes.PLAYER)[0].money -= 12
            self.find_sprites(SpriteTypes.PLAYER)[0].arms = 0.9
            self.add_event(EngineEvent(
                "info", "arms_count", {"value": 1}
            ))
        if self.checking_touch_by_type(SpriteTypes.PLAYER) and event.type == pygame.KEYDOWN and pressed[pygame.K_y] and \
            self.find_sprites(SpriteTypes.PLAYER)[0].money >= 15 and self.find_sprites(SpriteTypes.PLAYER)[0].arms >= 0.9:
            self.find_sprites(SpriteTypes.PLAYER)[0].money -= 15
            self.find_sprites(SpriteTypes.PLAYER)[0].arms = 0.8
            self.add_event(EngineEvent(
                "info", "arms_count", {"value": 2}
            ))
        if self.checking_touch_by_type(SpriteTypes.PLAYER) and event.type == pygame.KEYDOWN and pressed[pygame.K_u] and \
            self.find_sprites(SpriteTypes.PLAYER)[0].money >= 12 and self.find_sprites(SpriteTypes.PLAYER)[0].arms >= 0.8:
            self.find_sprites(SpriteTypes.PLAYER)[0].money -= 20
            self.find_sprites(SpriteTypes.PLAYER)[0].arms = 0.7
            self.add_event(EngineEvent(
                "info", "arms_count", {"value": 3}
            ))
        if self.checking_touch_by_type(SpriteTypes.PLAYER) and event.type == pygame.KEYDOWN and pressed[pygame.K_i] and \
            self.find_sprites(SpriteTypes.PLAYER)[0].money >= 25 and self.find_sprites(SpriteTypes.PLAYER)[0].arms >= 0.7:
            self.find_sprites(SpriteTypes.PLAYER)[0].money -= 25
            self.find_sprites(SpriteTypes.PLAYER)[0].arms = 0.6
            self.add_event(EngineEvent(
                "info", "arms_count", {"value": 4}
            ))
        if self.checking_touch_by_type(SpriteTypes.PLAYER) and event.type == pygame.KEYDOWN and pressed[pygame.K_o] and \
                self.find_sprites(SpriteTypes.PLAYER)[0].money >= 30 and self.find_sprites(SpriteTypes.PLAYER)[0].arms >= 0.6:
            self.find_sprites(SpriteTypes.PLAYER)[0].money -= 30
            self.find_sprites(SpriteTypes.PLAYER)[0].arms = 0.5
            self.add_event(EngineEvent(
                "info", "arms_count", {"value": 5}
            ))

    def update(self) -> None:
        print(self)
        self.create_dialog(
            "Привет странник, ты можешь купить у меня всё,\nчто тебе надо:\n"
            "маленькое сердце жизни: 10 монет (нажмите'5')\nбольшое сердце жизни: 18 монет (нажмите'6')\n"
            "1) лёгкая броня: 12 монет(нажите't')\n2) броня разведчика: 15 монет(нажите'y')\n"
            "3) броня рыцаря: 20 монет(нажите'u')\n4) тяжёлая броня: 25 монет(нажите'i')\n"
            "5) метеоритная броня: 30 монет(нажите'o')", (400, 280))

    def buy(self):
        pass
