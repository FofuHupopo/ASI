import pygame

from typing import Tuple, Callable

from engine.objects import BaseSprite


class ButtonSprite(BaseSprite):
    def init(self, image_path, coordinates, size: Tuple[int, int], action, callback: Callable):
        self.load_image(image_path)
        
        self.action = action
        self.rect.x = coordinates[0]
        self.rect.y = coordinates[1]
        self.callback = callback
        self.coordinates = coordinates
        self.is_hover = False

        self.scale_image(size)

    def update(self) -> None:
        ...

    def draw_line(self):
        return {"coord": self.coordinates, "size": self.rect.size}

    def events_handler(self, event: pygame.event.Event):
        pressed = pygame.key.get_pressed()
        pos = pygame.mouse.get_pos()

        if (
            event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and
            self.rect.x <= pos[0] <= self.rect.x + self.rect.width and
            self.rect.y <= pos[1] <= self.rect.y + self.rect.height
        ):
            self.callback()
