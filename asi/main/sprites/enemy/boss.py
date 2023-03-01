import pygame
import random

from typing import Sequence
from dataclasses import dataclass

from engine.objects import BaseSprite, AnimatedSprite
from engine.core import EngineSettings
from engine.objects.sprite import SpriteTypes

from .projectile_enemy import Projectlie
from .grad import Grad
from ..player.HEAL import Heal
from ..player.money import Money


class Boss(AnimatedSprite):
    def init(self, coords):
        self.set_type(SpriteTypes.BOSS)
        self.register_animations(
            "boss/boss.png", {
                "attack": (
                    "boss/attack/boss_attack1.png",
                    "boss/attack/boss_attack2.png",
                    "boss/attack/boss_attack3.png",
                    "boss/attack/boss_attack4.png",
                    "boss/attack/boss_attack5.png",
                    "boss/attack/boss_attack6.png",
                    "boss/attack/boss_attack7.png",
                    "boss/attack/boss_attack8.png"
                ),
                "big_attack": (
                    "boss/big_attack/big_attack.png",
                    "boss/big_attack/big_attack2.png",
                    "boss/big_attack/big_attack3.png",
                    "boss/big_attack/big_attack4.png",
                    "boss/big_attack/big_attack5.png"
                ),
                "middle_attack": (
                    "boss/middle_attack/middle_attack1.png",
                    "boss/middle_attack/middle_attack2.png",
                    "boss/middle_attack/middle_attack3.png",
                    "boss/middle_attack/middle_attack4.png"
                )
            }
        )
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
        self.flag_attack = True

    def attack(self):
        if self.direction == 1:
            self.load_sprite(Projectlie, coords=(self.rect.x + self.width - 50, self.rect.y + 50),
                             coords_player=self.find_sprites(SpriteTypes.PLAYER)[0].rect.x, damadge=25, speed=10,
                             view="arms")
        else:
            self.load_sprite(Projectlie, coords=(self.rect.x + 50, self.rect.y + 50),
                             coords_player=self.find_sprites(SpriteTypes.PLAYER)[0].rect.x, damadge=25, speed=10,
                             view="arms")

    def big_attack(self):
        if self.direction == 1:
            self.load_sprite(Projectlie, coords=(self.rect.x + self.width - 100, self.rect.y + 50),
                             coords_player=self.find_sprites(SpriteTypes.PLAYER)[0].rect.x, damadge=50, speed=8,
                             view="ice_ball")
        else:
            self.load_sprite(Projectlie, coords=(self.rect.x + 100, self.rect.y + 50),
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
        if self.current_animation_frame == 6 and self.current_animation_name == "attack" and self.flag_attack:
            self.attack()
            self.flag_attack = False
        elif self.current_animation_frame == 4 and self.current_animation_name == "big_attack" and self.flag_attack:
            self.big_attack()
            self.flag_attack = False
        if self.checking_touch_by_type(SpriteTypes.THROWING_WEAPON):
            self.health -= self.checking_touch_by_type(SpriteTypes.THROWING_WEAPON)[0].damadge

            if EngineSettings.get_var("PLAY_SOUNDS"):
                pygame.mixer.Channel(2).play(pygame.mixer.Sound("asi/main/resources/sound/arms_in_enemy.mp3"))

            self.checking_touch_by_type(SpriteTypes.THROWING_WEAPON)[0].kill()

        if self.health == 0:
            self.dead()

        if self.find_sprites(SpriteTypes.PLAYER)[0].rect.x < self.rect.x and self.direction != 0:
            self.direction = 0
            self.mirror_image(by_x=True)
        elif self.find_sprites(SpriteTypes.PLAYER)[0].rect.x >= self.rect.x and self.direction != 1:
            self.mirror_image(by_x=False)
            self.direction = 1

        self.time = min(self.time + 1, self.time_attack)
        if self.var:
            if self.time_attack == self.time:
                self.flag_attack = True
                if self.checking_touch_by_type(SpriteTypes.PLAYER):
                    self.start_animation("middle_attack", 1, 4, True)
                    self.find_sprites(SpriteTypes.PLAYER)[0].change_health(
                        -50 * self.find_sprites(SpriteTypes.PLAYER)[0].arms)
                    if EngineSettings.get_var("PLAY_SOUNDS"):
                        pygame.mixer.Channel(13).play(pygame.mixer.Sound("asi/main/resources/sound/middle_attack.mp3"))
                    self.time = 0
                else:
                    if self.health > 750:
                        self.start_animation("attack", 1, 5, True)
                        if EngineSettings.get_var("PLAY_SOUNDS"):
                            pygame.mixer.Channel(13).play(pygame.mixer.Sound("asi/main/resources/sound/boss_attack.mp3"))
                        self.time = 0
                    elif self.health > 500:
                        if random.randint(1, 10) < 4:
                            self.start_animation("big_attack", 1, 5, True)
                            if EngineSettings.get_var("PLAY_SOUNDS"):
                                pygame.mixer.Channel(13).play(
                                    pygame.mixer.Sound("asi/main/resources/sound/zaryadka_lazera.mp3"))
                            self.time = 0
                        else:
                            self.start_animation("attack", 1, 5, True)
                            if EngineSettings.get_var("PLAY_SOUNDS"):
                                pygame.mixer.Channel(13).play(
                                    pygame.mixer.Sound("asi/main/resources/sound/boss_attack.mp3"))
                            self.time = 0
                    else:
                        if random.randint(1, 10) < 6:
                            self.start_animation("attack", 1, 5, True)
                            if EngineSettings.get_var("PLAY_SOUNDS"):
                                pygame.mixer.Channel(13).play(
                                    pygame.mixer.Sound("asi/main/resources/sound/boss_attack.mp3"))
                            self.time = 0
                        elif random.randint(1, 6) < 3:
                            self.bombard()
                            self.start_animation("middle_attack", 1, 4, True)
                            if EngineSettings.get_var("PLAY_SOUNDS"):
                                pygame.mixer.Channel(13).play(pygame.mixer.Sound("asi/main/resources/sound/middle_attack.mp3"))
                            self.time = 0
                        else:
                            self.start_animation("big_attack", 1, 5, True)
                            if EngineSettings.get_var("PLAY_SOUNDS"):
                                pygame.mixer.Channel(13).play(
                                    pygame.mixer.Sound("asi/main/resources/sound/zaryadka_lazera.mp3"))
                            self.time = 0