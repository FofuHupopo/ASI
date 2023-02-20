import pygame
import random

from engine.objects import BaseSprite
from engine.objects.sprite import SpriteTypes
from asi.main.sprites.player.HEAL import Heal
from asi.main.sprites.player.money import Money


class BaseEnemy(BaseSprite):
    def init(self):
        self.set_type(SpriteTypes.ENEMY)

    def find_zone(self):
        old_rect = (self.rect.x, self.rect.y)

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
        # self.rect.y = self.main_coordsy
        # self.rect.x = self.main_coordsx
        self.rect.x = old_rect[0]
        self.rect.y = old_rect[1]
        self.zone_x1 = self.zone_x1 - self.rect.x
        self.zone_x2 = self.zone_x2 - self.rect.x
        self.zone_y = self.rect.y - self.zone_y

    def dead(self):
        if random.randint(1, 10) <= self.chance_heal:
            self.load_sprite(Heal, coords=(random.randint(self.rect.x - 20, self.rect.x + self.width),
                                           random.randint(self.rect.y - 20, self.rect.y + self.height - 50)),
                             view="little")
        else:
            for i in range(random.randint(self.max_prize // 2, self.max_prize)):
                self.load_sprite(Money, coords=(random.randint(self.rect.x - 20, self.rect.x + self.width),
                                                random.randint(self.rect.y - 20, self.rect.y + self.height - 25)))
        pygame.mixer.Channel(9).play(pygame.mixer.Sound("asi/main/resources/sound/dead_enemy.mp3"))
        pygame.mixer.Channel(0).set_volume(0.05)
        self.kill()

    def update(self):
        if self.checking_touch_by_type(SpriteTypes.THROWING_WEAPON):
            self.health -= self.checking_touch_by_type(SpriteTypes.THROWING_WEAPON)[0].damadge
            pygame.mixer.Channel(2).play(pygame.mixer.Sound("asi/main/resources/sound/arms_in_enemy.mp3"))
            self.checking_touch_by_type(SpriteTypes.THROWING_WEAPON)[0].kill()
        if self.health <= 0:
            self.dead()
        self.coords_player = self.find_sprites(SpriteTypes.PLAYER)[0].rect
        self.time = min(self.time + 1, self.time_attack)
        if not self.flag_zone:
            self.find_zone()
        elif self.coords_player.x >= self.zone_x1 + self.rect.x - self.relacetion_x and \
                self.coords_player.x <= self.zone_x2 + self.rect.x - self.relacetion_x \
                and self.coords_player.y >= - self.zone_y + self.rect.y and self.coords_player.y <= self.rect.y:
            if abs(self.coords_player.x - self.rect.x) < self.attack_radius_x and \
                    abs(self.coords_player.y - self.rect.y < self.attack_radius_y):
                if self.time_attack <= self.time:
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
