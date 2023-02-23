import pygame

from typing import Tuple

from engine.objects import BaseObject
from engine.core import EngineSettings


class StartDialogObject(BaseObject):
    def init(self, dialog_text, dialog_size):
        self.__text = "F"
        self.__size = (100, 100)

        if isinstance(dialog_text, str):
            dialog_text = [dialog_text]

        self.__dialog_text = dialog_text
        self.__dialog_size = dialog_size
        
        self.__dialog_ind = 0
        self.__dialog_max_ind = len(self.__dialog_text) - 1
        
        self.__opened = False
        self.__readed = False

    def render(self, surface: pygame.Surface):
        if not self.__opened:
            self.__render_help(surface)
            return

        if not self.__readed:
            self.__render_dialog(surface)
            return
    
    def __render_help(self, surface):
        x, y = EngineSettings.get_var("WIDTH") - self.__size[0] - 25, 25

        pygame.draw.rect(
            surface, (255, 255, 255),
            pygame.Rect(
                (x, y),
                self.__size
            ), 2, 3
        )

        font = pygame.font.SysFont('serif', 66, bold=True)

        for ind, text in enumerate(self.__text.split("\n")):
            text_surface = font.render(text, False, "white")
            surface.blit(text_surface, (x + 25, y + 25))
        
    def __render_dialog(self, surface):
        x, y = EngineSettings.get_var("WIDTH") - self.__dialog_size[0] - 25, 25

        pygame.draw.rect(
            surface, (255, 255, 255),
            pygame.Rect(
                (x, y),
                self.__dialog_size
            ), 2, 3
        )
        
        for ind, text in enumerate(self.__dialog_text[self.__dialog_ind].split("\n")):
            font = pygame.font.SysFont('serif', 16, bold=True)
            text_surface = font.render(text, False, "white")
            surface.blit(text_surface, (x + 25, y + 25 + ind * 25))
        
        font = pygame.font.SysFont('serif', 13, bold=True)
        text_surface = font.render("Нажмите \"F\" для продолжения.", False, "white")
        surface.blit(text_surface, (x + 25, y + self.__dialog_size[1] - 25))
    
    def events_handler(self, event: pygame.event.Event):
        pressed = pygame.key.get_pressed()

        if event.type == pygame.KEYDOWN and pressed[pygame.K_f]:
            if self.__opened:
                if self.__dialog_ind == self.__dialog_max_ind:
                    self.__dialog_ind = 0
                    self.__readed = True

                self.__dialog_ind += 1

            self.__opened = True
    
    @property
    def readed(self):
        return self.__readed


class DialogObject(BaseObject):
    def init(self, text: str, size: Tuple[int, int]):
        self.__text = text
        self.__size = size

    def render(self, surface: pygame.Surface):
        x, y = EngineSettings.get_var("WIDTH") - self.__size[0] - 25, 25

        pygame.draw.rect(
            surface, (255, 255, 255),
            pygame.Rect(
                (x, y),
                self.__size
            ), 2, 3
        )

        font = pygame.font.SysFont('serif', 16, bold=True)
        text_surface = font.render(self.__text, False, "white")
        surface.blit(text_surface, (x + 25, y + 25))
        
        font = pygame.font.SysFont('serif', 13, bold=True)
        text_surface = font.render("Нажмите \"F\" для закрытия окна.", False, "white")
        surface.blit(text_surface, (x + 25, y + self.__size[1] - 25))
    
    def update(self) -> None:
        ...
    
    def events_handler(self, event: pygame.event.Event):
        pressed = pygame.key.get_pressed()

        if event.type == pygame.KEYDOWN and pressed[pygame.K_f]:
            self._BaseObject__scene.remove_object(self)
