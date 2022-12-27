import pygame
import random

from typing import Sequence

from engine.objects import BaseObject


class PlayerObject(BaseObject):
    def init(self):
        self.color = pygame.Color("orange")
        self.coords = [500, 250]
        self.wh = (50, 100)
        self.speed_x = 0
        self.speed_y = 0
        self.time_y = 0
        self.fly = False

    def render(self, surface: pygame.Surface) -> pygame.Surface:

        self.coords[0] -= self.speed_x
        if self.fly:
            self.coords[1] -= self.speed_y
            self.speed_y -= self.time_y
            self.time_y += 10 * 0.001
        pygame.draw.rect(
            surface, pygame.Color(self.color),
            [self.coords, self.wh],
            0
        )

    def events_handler(self, event: pygame.event.Event):
        keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN and keys[pygame.K_SPACE] and not self.fly:
            self.speed_y = 5
            self.fly = True

    def key_pressed_handler(self, pressed: Sequence[bool]):
        if pressed[pygame.K_a]:
            self.speed_x = 3
        elif pressed[pygame.K_d]:
            self.speed_x = -3
        else:
            self.speed_x = 0
