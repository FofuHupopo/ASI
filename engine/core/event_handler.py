import pygame

from typing import Sequence

from . import GameStack


class EventHandler:
    @staticmethod
    def event(event: pygame.event.Event):
        for object in GameStack.get_stack():
            object._events_handler(event)
        
        for sprite in GameStack.get_sprite_group().sprites():
            sprite._events_handler(event)

    @staticmethod
    def key_pressed(pressed: Sequence[bool]):
        for object in GameStack.get_stack():
            object._key_pressed_handler(pressed)
            
        for sprite in GameStack.get_sprite_group().sprites():
            sprite._key_pressed_handler(pressed)


class SceneEventHandler:
    def __init__(self, game_stack) -> None:
        self.__scene_game_stack = game_stack

    def event(self, event: pygame.event.Event):
        for object in self.__scene_game_stack.object_stack:
            object._events_handler(event)
        
        for sprite in self.__scene_game_stack.sprite_group:
            sprite._events_handler(event)

    def key_pressed(self, pressed: Sequence[bool]):
        for object in self.__scene_game_stack.object_stack:
            object._key_pressed_handler(pressed)
            
        for sprite in self.__scene_game_stack.sprite_group:
            sprite._key_pressed_handler(pressed)