import pygame

from typing import Sequence

from engine.core import GameStack
from engine.objects import BaseObject, BaseSprite


class EventHandler:
    def event(self, event: pygame.event.Event):
        for object in GameStack.get_stack():
            object: BaseObject
            object._events_handler(event)
        
        for sprite in GameStack.get_sprite_group().sprites():
            sprite: BaseSprite
            sprite._events_handler(event)

    def key_pressed(self, pressed: Sequence[bool]):
        for object in GameStack.get_stack():
            object: BaseObject
            object._key_pressed_handler(pressed)
            
        for sprite in GameStack.get_sprite_group().sprites():
            sprite: BaseSprite
            sprite._key_pressed_handler(pressed)
