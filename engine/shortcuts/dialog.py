import pygame

from typing import Tuple

from engine.objects import BaseObject
from engine.core import EngineSettings


class DialogObject(BaseObject):
    def init(self, text, size: Tuple[int, int]):
        self.__text = text
        self.__size = size
    
    def render(self, surface: pygame.Surface):
        x, y = EngineSettings.get_var("WIDTH") - self.__size[0] - 25, 25

        pygame.draw.rect(
            surface, (255, 255, 255),
            pygame.Rect(
                (x, y),
                self.__size
            ), 1
        )

        font = pygame.font.SysFont('serif', 16, bold=True)
        text_surface = font.render(self.__text, False, "white")
        surface.blit(text_surface, (x + 25, y + 25))
        
        font = pygame.font.SysFont('serif', 13, bold=True)
        text_surface = font.render("Press \"F\" to close this window", False, "white")
        surface.blit(text_surface, (x + 25, y + self.__size[1] - 25))
    
    def update(self) -> None:
        ...
    
    def events_handler(self, event: pygame.event.Event):
        pressed = pygame.key.get_pressed()

        if event.type == pygame.KEYDOWN and pressed[pygame.K_f]:
            self._BaseObject__scene.remove_object(self)