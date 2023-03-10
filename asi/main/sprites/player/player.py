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
class PlayerĐˇharacteristics:
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
        self.__died_timer_mx = 60
        self.__died_timer = 0
        
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
        self.flag_dialog = True
        self.flag_dialog_end = 0

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
    def load_level(filename):  # Đ·Đ°ĐłŃ€Ń?Đ·ĐşĐ° Ń?Ń€ĐľĐ˛Đ˝ŃŹ
        filename = r"asi/main/resources/map/" + filename
        with open(filename, "r") as mapFile:
            level_map = [line for line in mapFile]
        max_width = max(map(len, level_map))

        return list(map(lambda x: list(x.ljust(max_width, ".")), level_map))  # Đ˛ĐľĐ·Đ˛Ń€Đ°Ń‰Đ°ĐµĐĽ Ń?ĐżĐ¸Ń?ĐľĐş Ń?ĐżĐ¸Ń?ĐşĐľĐ˛ ĐşĐ°Ń€Ń‚Ń‹

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
        if self.__is_died:
            self.__died_timer += 1
            
            if self.__died_timer >= self.__died_timer_mx:
                self._BaseSprite__scene.respawn()
            
            return

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
            if self.stamina < PlayerĐˇharacteristics.max_stamina:
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
        joystick = None

        if pygame.joystick.get_count():
            joystick = pygame.joystick.Joystick(0)

        if (
            (event.type == pygame.KEYDOWN and keys[pygame.K_SPACE]) or
            (event.type == pygame.JOYBUTTONDOWN and event.button == 3)
        ):
            if not self.is_fly():
                self.speed_y = 10

        if (
            (event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_RIGHT) or
            (event.type == pygame.JOYBUTTONDOWN and event.button == 9)
        ):
            self.melee_attack()

        if (
            (event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT) or
            (event.type == pygame.JOYBUTTONDOWN and event.button == 10)
        ):
            if self.time_attack == self.recharge:
                self.__throw_arm()
                self.time_attack = 0

        if (
                (
                    (event.type == pygame.KEYDOWN and keys[pygame.K_1]) or
                    (event.type == pygame.JOYBUTTONDOWN and event.button == 13)
                ) and self.count_heal > 0
        ):
            self.change_health(50)
            self.count_heal -= 1
            if EngineSettings.get_var("PLAY_SOUNDS"):
                pygame.mixer.Channel(7).play(pygame.mixer.Sound("asi/main/resources/sound/little_heal.mp3"))

        if (
            (
                (event.type == pygame.KEYDOWN and keys[pygame.K_2]) or
                (event.type == pygame.JOYBUTTONDOWN and event.button == 11)
            ) and self.count_big_heal > 0
        ):
            self.change_health(100)
            if EngineSettings.get_var("PLAY_SOUNDS"):
                pygame.mixer.Channel(7).play(pygame.mixer.Sound("asi/main/resources/sound/big_heal.mp3"))
            self.count_big_heal -= 1

        if event.type == pygame.KEYDOWN and keys[pygame.K_3]:
            self.count_heal += 1
        if event.type == pygame.KEYDOWN and keys[pygame.K_4]:
            self.count_big_heal += 1
        if self.flag_dialog:
            self.create_dialog("Đž ĐłĐľŃ?ĐżĐľĐ´Đ¸, Ń‡Ń‚Đľ Ń?Đľ ĐĽĐ˝ĐľĐą Ń?Ń‚Đ°Đ»Đľ, ĐłĐ´Đµ ŃŹ... \n"
                               "Đ“Ń€Ń‘Đ±Đ°Đ˝Đ˝Ń‹Đµ Đ¸Đ˝Đ´ĐµĐąŃ†Ń‹ Ń?ĐşĐ°Đ·Đ°Đ»Đ¸ ĐĽĐ˝Đµ Ń‡Ń‚Đľ Đ˛ ŃŤŃ‚ĐľĐą ĐżĐµŃ‰ĐµŃ€Đµ ĐżĐľ Đ»ĐµĐłĐµĐ˝Đ´Đµ Đ»ĐµĐ¶Đ¸Ń‚ ĐĽĐ˝ĐľĐłĐľ ĐĽĐ˝ĐľĐłĐľ Đ·ĐľĐ»ĐľŃ‚Đ°,\n "
                               "Đ·Đ°Ń‡ĐµĐĽ ŃŹ Đ¸ĐĽ ĐżĐľĐ˛ĐµŃ€Đ¸Đ» Đ˛ ŃŤŃ‚Đ¸ ĐłĐ»Ń?ĐżĐľŃ?Ń‚Đ¸, Đ»Ń?Ń‡Ń?Đµ Đ±Ń‹ ĐľĐ±Ń‹Ń?ĐşĐ°Đ» Đ¸Ń… ĐµŃ‰Ń‘ Ń€Đ°Đ· Đ¸ Đ·Đ°Đ±Ń€Đ°Đ» Đ±Ń‹ ĐľŃ?Ń‚Đ°Ń‚ĐşĐ¸.\n"
                               "ĐťŃ? Đ˝Đ¸Ń‡ĐµĐłĐľ, Đ˛ĐľŃ‚ ĐşĐ°Đş Đ˛Ń‹Đ±ĐµŃ€Ń?Ń?ŃŚ ŃŹ Đ¸ĐĽ ŃŤŃ‚Đľ ĐżŃ€ĐľŃ?Ń‚Đľ Ń‚Đ°Đş Đ˝Đµ ĐľŃ?Ń‚Đ°Đ˛Đ»ŃŽ.Đ˘Đ°Đş, Đ»Đ°Đ´Đ˝Đľ, \n"
                               "ĐłĐ»Đ°Đ˛Đ˝ĐľĐµ Đ˝Đµ ĐżĐ°Đ˝Đ¸ĐşĐľĐ˛Đ°Ń‚ŃŚ, Đ˝Đ°Đ´Đľ Đ˝Đ°ĐąŃ‚Đ¸ Đ˛Ń‹Ń…ĐľĐ´ Đ¸Đ· ŃŤŃ‚ĐľĐą ĐĽĐµŃ?Ń‚Đ°, Đ° ĐµŃ?Đ»Đ¸ Đ¸Ń… Ń?Đ»ĐľĐ˛Đ° Đľ Đ±ĐľĐłĐ°Ń‚Ń?Ń‚Đ˛Đµ \n"
                               "ĐľĐşĐ°Đ¶Ń?Ń‚Ń?ŃŹ ĐżŃ€Đ°Đ˛Đ´ĐľĐą, Ń‚Đľ ŃŹ ĐľĐ±ŃŹĐ·Đ°Đ˝ ĐµĐłĐľ Đ˝Đ°ĐąŃ‚Đ¸, Đ¸ Ń‚ĐľĐłĐ´Đ° Ń?Ń‚Đ°Đ˝Ń? Ń?Đ°ĐĽŃ‹ĐĽ Đ±ĐľĐłĐ°Ń‚Ń‹ĐĽ Ń‡ĐµĐ»ĐľĐ˛ĐµĐşĐľĐĽ Đ˛\n"
                               "Đ®Đ¶Đ˝ĐľĐą Đ?ĐĽĐµŃ€Đ¸ĐşĐµ, ĐżĐľĐşĐ° ĐľŃ?Ń‚Đ°Đ»ŃŚĐ˝Ń‹Đµ Đ¸Ń?ĐżĐ°Đ˝Ń†Ń‹ Đ±Ń?Đ´Ń?Ń‚ ĐľŃ‚Đ±Đ¸Ń€Đ°Ń‚ŃŚ Đ¶Đ°Đ»ĐşĐ¸Đµ ĐłŃ€ĐľŃ?Đ¸ Ń? Đ¸Đ˝Đ´ĐµĐąŃ†ĐµĐ˛. Đ’\n"
                               "ĐşĐľĐ˝Ń†Đµ ĐşĐľĐ˝Ń†ĐľĐ˛, ŃŹ Đ¶Đµ Ń‚ĐľĐ¶Đµ Đ˝Đµ Đ°Đ±Ń‹ ĐşŃ‚Đľ, Đ˝Đµ Đ·Ń€ŃŹ Đ¶Đµ ŃŹ ĐżŃ€Đ¸ĐµŃ…Đ°Đ» Đ¸Đ· Đ?Ń?ĐżĐ°Đ˝Đ¸Đ¸ Đ˛ Ń‚Đ°ĐşĐ¸Đµ ĐşŃ€Đ°ŃŹ.\n"
                               "ĐťĐ°Đ´Đľ ĐżĐľŃ?Ń‚Đ°Ń€Đ°Ń‚ŃŚŃ?ŃŹ Đ˛Ń?ĐżĐľĐĽĐ˝Đ¸Ń‚ŃŚ, Ń‡Ń‚Đľ Đ˛ĐľĐľĐ±Ń‰Đµ ĐżŃ€ĐľĐ¸Đ·ĐľŃ?Đ»Đľ â€¦ ĐˇŃ‚Ń€Đ°Đ˝Đ˝Đľ, ŃŹ ĐżĐľĐĽĐ˝ŃŽ, ĐşĐ°Đş Đ·Đ°Ń?Ń‘Đ» Đ˛ ŃŤŃ‚Ń?\n"
                               "ĐżĐµŃ‰ĐµŃ€Ń?, Đ° Đ´Đ°Đ»ŃŚŃ?Đµ Ń‚ĐľĐ»ŃŚĐşĐľ ĐżŃ?Ń?Ń‚ĐľŃ‚Đ°, Đ¸ Đ˛ĐľŃ‚ ŃŹ ĐľĐşĐ°Đ·Ń‹Đ˛Đ°ŃŽŃ?ŃŚ Đ·Đ´ĐµŃ?ŃŚ. ĐťĐľ Ń‡Ń‚Đľ Ń?Ń‚Đ°Đ»Đľ Ń? ĐĽĐľĐ¸ĐĽ Ń‚ĐµĐ»ĐľĐĽ.\n"
                               "Đ•ĐłĐľ ĐżŃ€Đ°ĐşŃ‚Đ¸Ń‡ĐµŃ?ĐşĐ¸ Đ˝ĐµŃ‚, ŃŹ ĐżŃ€ĐµĐ˛Ń€Đ°Ń‚Đ¸Đ»Ń?ŃŹ Đ˛ ĐşĐ°ĐşĐľĐą-Ń‚Đľ Đ´Ń?Ń… ",
                               (700, 400))

        
            if (
                    (event.type == pygame.KEYDOWN and keys[pygame.K_f]) or
                    (event.type == pygame.JOYBUTTONDOWN and event.button == 1)
                ):
                self.flag_dialog = False

        if len(self.find_sprites(SpriteTypes.BOSS)) == 0:
            if self.flag_dialog_end < 3:
                self.create_dialog(["ĐŁŃ€Đ°, Đ´ĐµĐ»Đľ Ń?Đ´ĐµĐ»Đ°Đ˝Đľ, Đ˝Ń? Đ˛Ń?Ń‘, ĐłĐ´Đµ Đ˛Ń‹Ń…ĐľĐ´ ", "ĐťĐ¸Ń‡ĐµĐłĐľ Đ˝Đµ Đ¸Đ·ĐĽĐµĐ˝Đ¸Đ»ĐľŃ?ŃŚ... ",
                                    "ĐšĐ°Đ¶ĐµŃ‚Ń?ŃŹ Ń‚ĐµĐżĐµŃ€ŃŚ Đ˛Ń?Ń‘ ĐżĐľĐ˝ŃŹŃ‚Đ˝Đľ, ŃŤŃ‚Đľ Đ˛Ń?Ń‘ Đ»Đ¸Ń?ŃŚ Đ»ĐľĐ˛Ń?Ń?ĐşĐ° ŃŤŃ‚ĐľĐłĐľ Đ±ĐľĐ¶ĐµŃ?Ń‚Đ˛Đ°, Đ˛Ń?Ń‘ ŃŤŃ‚Đľ Đ˝Đµ Đ¸ĐĽĐµĐµŃ‚\n"
                                    "Đ˝Đ¸ĐşĐ°ĐşĐľĐłĐľ Đ·Đ˝Đ°Ń‡ĐµĐ˝Đ¸ŃŹ, Ń‚ĐľŃ€ĐłĐľĐ˛Ń†Ń‹, Ń?Ń?Đ˝Đ´Ń?ĐşĐ¸, Đ»ĐµŃ‡ĐµĐ˝Đ¸Đµ, ĐżŃ€ĐľĐşĐ°Ń‡ĐşĐ° ŃŤŃ‚Đľ Đ˛Ń?Ń‘ Đ»Đ¸Ń?ŃŚ ĐşĐ°ĐşĐ°ŃŹ-Ń‚Đľ\n"
                                    "Đ¸Đ»Đ»ŃŽĐ·Đ¸ŃŹ, Ń‡Ń‚ĐľĐ±Ń‹ Ń‚Ń‹ ĐżĐľĐ±ĐľĐ»ŃŚŃ?Đµ ĐżĐľĐĽŃ?Ń‡Đ°Đ»Ń?ŃŹ, Ń‡Ń‚ĐľĐ±Ń‹ Đ´Đľ ĐżĐľŃ?Đ»ĐµĐ´Đ˝ĐµĐłĐľ Đ˝Đµ Ń‚ĐµŃ€ŃŹĐ» Đ˝Đ°Đ´ĐµĐ¶Đ´Ń? Đ˛Ń‹Đ±Ń€Đ°Ń‚ŃŚŃ?ŃŹ ĐľŃ‚Ń?ŃŽĐ´Đ°...",
                                    "Đ“ĐľĐ»ĐľŃ? Ń?Đ˛ĐµŃ€Ń…Ń?: Ń…Đ°-Ń…Đ°, Đ˝Đ°Đ´Đľ ĐľŃ‚Đ´Đ°Ń‚ŃŚ Đ´ĐľĐ»Đ¶Đ˝ĐľĐµ Ń‚Ń‹ ĐżŃ€ĐľŃ?Ń‘Đ» ĐĽĐľŃ‘ Đ¸Ń?ĐżŃ‹Ń‚Đ°Đ˝Đ¸Đµ Đ´Đľ ĐşĐľĐ˝Ń†Đ° Đ¸\n"
                                    " Đ˛ ĐşĐľĐ˝Ń†Đµ Ń‚Ń‹ Đ˛Ń?Ń‘ ĐżĐľĐ˝ŃŹĐ», Ń‚Ń‹ Đ˝Đ¸ĐşĐľĐłĐ´Đ° ĐľŃ‚Ń?ŃŽĐ´Đ° Đ˝Đµ Đ˛Ń‹Đ±ĐµŃ€ĐµŃ?ŃŚŃ?ŃŹ, Ń‚Ń‹ Đ±Ń?Đ´ĐµŃ?ŃŚ Ń?ĐşĐ¸Ń‚Đ°Ń‚ŃŚŃ?ŃŹ Đ·Đ´ĐµŃ?ŃŚ\n"
                                    " Đ˛ĐµŃ‡Đ˝ĐľŃ?Ń‚ŃŚ ĐżĐľĐşĐ° Đ˝Đµ ĐżĐľŃ‚ĐµŃ€ŃŹĐµŃ?ŃŚ Ń€Đ°Ń?Ń?Ń?Đ´ĐľĐş, Đ˛Ń?Đµ Đ˛Ń‹ Đ¶Đ°Đ»ĐşĐ¸Đµ Đ»ŃŽĐ´Đ¸, Đ˛Ń‹ Ń‚ĐľĐ»ŃŚĐşĐľ Đ¸ Đ´Ń?ĐĽĐ°ĐµŃ‚Đµ\n"
                                    " Đľ Đ´ĐµĐ˝ŃŚĐłĐ°Ń…, Đľ Ń?Đ»Đ°Đ˛Đµ, Đľ Đ˛Ń‹ĐłĐľĐ´Đµ. Đ’Ń‹ Ń?Đ»Đ¸Ń?ĐşĐľĐĽ Đ°Đ»Ń‡Đ˝Ń‹, Ń‡Ń‚ĐľĐ±Ń‹ Đ·Đ°ĐĽĐµŃ‡Đ°Ń‚ŃŚ ĐşŃ€Đ°Ń?ĐľŃ‚Ń?\n"
                                    " Đ¸ ĐżŃ€ĐµĐşŃ€Đ°Ń?Đ˝ĐľŃ?Ń‚ŃŚ ŃŤŃ‚ĐľĐłĐľ ĐĽĐ¸Ń€Đ°, Đ˛Ń‹ Đ˝Đµ Đ·Đ°Ń?Đ»Ń?Đ¶Đ¸Đ˛Đ°ĐµŃ‚Đµ Đ¶Đ¸Ń‚ŃŚ Đ˝Đ° ŃŤŃ‚ĐľĐĽ Ń?Đ˛ĐµŃ‚Đµ. Đ”Đ»ŃŹ Ń‚Đ°ĐşĐ¸Ń… ĐşĐ°Đş\n"
                                    " Đ˛Ń‹ ŃŹ Đ¸ Ń?ĐľĐ·Đ´Đ°Đ» ŃŤŃ‚ĐľŃ‚ Đ»Đ°Đ±Đ¸Ń€Đ¸Đ˝Ń‚, Ń‡Ń‚ĐľĐ±Ń‹ Đ¸Đ·Đ±Đ°Đ˛Đ»ŃŹŃ‚ŃŚ ŃŤŃ‚ĐľŃ‚ ĐĽĐ¸Ń€ ĐľŃ‚ Ń‚Đ°ĐşĐ¸Ń… Đ˝Đ¸Ń‡Ń‚ĐľĐ¶ĐµŃ?Ń‚Đ˛ ĐşĐ°Đş Đ˛Ń‹.\n"
                                    " ĐśĐľĐ¶ĐµŃ?ŃŚ Ń?Ń‚Đ°Ń‚ŃŚ Ń…ĐľŃ‚ŃŚ ĐĽĐ¸Đ»Đ»Đ¸ĐľĐ˝ĐµŃ€ĐľĐĽ, Đ·Đ°Ń€Đ°Đ±ĐľŃ‚Đ°Ń‚ŃŚ ĐłĐľŃ€Ń‹ Đ·ĐľĐ»ĐľŃ‚Đ°, Ń?Đ±Đ¸Ń‚ŃŚ Đ·Đ´ĐµŃ?ŃŚ Đ˛Ń?ĐµŃ…, ĐşŃ?ĐżĐ¸Ń‚ŃŚ\n"
                                    " Đ˛Ń?Đµ Ń?Đ°ĐĽĐľĐµ Đ»Ń?Ń‡Ń?ĐµĐµ Đ¸ Ń?Ń‚Đ°Ń‚ŃŚ Ń?Đ°ĐĽŃ‹ĐĽ Ń?Đ¸Đ»ŃŚĐ˝Ń‹ĐĽ, Ń‚Ń‹ Đ˝Đ¸ Đ·Đ° Ń‡Ń‚Đľ Đ˝Đµ Đ˛Ń‹ĐąĐ´ĐµŃ?ŃŚ ĐľŃ‚Ń?ŃŽĐ´Đ°.\n"
                                    " ĐˇŃ‡Đ°Ń?Ń‚Đ»Đ¸Đ˛Đľ ĐľŃ?Ń‚Đ°Đ˛Đ°Ń‚ŃŚŃ?ŃŹ.  Đ?Đ»Đ¸ ĐşĐ°Đş Ń‚Đ°ĐĽ Ń? Đ˛Đ°Ń? ĐłĐľĐ˛ĐľŃ€ŃŹŃ‚ Đ˛ Đ?Ń?ĐżĐ°Đ˝Đ¸Đ¸ Feliz estancia",
                                    "Đ“Đł - Đ? ĐżĐľŃ‡ĐµĐĽŃ? ĐĽĐ˝Đµ Ń?Đ¸Đ´ĐµĐ»ĐľŃ?ŃŚ Ń? Ń?ĐµĐ±ŃŹ Đ˝Đ° Ń€ĐľĐ´Đ¸Đ˝Đµ, Ń€Đ°Đ´Đ¸ Ń‡ĐµĐłĐľ ŃŹ ĐżĐľĐµŃ…Đ°Đ» Ń?ŃŽĐ´Đ°, Ń‚ĐľĐ»ŃŚĐşĐľ Ń€Đ°Đ´Đ¸\n"
                                    " ŃŤŃ‚Đ¸Ń… ĐłĐ°Đ»Đ¸ĐĽŃ‹Ń… Đ´ĐµĐ˝ĐµĐł. ĐźĐľŃ‚Ń€Đ°Ń‚Đ¸Đ» Đ˛Ń?ŃŽ Ń?Đ˛ĐľŃŽ Đ¶Đ¸Đ·Đ˝ŃŚ Đ˛ ĐżŃ?Ń?Ń‚Ń?ŃŽ... "], (800, 400))
                if event.type == pygame.KEYDOWN and keys[pygame.K_f]:
                    self.flag_dialog_end += 1


    def change_health(self, value):
        PlayerĐˇharacteristics.health = max(0, min(self.health + value, PlayerĐˇharacteristics.max_health))
        self.add_event(EngineEvent(
            "info", "hp", {"value": self.health}
        ))

        if self.health <= 0 and not self.__is_died:
            self.start_animation(
                "death", 1, 10, is_priority=True
            )
            self.set_normal_image("player/blank.png")

            if EngineSettings.get_var("PLAY_SOUNDS"):
                pygame.mixer.Channel(9).play(pygame.mixer.Sound("asi/main/resources/sound/dead_player.mp3"))

            self.__is_died = True
            self.__can_move = False

            self.change_health(PlayerĐˇharacteristics.max_health)

    def __change_stamina(self, value):
        PlayerĐˇharacteristics.stamina = max(0, min(self.stamina + value, PlayerĐˇharacteristics.max_stamina))

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
        self.change_health(-self.health)

    @property
    def health(self):
        return PlayerĐˇharacteristics.health

    @property
    def stamina(self):
        return PlayerĐˇharacteristics.stamina

    @property
    def stamina_boost(self):
        return PlayerĐˇharacteristics.stamina_boost

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
        PlayerĐˇharacteristics.money = value

        self.add_event(EngineEvent(
            "info", "money", {"value": self.money}
        ))

    def get_money(self):
        return PlayerĐˇharacteristics.money

    money = property(fset=set_money, fget=get_money)
    
    def update_ui(self):
        self.change_health(0)
        self.__change_stamina(0)
        self.set_little_heal(self.get_little_heal())
        self.set_big_heal(self.get_big_heal())
        self.set_money(self.money)

    def key_pressed_handler(self, pressed: Sequence[bool]):
        additional_speed = self.stamina_boost * self.__shift_pressed * bool(self.stamina)
        joy_axis = 0

        if pygame.joystick.get_count():
            joy_axis = pygame.joystick.Joystick(0).get_axis(0)

        if (pressed[pygame.K_a] or (joy_axis and joy_axis < -0.3)) and self.__can_move:
            self.direction = -1
            self.speed_x = 5 * self.direction + additional_speed * self.direction
            self.time_x = 8

            self.mirror_image(by_x=True)
            if self.current_animation_name != "walk":
                self.start_animation("walk", 1, 7)
        elif (pressed[pygame.K_d] or (joy_axis and joy_axis > 0.3)) and self.__can_move:
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
