import pygame


class GameStack:
    stack = []
    sprite_group = pygame.sprite.Group()

    @staticmethod
    def append_stack(item):
        GameStack.stack.insert(-1, item)

    @staticmethod
    def get_stack():
        return GameStack.stack

    @staticmethod
    def pop_stack(index: int):
        return GameStack.stack.pop(index)

    @staticmethod
    def add_sprite_group(sprite):
        GameStack.sprite_group.add(sprite)
    
    @staticmethod
    def get_sprite_group():
        return GameStack.sprite_group
    
    @staticmethod
    def pop_stack_group(sprite):
        GameStack.sprite_group.remove(sprite)
        

class SceneGameStack:
    def __init__(self) -> None:
        self.__object_stack = []
        self.__sprite_group = pygame.sprite.Group()

    @property
    def object_stack(self):
        return self.__object_stack

    @property
    def sprite_group(self):
        return self.__sprite_group
