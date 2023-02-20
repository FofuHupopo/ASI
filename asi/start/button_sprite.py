import pygame

from typing import Tuple, Callable

from engine.objects import BaseSprite
from engine.core import EngineEvent

from asi import settings


class ButtonSprite(BaseSprite):
    def init(self, image_path, type_button, coordinates, action,  callback: Callable, **kwargs):
        self.load_image(image_path)
        
        self.action = action
        self.rect.x = coordinates[0]
        self.rect.y = coordinates[1]
        self.coordinates = coordinates
        self.callback = callback
        self.type_button = type_button
        self.is_hover = False

    def change_size_image(self):  # изменить размер картинки кнопки
        if self.type_button == "play":
            self.scale_image((190, 66))
        elif self.type_button == "setting":
            self.scale_image((400, 66))
        else:
            self.scale_image((170, 66))

    def update(self) -> None:
        self.change_size_image()

    def draw_line(self):
        # self.add_event(EngineEvent("menu_action", "mouse_draw_line", {"coord": coord, "size": size}))
        return {"coord": self.coordinates, "size": self.rect.size}

    def events_handler(self, event: pygame.event.Event):
        pressed = pygame.key.get_pressed()
        pos = pygame.mouse.get_pos()

        # if (self.rect.x <= pos[0] <= self.rect.x + self.rect.width) and\
        #         (self.rect.y <= pos[1] <= self.rect.y + self.rect.height):
        #     self.is_hover = True
        # else:
        #     self.is_hover = False
