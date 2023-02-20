import pygame

from typing import Sequence
from engine.core import GameStack


class BaseObject:
    def __init__(self, scene, **kwargs) -> None:
        GameStack.append_stack(self)
        self.__scene = scene

        self.init(**kwargs)
    
    def __del__(self):
        self.__scene.remove_object(self)

    def init(self, **kwargs): ...
    
    def load_object(self, object_class, **kwargs):
        return self.__scene.load_object(object_class, **kwargs)
    
    def add_event(self, event):
        self.__scene.add_event(event)
    
    def get_events(self):
        return self.__scene.get_events()
    
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
