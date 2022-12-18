import pygame


class GameStack:
    stack = []
    sprite_group = pygame.sprite.Group()

    @staticmethod
    def append_stack(item):
        GameStack.stack.append(item)

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
