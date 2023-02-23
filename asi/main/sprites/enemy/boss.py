import pygame
import random

from typing import Sequence
from dataclasses import dataclass

from engine.objects import BaseSprite
from engine.core import EngineSettings
from engine.objects.sprite import SpriteTypes

from .projectile_enemy import Projectlie
from .grad import Grad
from ..player.HEAL import Heal
from ..player.money import Money


class Boss(BaseSprite):
    def init(self, coords):
        self.set_type(SpriteTypes.BOSS)
        self.load_image("boss/boss.png")
        self.scale_image((150, 150))
        self.rect.x = coords[0] - 50
        self.rect.y = coords[1] - 50

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

    def bombard(self):
        x = self.rect.x - 50 * 15
        for i in range(7):
            self.load_sprite(Grad, coords=(x + i * 4 * 50 + random.randint(0, 3) * 50, self.rect.y - 50 * 7),
                             speed=random.randint(8, 13))

    def dead(self):
        self.find_sprites(SpriteTypes.PLAYER)[0].list_trigger[0].close_door()
        self.load_sprite(Heal, coords=(random.randint(self.rect.x - 20, self.rect.x + self.width),
                                       random.randint(self.rect.y - 20, self.rect.y + self.height - 50)),
                         view="little")
        for i in range(random.randint(6, 10)):
            self.load_sprite(Money, coords=(random.randint(self.rect.x - 20, self.rect.x + self.width),
                                            random.randint(self.rect.y - 20, self.rect.y + self.height - 25)))
        self.find_sprites(SpriteTypes.PLAYER)[0].musik()
        self.kill()

    def update(self):
        if self.checking_touch_by_type(SpriteTypes.THROWING_WEAPON):
            self.health -= self.checking_touch_by_type(SpriteTypes.THROWING_WEAPON)[0].damadge

            if EngineSettings.get_var("PLAY_SOUNDS"):
                pygame.mixer.Channel(2).play(pygame.mixer.Sound("asi/main/resources/sound/arms_in_enemy.mp3"))

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
                else:
                    if random.randint(1, 10) < 6:
                        self.attack()
                        self.time = 0
                    elif random.randint(1, 6) < 3:
                        self.bombard()
                        self.time = 0
                    else:
                        self.big_attack()
                        self.time = 0
