import pygame

from typing import Tuple, Callable

from engine.objects import BaseSprite


class ButtonSprite(BaseSprite):
    def init(self, image_path, type_button, coordinates,  callback: Callable, **kwargs):
        self.load_image(image_path)

        self.rect.x = coordinates[0]
        self.rect.y = coordinates[1]
        self.coordinates = coordinates
        self.callback = callback
        self.type_button = type_button

    def change_size_image(self):  # изменить размер картинки кнопки
        if self.type_button == "play":
            self.scale_image((110, 35))
        elif self.type_button == "setting":
            self.scale_image((220, 35))
        else:
            self.scale_image((100, 35))

    def update(self) -> None:
        self.change_size_image()

    def draw_line(self, coord, size):
        ...
        # pygame.draw.line((255, 255, 255), coord, (coord[0] + size[0], coord[1] + size[1]))

    def events_handler(self, event: pygame.event.Event):
        pressed = pygame.key.get_pressed()

        if event.type == pygame.MOUSEMOTION:
            pos = event.pos
            if (self.rect.x <= pos[0] <= self.rect.x + self.rect.width) and\
                    (self.rect.y <= pos[1] <= self.rect.y + self.rect.height):
                self.draw_line(self.rect.topleft, self.rect.size)
