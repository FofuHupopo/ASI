import pygame
import random

from typing import Sequence

from engine.objects import BaseSprite
from .throwing_arms import Arms
from .obstacle import Obstacle
from .storage import Storage
from .trader import Trader
from engine.objects.sprite import SpriteTypes
from .map import Map


class PlayerObject(BaseSprite):
    def init(self):

        self.tile_image = {
            "wall": self.load_image("player/creature.png")
        }

        self.set_type(SpriteTypes.PLAYER)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.x = 500
        self.rect.y = 220
        self.speed_y = 0
        self.time_y = 0
        self.direction = 1
        self.health = 100
        self.level_sprites = []
    # ----------
        self.create_map(self.load_level("map.txt"))

    def create_map(self, level_map):
        for y in range(len(level_map)):
            row_sprite = []
            for x in range(len(level_map[y])):
                if level_map[y][x] == "#":
                    row_sprite.append(self.load_sprite(Obstacle, coords=[50 * x, 50 * y]))
                if level_map[y][x] == "$":
                    row_sprite.append(self.load_sprite(Storage, coords=[50 * x, 50 * y]))
                if level_map[y][x] == "t":
                    row_sprite.append(self.load_sprite(Trader, coords=[50 * x, 50 * y]))
            # self.level_sprites.append(row_sprite) - кусок хуйни, которого не видят

    @staticmethod
    def load_level(filename):  # загрузка уровня
        filename = r"asi/main/resources/map/" + filename
        with open(filename, "r") as mapFile:
            level_map = [line for line in mapFile]
        max_width = max(map(len, level_map))

        return list(map(lambda x: list(x.ljust(max_width, ".")), level_map))  # возвращаем список списков карты
    # -----------

    def is_fly(self):
        self.rect.y += 1
        if self.checking_touch_by_type(SpriteTypes.OBSTACLE) or self.checking_touch_by_type(SpriteTypes.STORAGE) \
                or self.checking_touch_by_type(SpriteTypes.NPC):
            self.rect.y -= 1
            return False
        else:
            self.rect.y -= 1
            return True

    def check(self, type):
        self.rect.x += 50
        if self.checking_touch_by_type(type):
            return self.checking_touch_by_type(type)[0]
        self.rect.x -= 100
        if self.checking_touch_by_type(type):
            return self.checking_touch_by_type(type)[0]
        self.rect.x += 50
        self.rect.y -= 50
        if self.checking_touch_by_type(type):
            return self.checking_touch_by_type(type)[0]
        self.rect.y += 50
        return None

    def update(self):
        self.rect.x += self.speed_x
        if self.direction == 1:
            for i in self.checking_touch_by_type(SpriteTypes.OBSTACLE):
                self.rect.x = min(self.rect.x, i.rect.x - self.width)
            for i in self.checking_touch_by_type(SpriteTypes.STORAGE):
                self.rect.x = min(self.rect.x, i.rect.x - self.width)
            for i in self.checking_touch_by_type(SpriteTypes.NPC):
                self.rect.x = min(self.rect.x, i.rect.x - self.width)
        else:
            for i in self.checking_touch_by_type(SpriteTypes.OBSTACLE):
                self.rect.x = max(self.rect.x, i.rect.x + i.width)
            for i in self.checking_touch_by_type(SpriteTypes.STORAGE):
                self.rect.x = max(self.rect.x, i.rect.x + i.width)
            for i in self.checking_touch_by_type(SpriteTypes.NPC):
                self.rect.x = max(self.rect.x, i.rect.x + i.width)
        if self.is_fly() or self.speed_y != 0:
            if self.speed_y == 0:
                self.time_y = 0.5
            self.rect.y -= self.speed_y
            if self.checking_touch_by_type(SpriteTypes.OBSTACLE) or self.checking_touch_by_type(SpriteTypes.STORAGE) \
                    or self.checking_touch_by_type(SpriteTypes.NPC):
                if self.speed_y > 0:
                    for i in self.checking_touch_by_type(SpriteTypes.OBSTACLE):
                        self.rect.y = max(self.rect.y, i.rect.y + i.height)
                    for i in self.checking_touch_by_type(SpriteTypes.STORAGE):
                        self.rect.y = max(self.rect.y, i.rect.y + i.height)
                    for i in self.checking_touch_by_type(SpriteTypes.NPC):
                        self.rect.y = max(self.rect.y, i.rect.y + i.height)
                    self.time_y = 0.5
                else:
                    for i in self.checking_touch_by_type(SpriteTypes.OBSTACLE):
                        self.rect.y = min(self.rect.y, i.rect.y - self.height)
                    for i in self.checking_touch_by_type(SpriteTypes.STORAGE):
                        self.rect.y = min(self.rect.y, i.rect.y - self.height)
                    for i in self.checking_touch_by_type(SpriteTypes.NPC):
                        self.rect.y = min(self.rect.y, i.rect.y - self.height)
                    self.time_y = 0
                    self.health -= max(0, (-25 - self.speed_y) * 4)
                    print(self.health)
                self.speed_y = 0
            else:
                self.speed_y -= self.time_y
                self.time_y += 10 * 0.002

    def events_handler(self, event: pygame.event.Event):
        keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN and keys[pygame.K_SPACE]:
            if not self.is_fly():
                self.speed_y = 10

        if event.type == pygame.KEYDOWN and keys[pygame.K_r]:
            self.load_sprite(Arms, coords=[self.rect.x + max(0, self.width * self.direction), self.rect.y],
                             direction=self.direction)

    def key_pressed_handler(self, pressed: Sequence[bool]):
        if pressed[pygame.K_a]:
            self.direction = -1
            self.speed_x = 5 * self.direction
        elif pressed[pygame.K_d]:
            self.direction = 1
            self.speed_x = 5 * self.direction
        else:
            self.speed_x = 0
        if pressed[pygame.K_e]:
            if self.check(SpriteTypes.STORAGE):
                self.check(SpriteTypes.STORAGE).open()