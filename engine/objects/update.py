import pygame

from engine.core.stack import GameStack, SceneGameStack
from . import BaseObject, BaseSprite


def update(
        surface: pygame.Surface, base_color: pygame.Color = pygame.Color("black")
        ) -> pygame.Surface:
    """Функция обновления состояния поверхности.

    Args:
        surface (pygame.Surface): Поверхность.
        base_color (pygame.Color, optional): Базовый цвет поверхности. Обычно черный.

    Returns:
        pygame.Surface: Обновленный кадр.
    """

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


def scene_update(
        surface: pygame.Surface, scene_stack: SceneGameStack,
        base_color: pygame.Color = pygame.Color("black")
        ) -> pygame.Surface:
    """Функция обновления состояния поверхности для сцены.

    Args:
        surface (pygame.Surface): Поверхность.
        
        base_color (pygame.Color, optional): Базовый цвет поверхности. Обычно черный.

    Returns:
        pygame.Surface: Обновленный кадр.
    """
    
    surface.fill(base_color)
    
    for object in scene_stack.object_stack:
        object: BaseObject

        if object._update():
            object._render(surface)

    scene_stack.sprite_group.update()
    scene_stack.sprite_group.draw(surface)
