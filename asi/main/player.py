import pygame
import random

from typing import Sequence
from dataclasses import dataclass
from engine.objects import BaseSprite
from engine.core import EngineEvent, EventTypes
from engine.objects.sprite import SpriteTypes

from .throwing_arms import Arms
from .obstacle import Obstacle
from .storage import Storage
from .trader import Trader


# from .animation import Animation


@dataclass
class PlayerСharacteristics:
    health = 100
    stamina = 100
    damage = 10
    stamina_boost = 3

    max_health = 100
    max_stamina = 100


class PlayerSprite(BaseSprite):
    def init(self, coords=(500, 220)):
        self.tile_image = {
            "player": self.load_image("player/creature.png")
        }

        self.set_type(SpriteTypes.PLAYER)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.x, self.rect.y = coords
        # self.rect.x = 500
        # self.rect.y = 220

        self.speed_y = 0
        self.time_y = 0
        self.time_x = 0
        self.direction = 1
        self.level_sprites = []

        self.count_heal = 0
        self.count_big_heal = 0
        self.money = 0

        self.list_door = self.find_sprites(SpriteTypes.DOOR)
        self.list_trigger = self.find_sprites(SpriteTypes.TRIGGER)

        self.__shift_pressed = False
        self.__artefacts = {
            "head": None,
            "necklace": None,
            "armor": None,
            "weapon": None,
            "bracelet": None,
            "boots": None,
        }

    # ----------
    # self.create_map(self.load_level("map.txt"))

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
            object = self.checking_touch_by_type(type)[0]
            self.rect.x -= 50
            return object
        self.rect.x -= 100
        if self.checking_touch_by_type(type):
            object = self.checking_touch_by_type(type)[0]
            self.rect.x += 50
            return object
        self.rect.x += 50
        self.rect.y += 50
        if self.checking_touch_by_type(type):
            object = self.checking_touch_by_type(type)[0]
            self.rect.y -= 50
            return object
        self.rect.y -= 50
        return None

    def update(self):
        if self.health == 0:
            self.dead()

        for localevent in self.get_events():
            if localevent["type"] == "info" and localevent["name"] == "minus_hp":
                self.change_health(-localevent["data"]["value"])

        self.rect.x += self.speed_x
        contact = self.checking_touch_by_type(SpriteTypes.OBSTACLE) + self.checking_touch_by_type(SpriteTypes.STORAGE) \
                  + self.checking_touch_by_type(SpriteTypes.NPC)
        if self.direction == 1:
            for i in contact:
                self.rect.x = min(self.rect.x, i.rect.x - self.width)
        else:
            for i in contact:
                self.rect.x = max(self.rect.x, i.rect.x + i.width)
        if self.is_fly() or self.speed_y != 0:
            if self.speed_y == 0:
                self.time_y = 0.5
            self.rect.y -= self.speed_y
            contact = self.checking_touch_by_type(SpriteTypes.OBSTACLE) + self.checking_touch_by_type(
                SpriteTypes.STORAGE) \
                      + self.checking_touch_by_type(SpriteTypes.NPC)
            if contact:
                if self.speed_y > 0:
                    for i in contact:
                        self.rect.y = max(self.rect.y, i.rect.y + i.height)
                    self.time_y = 0.5
                else:
                    for i in contact:
                        self.rect.y = min(self.rect.y, i.rect.y - self.height)
                    self.time_y = 0

                    self.change_health(-max(0, (-25 - self.speed_y) * 4))

                self.speed_y = 0
            else:
                self.speed_y -= self.time_y
                self.time_y += 10 * 0.002

        if self.__shift_pressed:
            self.__change_stamina(-0.8)
        else:
            if self.stamina < PlayerСharacteristics.max_stamina:
                self.__change_stamina(0.2)

    def events_handler(self, event: pygame.event.Event):
        keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN and keys[pygame.K_SPACE]:
            if not self.is_fly():
                self.speed_y = 10

        if event.type == pygame.KEYDOWN and keys[pygame.K_l]:
            self.__change_health(-10)

        if event.type == pygame.KEYDOWN and keys[pygame.K_r]:
            self.load_sprite(Arms, coords=[self.rect.x + max(0, self.width * self.direction), self.rect.y],
                             direction=self.direction)
        if event.type == pygame.KEYDOWN and keys[pygame.K_2] and self.count_heal > 0:
            self.change_health(50)
            self.count_heal -= 1
        if event.type == pygame.KEYDOWN and keys[pygame.K_1] and self.count_big_heal > 0:
            self.change_health(100)
            self.count_big_heal -= 1

    def change_health(self, value):
        PlayerСharacteristics.health = max(0, min(self.health + value, PlayerСharacteristics.max_health))

        self.add_event(EngineEvent(
            "info", "hp", {"value": self.health}
        ))

    def __change_stamina(self, value):
        PlayerСharacteristics.stamina = max(0, min(self.stamina + value, PlayerСharacteristics.max_stamina))

        self.add_event(EngineEvent(
            "info", "stamina", {"value": self.stamina}
        ))
        
    def dead(self):
        pass

    @property
    def health(self):
        return PlayerСharacteristics.health

    @property
    def stamina(self):
        return PlayerСharacteristics.stamina

    @property
    def stamina_boost(self):
        return PlayerСharacteristics.stamina_boost

    def key_pressed_handler(self, pressed: Sequence[bool]):
        additional_speed = self.stamina_boost * self.__shift_pressed * bool(self.stamina)

        if pressed[pygame.K_a]:
            self.direction = -1
            self.speed_x = 5 * self.direction + additional_speed * self.direction
            self.time_x = 8
        elif pressed[pygame.K_d]:
            self.direction = 1
            self.speed_x = 5 * self.direction + additional_speed * self.direction
            self.time_x = 8
        else:
            if self.time_x == 0:
                self.speed_x = 0
            else:
                self.speed_x = self.time_x * self.direction + additional_speed * self.direction
                self.time_x -= 1

        if pressed[pygame.K_e]:
            if self.check(SpriteTypes.STORAGE):
                self.check(SpriteTypes.STORAGE).open()

        self.__shift_pressed = pressed[pygame.K_LSHIFT]
