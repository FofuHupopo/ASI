import pygame

from dataclasses import dataclass
from typing import Sequence, Tuple, List

from engine.core import GameStack, Resources, EngineSettings
from engine.shortcuts import StartDialogObject


@dataclass
class SpriteTypes:
    PLAYER = "player"
    ENEMY = "enemy"
    OBSTACLE = "obstacle"
    DECORATION = "decoration"
    WEAPON = "weapon"
    STORAGE = "storage"
    NPC = "npc"
    BOARD = "board"
    THROWING_WEAPON = "throwing_weapon"
    HEAL = "heal"
    DOOR = "door"
    TRIGGER = "trigger"
    BOSS = "boss"
    TREADER = "treader"


class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, scene=None, scene_update=False, **kwargs) -> None:
        super().__init__(GameStack.get_sprite_group())

        self.__angel = 0.0
        self.__size: Tuple[int, int] = (100, 100)
        self.__image_path = ""
        self.__type = None
        self.__x_bool = False
        self.__y_bool = False

        self.__scene_update = scene_update
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
    
    def kill(self) -> None:
        super().kill()
        
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

    def mirror_image(self, by_x=None, by_y=None):
        if not isinstance(by_x, type(None)):
            self.__x_bool = by_x
            
        if not isinstance(by_y, type(None)):
            self.__y_bool = by_y
        
        self.__reload_image()
    
    def set_type(self, type_: SpriteTypes):
        """Метод для указания типа спрайта.
        Используйте 'engine.objects.sprite.SpriteTypes'

        Args:
            type_ (SpriteTypes): Тип спрайта.
        """
        
        self.__type = type_
        
    def get_type(self):
        return self.__type

    def checking_touch_by_type(self, type_: SpriteTypes) -> List["BaseSprite"]:
        """Возвращает список объектов по типу, с которыми пересекается этот спрайт

        Args:
            type_ (SpriteTypes): Тип спрайтов

        Returns:
            List: Список спрайтов
        """
        
        sprites = []
        
        for sprite in self.__scene.sprite_group.sprites():
            if sprite.get_type() != type_:
                continue
            
            if pygame.Rect.colliderect(self.rect, sprite.rect):
                sprites.append(sprite)

        return sprites
    
    def create_dialog(self, text, size):
        if self.checking_touch_by_type(SpriteTypes.PLAYER):
            if not hasattr(self, "dialog"):
                self.dialog = self.load_object(
                    StartDialogObject,
                    dialog_text=text,
                    dialog_size=size
                )
            else:
                if self.dialog.readed:
                    self.dialog.__del__()
                    del self.__dict__["dialog"]
        else:
            if hasattr(self, "dialog"):
                self.dialog.__del__()
                del self.__dict__["dialog"]

    def is_dialog(self):
        return hasattr(self, "dialog")

    def load_sprite(self, sprite_class, **kwargs):
        sprite = self.__scene.load_sprite(sprite_class, **kwargs)
        
        for group in self.groups():
            group.add(sprite)
        
        return sprite
    
    def load_object(self, object_class, **kwargs):
        return self.__scene.load_object(object_class, **kwargs)
    
    def add_event(self, event):
        self.__scene.add_event(event)
    
    def get_events(self):
        return self.__scene.get_events()
    
    def find_sprites(self, sprite_type):
        return self.__scene.find_sprites(sprite_type)
    
    def __reload_image(self, new_sprite_image_path: str=None):
        has_rect = False

        if hasattr(self, "rect"):
            old_rect = self.rect
            has_rect = True

        if new_sprite_image_path:
            self.load_image(new_sprite_image_path)
        else:
            self.load_image(self.__image_path)
        
        self.image = pygame.transform.rotate(self.image, self.__angel)
        self.image = pygame.transform.scale(self.image, self.__size)
        self.image = pygame.transform.flip(self.image, self.__x_bool, self.__y_bool)
        
        # print(new_image.get_rect(), self.image.get_rect())
        
        if has_rect:
            self.rect = self.image.get_rect(
                x=old_rect.x,
                y=old_rect.y,
                # center=old_rect.center  # располагает картинку по старому центру
            )
        else:
            self.rect = self.image.get_rect()
    
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


class AnimatedSprite(BaseSprite):
    def __init__(self, scene, **kwargs):
        self.__current_animation_name = None
        self.__current_animation_frame = 0
        self.animation_running = False
        
        self.__base_image_path = None
        self.__animations = dict()
    
        self.__current_animation_count = 1
        self.__current_animation_number = 1
        
        self.__current_animation_priority = False
        
        self.__waiting_ticks = 10
        self.__current_tick_after_animation = 0
        
        self.__draw_animations = EngineSettings.get_var("DRAW_ANIMATIONS")

        return super().__init__(scene, **kwargs)

    def register_animations(self, base_image_path, animations_dict):
        self.__base_image_path = base_image_path
        self.__animations = animations_dict

        self.__load_base_image()

    @property
    def current_animation_frame(self):
        return self.__current_animation_frame

    def start_animation(self, animation_name: str, count: int=1, waiting_ticks: int=10, is_priority: bool=False):
        """Метод начала анимации

        Args:
            animation_name (str): Название анимации
            count (int, optional): Кол-во повторений. По стандарту 1.
            waiting_ticks (int, optional): Задержка в тиках между анимациями. По стандарту 10.
            is_priority (bool, optional): Приоритет. Выолняется в любом случае или не выполняется при исполнении другой анимации.

        Raises:
            ValueError: Анимация с таким названием не существует
        """

        if animation_name not in self.__animations:
            raise ValueError(f"Анимация с именем {animation_name} не найдена.")
        
        self.__draw_animations = EngineSettings.get_var("DRAW_ANIMATIONS")
        
        if (self.animation_running and self.__current_animation_priority) or not self.__draw_animations:
            return

        self.__current_animation_name = animation_name
        self.__current_animation_frame = 0
        
        self.animation_running = True
        self.__current_animation_priority = is_priority
        
        self.__current_animation_count = count
        self.__current_animation_number = 0
        
        self.__waiting_ticks = waiting_ticks
        self.__current_tick_after_animation = 0
    
    def stop_animation(self):
        self.__current_animation_name = 0
        self.__current_animation_frame = None
        
        self.animation_running = False
        
        self.__current_animation_count = 1
        self.__current_animation_number = 0
        
        self.__waiting_ticks = 10
        self.__current_tick_after_animation = 10

        self.__load_base_image()
    
    def set_normal_image(self, image_path: str):
        self.__base_image_path = image_path
    
    def __load_base_image(self, path=None):
        self._BaseSprite__reload_image(
            path or self.__base_image_path
        )

    @property
    def current_animation_paths(self):
        return self.__animations[self.__current_animation_name]
    
    @property
    def current_animation_name(self):
        return self.__current_animation_name
        
    def __run_animation(self):
        self.__current_animation_frame += 1
        
        if self.__current_animation_frame >= len(self.current_animation_paths):
            self.__current_animation_frame = 0
            self.__current_animation_number += 1
            
            if self.__current_animation_number >= self.__current_animation_count:
                self.stop_animation()
                return
            
        self.__load_base_image(
            self.current_animation_paths[self.__current_animation_frame]
        )

    def _update(self, scene_update=False):
        if self.animation_running and self.__draw_animations:
            if self.__current_tick_after_animation > self.__waiting_ticks:
                self.__current_tick_after_animation = 0
                self.__run_animation()
            
            self.__current_tick_after_animation += 1

        return super()._update(scene_update)
