import pygame
import os

from dataclasses import dataclass
from typing import Sequence, Tuple

from engine.core import GameStack, Resources


@dataclass
class SpriteTypes:
    PLAYER = "player"
    ENEMY = "enemy"
    OBSTACLE = "obstacle"
    WEAPON = "weapon"
    STORAGE = "storage"
    NPC = "npc"
    THROWING_WEAPON = "throwing_weapon"
    HEAL = "heal"


class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, scene=None, scene_update=False, **kwargs) -> None:
        super().__init__(GameStack.get_sprite_group())

        self.__angel = 0.0
        self.__size: Tuple[int, int] = (100, 100)
        self.__image_path = ""
        self.__type = None

        self.__scene_update=scene_update
        self.__scene = scene

        self.init(**kwargs)

    def load_image(self, path: str):
        """Загрузка изображения для спрайта.

        Args:
            path (str): Путь до изображения относительно папки 'resources'.

        Raises:
            FileNotFoundError: Файл не найден.
        """

        fullname = Resources.get(path)
        self.__image_path = path

        self.image = pygame.image.load(fullname)
        self.rect = self.image.get_rect()
        
    def scale_image(self, new_size: Tuple[int, int]) -> None:
        """Изменения размеров спрайта.

        Args:
            new_size (Tuple[int, int]): Новые размеры (ширина, высота).
            save_rect (bool, optional): Сохранять предыдущие размеры. Обычно False.
            coords (Tuple[int, int], optional): Новые координаты. Обычно None.
        """
    
        self.__size = tuple(map(lambda value: max(value, 0), new_size))
        self.__reload_image()

    def rotate_image(self, angel: float):
        """Метод поворота спрайта.

        Args:
            angel (float): Угол поворота.
        """

        self.__angel = (self.__angel + angel) % 360
        self.__reload_image()

    def set_type(self, type_: SpriteTypes):
        """Метод для указания типа спрайта.
        Используйте 'engine.objects.sprite.SpriteTypes'

        Args:
            type_ (SpriteTypes): Тип спрайта.

        Raises:
            ValueError: Пердан не правильный тип спрайта.
        """

        # if type(type_) not in SpriteTypes.mro():
        #     raise ValueError("Параметр 'type_' должен принадлежать классу 'SpriteTypes'")
        
        self.__type = type_
        
    def get_type(self):
        return self.__type

    def checking_touch_by_type(self, type_: SpriteTypes):
        """Возвращает список объектов по типу, с которыми пересекается этот спрайт

        Args:
            type_ (SpriteTypes): Тип спрайтов

        Returns:
            _type_: _description_
        """
        # if type(type_) not in SpriteTypes:
        #     raise ValueError("Параметр 'type_' должен принадлежать классу 'SpriteTypes'")
        
        sprites = []
        
        for sprite in self.__scene.sprite_group.sprites():
            if sprite.get_type() != type_:
                continue
            
            if pygame.Rect.colliderect(self.rect, sprite.rect):
                sprites.append(sprite)

        return sprites
    
    def load_sprite(self, sprite, **kwargs):
        return self.__scene.load_sprite(sprite, **kwargs)
    
    def add_event(self, event):
        self.__scene.add_event(event)
    
    def get_events(self):
        return self.__scene.get_events()
    
    def find_sprites(self, sprite_type):
        return self.__scene.find_sprites(sprite_type)
    
    def __reload_image(self):
        old_rect = self.rect

        self.load_image(self.__image_path)
        
        self.image = pygame.transform.rotate(self.image, self.__angel)
        self.image = pygame.transform.scale(self.image, self.__size)
        
        # print(new_image.get_rect(), self.image.get_rect())
        
        self.rect = self.image.get_rect(
            x=old_rect.x,
            y=old_rect.y,
            center=old_rect.center
        )
    
    def reset_rotation_angel(self):
        """Обнуление угла поворота спрайта.
        """

        self.__angel = 0.0
        self.__reload_image()

    def init(self, **kwargs): ...
    
    def render(self, surface: pygame.Surface): ...
    
    def _render(self, surface: pygame.Surface):
        return self.render(surface)

    def update(self) -> None: ...
    
    def _update(self, scene_update=False):
        if self.__scene_update and scene_update: 
            self.update()

    def events_handler(self, event: pygame.event.Event): ...
    
    def _events_handler(self, event: pygame.event.Event):
        self.events_handler(event)

    def key_pressed_handler(self, pressed: Sequence[bool]): ...

    def _key_pressed_handler(self, pressed: Sequence[bool]):
        self.key_pressed_handler(pressed)
