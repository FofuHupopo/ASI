import pygame

from .stack import GameStack
from engine.objects import BaseObject, BaseSprite


def update(surface: pygame.Surface, base_color: pygame.Color = pygame.Color("black")):
    surface.fill(base_color)

    for object in GameStack.get_stack():
        object: BaseObject

        if object._update():
            object._render(surface)
            
    for sprite in GameStack.get_sprite_group().sprites():
        sprite: BaseSprite
        
        sprite._update()

    GameStack.get_sprite_group().draw(surface)
    GameStack.get_sprite_group().update()

    return surface
