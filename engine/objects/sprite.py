import pygame
import os

from typing import Sequence, Tuple

from engine.core import GameStack


class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, **kwargs) -> None:
        super().__init__(GameStack.get_sprite_group())
        self.init(**kwargs)
        
    def load_image(self, path):
        self.__image_path = path
        fullname = os.path.join('asi/resources/', path)

        if not os.path.isfile(fullname):
            raise FileNotFoundError(f"Файл с изображением '{fullname}' не найден")

        self.image = pygame.image.load(fullname)
        self.rect = self.image.get_rect()
        
    def scale_image(self, new_size: Tuple[int, int], save_rect: bool = False, coords: Tuple[int, int] = None) -> None:
        x, y = self.rect.x, self.rect.y
        new_size = tuple(map(lambda value: max(value, 0), new_size))

        self.load_image(self.__image_path)
        self.image = pygame.transform.scale(self.image, new_size)
        
        if coords:
            x, y = coords

        if not save_rect:
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = x, y

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
