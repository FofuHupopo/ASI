import pygame
import enum

from typing import Sequence
from engine.core import GameStack


class BaseObject:
    def __init__(self, **kwargs) -> None:
        GameStack.append_stack(self)

        self.init(**kwargs)

    def init(self, **kwargs): ...
    
    def render(self, surface: pygame.Surface): ...
    
    def _render(self, surface: pygame.Surface):
        return self.render(surface)

    def update(self) -> None: ...
    
    def _update(self) -> None:
        dict = self.__dict__

        self.update()
        
        return dict == self.__dict__

    def events_handler(self, event: pygame.event.Event): ...
    
    def _events_handler(self, event: pygame.event.Event):
        self.events_handler(event)

    def key_pressed_handler(self, pressed: Sequence[bool]): ...
    
    def _key_pressed_handler(self, pressed: Sequence[bool]):
        self.key_pressed_handler(pressed)
