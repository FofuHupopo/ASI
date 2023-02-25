import pygame
import random

from typing import Sequence
from dataclasses import dataclass
from engine.objects import BaseSprite, AnimatedSprite
from engine.core import EngineEvent, EventTypes, EngineSettings
from engine.objects.sprite import SpriteTypes

from .throwing_arms import Arms
from ..environment.obstacle import Obstacle
from .storage import Storage
from ..npc.trader import Trader

from asi import settings


# from .animation import Animation


@dataclass
class PlayerСharacteristics:
    health = 100
    stamina = 100
    damage = 10
    stamina_boost = 3

    max_health = 100
    max_stamina = 100

    money = 0


class PlayerSprite(AnimatedSprite):
    def init(self, coords=(500, 220)):
        # self.tile_image = {
        #     "player": self.load_image("player/creature.png")
        # }
        self.register_animations(
            "player/normal.png",
            {
                "idle": (
                    "player/idle/idle-1.png",
                    "player/idle/idle-2.png"
                ),
                "blink": (
                    "player/blink/blink-1.png",
                    "player/blink/blink-2.png",
                ),
                "walk": (
                    "player/walk/walk-1.png",
                    "player/walk/walk-2.png",
                    "player/walk/walk-3.png",
                    "player/walk/walk-4.png",
                ),
                "death": (
                    "player/death/death-1.png",
                    "player/death/death-2.png",
                    "player/death/death-3.png",
                    "player/death/death-4.png",
                ),
                "melee_attack": (
                    "player/attack/attack-1.png",
                    "player/attack/attack-2.png",
                    "player/attack/attack-3.png",
                    "player/attack/attack-4.png",
                    "player/attack/attack-5.png",
                    "player/attack/attack-6.png",
                    "player/attack/attack-7.png",
                    "player/attack/attack-8.png",
                )
            }
        )
        self.__idle_counter = 0
        self.__idle_mx = 8
        self.scale_image((50, 100))

        self.set_type(SpriteTypes.PLAYER)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.x, self.rect.y = coords
        # self.rect.x = 500
        # self.rect.y = 220

        self.speed_y = 0
        self.speed_x = 0
        self.time_y = 0
        self.time_x = 0
        self.direction = 1
        self.level_sprites = []

        self.__count_big_heal = 0
        self.__count_heal = 0
        self.arms = 1
        self.recharge = 30

        self.__can_move = True
        self.__is_died = False
        self.__throwing_arms_count = 6
        self.__throwing_arms_max_value = 6
        self.__throwing_arms_cd = 50
        self.__throwing_arms_cd_number = 0

        self.send_throwing_arm_event()

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

        pygame.mixer.init()
        self.list_musik = ["fon_horizon.mp3", "fon_inrestellar.mp3", "fon_original1.mp3", "fon_original2.mp3",
                           "fon_original3.mp3", "fon_original4.mp3", "fon_wither.mp3", "fon_detroit.mp3"]
        self.now_musik = -1

        if EngineSettings.get_var("PLAY_SOUNDS"):
            self.musik()

        pygame.mixer.set_num_channels(15)
        self.time_attack = self.recharge

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
        if self.current_animation_frame == 4 and self.current_animation_name == "melee_attack" and self.time_attack == self.recharge:
            self.time_attack = 0
            if EngineSettings.get_var("PLAY_SOUNDS"):
                pygame.mixer.Channel(14).play(pygame.mixer.Sound("asi/main/resources/sound/player_attack.mp3"))
            for i in self.checking_touch_by_type(SpriteTypes.ENEMY):
                i.health -= 100
            if len(self.find_sprites(SpriteTypes.BOSS)) > 0:
                boss = self.find_sprites(SpriteTypes.BOSS)[0]
                if self.rect.x > boss.rect.x - 50 and self.rect.x < boss.rect.x + 100 and self.rect.y > boss.rect.y - 50:
                    boss.health -= 100

        self.time_attack = min(self.recharge, self.time_attack + 1)

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
                    if EngineSettings.get_var("PLAY_SOUNDS"):
                        pygame.mixer.Channel(8).play(pygame.mixer.Sound("asi/main/resources/sound/player_in_floor.mp3"))
                        pygame.mixer.Channel(8).set_volume(0.1)
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

        if (
                self.__throwing_arms_cd_number < self.__throwing_arms_cd and
                self.__throwing_arms_count < self.__throwing_arms_max_value
        ):
            self.__throwing_arms_cd_number += 1
        elif (
                self.__throwing_arms_cd_number >= self.__throwing_arms_cd and
                self.__throwing_arms_count < self.__throwing_arms_max_value
        ):
            self.__throwing_arms_cd_number = 0
            self.__throwing_arms_count += 1

        self.send_throwing_arm_event()
        if not pygame.mixer.get_busy():
            self.musik()

        # elif self.__throwing_arms_count == self.__throwing_arms_max_value:
        #     self.__throwing_arms_cd_number = 0

    def events_handler(self, event: pygame.event.Event):
        keys = pygame.key.get_pressed()

        if (
                (event.type == pygame.KEYDOWN and keys[pygame.K_SPACE]) or
                (event.type == pygame.JOYBUTTONDOWN and event.button == 3)
        ):
            if not self.is_fly():
                self.speed_y = 10

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_RIGHT:
            self.melee_attack()

        if (
                (event.type == pygame.KEYDOWN and keys[pygame.K_r]) or
                (event.type == pygame.JOYBUTTONDOWN and event.button == 10)
        ):
            if self.time_attack == self.recharge:
                self.__throw_arm()
                self.time_attack = 0

        if (
                (event.type == pygame.KEYDOWN and keys[pygame.K_1] and self.count_heal > 0) or
                (event.type == pygame.JOYBUTTONDOWN and event.button == 13)
        ):
            self.change_health(50)
            self.count_heal -= 1
            if EngineSettings.get_var("PLAY_SOUNDS"):
                pygame.mixer.Channel(7).play(pygame.mixer.Sound("asi/main/resources/sound/little_heal.mp3"))
        if event.type == pygame.KEYDOWN and keys[pygame.K_2] and self.count_big_heal > 0:
            self.change_health(100)
            if EngineSettings.get_var("PLAY_SOUNDS"):
                pygame.mixer.Channel(7).play(pygame.mixer.Sound("asi/main/resources/sound/big_heal.mp3"))
            self.count_big_heal -= 1

        if event.type == pygame.KEYDOWN and keys[pygame.K_3]:
            self.count_heal += 1
        if event.type == pygame.KEYDOWN and keys[pygame.K_4]:
            self.count_big_heal += 1

    def change_health(self, value):
        PlayerСharacteristics.health = max(0, min(self.health + value, PlayerСharacteristics.max_health))
        self.add_event(EngineEvent(
            "info", "hp", {"value": self.health}
        ))

        if self.health == 0:
            # self.dead()
            self.start_animation(
                "death", 1, 10, is_priority=True
            )
            # self.set_normal_image("player/blank.png")
            if EngineSettings.get_var("PLAY_SOUNDS"):
                pygame.mixer.Channel(9).play(pygame.mixer.Sound("asi/main/resources/sound/dead_player.mp3"))
            # self.__is_died = True
            # self.__can_move = False

            self.change_health(PlayerСharacteristics.max_health)

    def __change_stamina(self, value):
        PlayerСharacteristics.stamina = max(0, min(self.stamina + value, PlayerСharacteristics.max_stamina))

        self.add_event(EngineEvent(
            "info", "stamina", {"value": self.stamina}
        ))

    def melee_attack(self):
        self.start_animation("melee_attack", 1, 4, True)



    def __throw_arm(self):
        if self.__throwing_arms_count > 0:
            self.__throwing_arms_count -= 1
            self.load_sprite(
                Arms,
                coords=[self.rect.x + max(0, self.width * self.direction), self.rect.y],
                direction=self.direction
            )

            self.send_throwing_arm_event()

    def send_throwing_arm_event(self):
        self.add_event(
            EngineEvent(
                "info", "shuriken_count", {
                    "value": self.__throwing_arms_count
                }
            )
        )

    def dead(self):
        if self.health != 0:
            self.change_health(-100)

    @property
    def health(self):
        return PlayerСharacteristics.health

    @property
    def stamina(self):
        return PlayerСharacteristics.stamina

    @property
    def stamina_boost(self):
        return PlayerСharacteristics.stamina_boost

    def set_little_heal(self, value):
        self.__count_heal = value

        self.add_event(EngineEvent(
            "info", "little_heal", {"value": self.__count_heal}
        ))

    def get_little_heal(self):
        return self.__count_heal

    count_heal = property(fset=set_little_heal, fget=get_little_heal)

    def set_big_heal(self, value):
        self.__count_big_heal = value

        self.add_event(EngineEvent(
            "info", "big_heal", {"value": self.__count_big_heal}
        ))

    def get_big_heal(self):
        return self.__count_big_heal

    count_big_heal = property(fset=set_big_heal, fget=get_big_heal)

    def set_money(self, value):
        PlayerСharacteristics.money = value

        self.add_event(EngineEvent(
            "info", "money", {"value": self.money}
        ))

    def get_money(self):
        return PlayerСharacteristics.money

    money = property(fset=set_money, fget=get_money)

    def key_pressed_handler(self, pressed: Sequence[bool]):
        additional_speed = self.stamina_boost * self.__shift_pressed * bool(self.stamina)
        # joy_axis = pygame.joystick.Joystick(0).get_axis(0)
        joy_axis = 0

        if (pressed[pygame.K_a] or joy_axis < -0.3) and self.__can_move:
            self.direction = -1
            self.speed_x = 5 * self.direction + additional_speed * self.direction
            self.time_x = 8

            self.mirror_image(by_x=True)
            if self.current_animation_name != "walk":
                self.start_animation("walk", 1, 7)
        elif (pressed[pygame.K_d] or joy_axis > 0.3) and self.__can_move:
            self.direction = 1
            self.speed_x = 5 * self.direction + additional_speed * self.direction
            self.time_x = 8

            self.mirror_image(by_x=False)
            if self.current_animation_name != "walk":
                self.start_animation("walk", 1, 7)
        else:
            if self.time_x == 0:
                self.speed_x = 0
            else:
                self.speed_x = self.time_x * self.direction + additional_speed * self.direction
                self.time_x -= 1

            if not self.animation_running and self.__can_move:
                if self.__idle_counter >= self.__idle_mx:
                    self.__idle_counter = 0
                    self.start_animation("blink", 1, 20)
                else:
                    self.__idle_counter += 1
                    self.start_animation("idle", 1, 20)

        if pressed[pygame.K_e]:
            if self.check(SpriteTypes.STORAGE):
                self.check(SpriteTypes.STORAGE).open()

        self.__shift_pressed = pressed[pygame.K_LSHIFT]

    def musik(self):
        id = random.randint(0, 7)
        while id == self.now_musik:
            id = random.randint(0, 7)
        self.now_musik = id

        if EngineSettings.get_var("PLAY_SOUNDS"):
            pygame.mixer.Channel(0).play(pygame.mixer.Sound("asi/main/resources/musik/" + self.list_musik[id]))
            pygame.mixer.Channel(0).set_volume(0.2)
