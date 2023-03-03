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
        self.register_animations(
             "enemy/gunner/inac/acon-1.png",  # стоит
             {
                 "attack": (
                     "enemy/gunner/attack/atack-1.png",
                     "enemy/gunner/attack/atack-2.png",
                     "enemy/gunner/attack/atack-3.png",
                     "enemy/gunner/attack/atack-4.png",
                 ),  # атака
                 "bullet": (
                     "enemy/gunner/bullet/bullet.png"
                 ),  # патрон
                 "death": (
                     "enemy/gunner/death/death-1.png",
                     "enemy/gunner/death/death-2.png",
                     "enemy/gunner/death/death-3.png",
                     "enemy/gunner/death/death-4.png",
                     "enemy/gunner/death/death-5.png",
                     "enemy/gunner/death/death-6.png",
                     "enemy/gunner/death/death-7.png",
                     "enemy/gunner/death/death-8.png",
                     "enemy/gunner/death/death-9.png"
                 ),  # смерть
                 "hit": (
                     "enemy/gunner/hit/hit.png"
                 ),  # удар по стрелку от игрока
                 "inac": (
                     "enemy/gunner/inac/acon-1.png",
                 )
             }
         )
        self.scale_image((100, 100))
        self.set_type(SpriteTypes.ENEMY)

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
        self.atack = False


    def update(self):
        super().update()
        if self.direction == 1:
            self.mirror_image(by_x=True)
        else:
            self.mirror_image(by_x=False)
        if self.current_animation_frame == 3 and self.current_animation_name == "attack" and self.atack:
            self.atack = False
            if self.find_sprites(SpriteTypes.PLAYER)[0].rect.x > self.rect.x:
                self.load_sprite(Projectlie, coords=(self.rect.x + self.width, self.rect.y + 50),
                                 coords_player=self.find_sprites(SpriteTypes.PLAYER)[
                                     0].rect.x, damadge=25, speed=10, view="fire_ball")
            else:
                self.load_sprite(Projectlie, coords=(self.rect.x, self.rect.y + 50),
                                 coords_player=self.find_sprites(SpriteTypes.PLAYER)[0].rect.x, damadge=25, speed=10,
                                 view="fire_ball")



    def attack(self):
        if self.direction == 1:
            self.mirror_image(by_x=True)
        else:
            self.mirror_image(by_x=False)
        self.stop_animation()
        self.atack = True
        self.start_animation("attack", 1, 3, True)