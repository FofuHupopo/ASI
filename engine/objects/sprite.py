import pygame
import os

from dataclasses import dataclass
from typing import Sequence, Tuple

from engine.core import GameStack


@dataclass
class SpriteTypes:
    PLAYER = "player"
    ENEMY = "enemy"
    OBSTACLE = "obstacle"
    WEAPON = "weapon"
    STORAGE = "storage"
    NPC = "npc"
    THROWING_WEAPON = "throwing_weapon"


class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, scene=None, **kwargs) -> None:
        super().__init__(GameStack.get_sprite_group())

        self.__angel = 0.0
        self.__size: Tuple[int, int] = (100, 100)
        self.__coords: Tuple[int, int] = (0, 0)
        self.__image_path = ""
        self.__type = None
        
        self.__scene = scene

        self.init(**kwargs)

    def load_image(self, path: str):
        """Загрузка изображения для спрайта.

        Args:
            path (str): Путь до изображения относительно папки 'resources'.

        Raises:
            FileNotFoundError: Файл не найден.
        """

        self.__image_path = path
        fullname = os.path.join('asi/resources/', path)

        if not os.path.isfile(fullname):
            raise FileNotFoundError(f"Файл с изображением '{fullname}' не найден")

        self.image = pygame.image.load(fullname)
        self.rect = self.image.get_rect()
        
    def scale_image(self, new_size: Tuple[int, int], save_rect: bool = False, coords: Tuple[int, int] = None) -> None:
        """Изменения размеров спрайта.

        Args:
            new_size (Tuple[int, int]): Новые размеры (ширина, высота).
            save_rect (bool, optional): Сохранять предыдущие размеры. Обычно False.
            coords (Tuple[int, int], optional): Новые координаты. Обычно None.
        """
    
        self.__size = tuple(map(lambda value: max(value, 0), new_size))

        if coords:
            self.__coords = coords

        self.__reload_image(save_rect)

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
        # if type(type_) not in SpriteTypes:
        #     raise ValueError("Параметр 'type_' должен принадлежать классу 'SpriteTypes'")
        
        sprites = []
        
        for sprite in self.__scene.sprite_group.sprites():
            if sprite.get_type() != type_:
                continue
            
            print(pygame.Rect.colliderect(self.rect, sprite.rect))
            
            if pygame.Rect.colliderect(self.rect, sprite.rect):
                print(sprite)
                sprites.append(sprite)

        return sprites
    
    def load_sprite(self, sprite, kwargs):
        self.__scene.load_sprite(sprite, kwargs)
    
    def __reload_image(self, save_rect=False):
        self.load_image(self.__image_path)

        self.image = pygame.transform.scale(self.image, self.__size)
        self.image = pygame.transform.rotate(self.image, self.__angel)

        if not save_rect:
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center
            self.rect.x, self.rect.y = self.__coords[0], self.__coords[1]

    
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
    
    def _update(self):
        self.update()

    def events_handler(self, event: pygame.event.Event): ...
    
    def _events_handler(self, event: pygame.event.Event):
        self.events_handler(event)

    def key_pressed_handler(self, pressed: Sequence[bool]): ...

    def _key_pressed_handler(self, pressed: Sequence[bool]):
        self.key_pressed_handler(pressed)


