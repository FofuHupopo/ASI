import pygame
import random

from typing import Sequence

from engine.objects import BaseObject


class PlayerObject(BaseObject):
    def init(self):
        self.color = pygame.Color("orange")
        self.start_coords = [-1, -1]
        self.additional_coords = [0, 0]
        
        self.drawing = False
        self.shift_pressed = False

    def render(self, surface: pygame.Surface) -> pygame.Surface:
        pygame.draw.rect(
            surface, pygame.Color(self.color),
            [self.start_coords, self.additional_coords],
            1
        )

    def events_handler(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.start_coords = event.pos
            self.additional_coords = [0, 0]
            self.drawing = True

        if event.type == pygame.MOUSEMOTION and self.drawing:
            self.additional_coords = [
                event.pos[0] - self.start_coords[0],
                event.pos[1] - self.start_coords[1]
            ]

        if event.type == pygame.MOUSEBUTTONUP:
            self.drawing = False
            self.start_coords = [-1, -1]
            self.additional_coords = [0, 0]
    
    def key_pressed_handler(self, pressed: Sequence[bool]):
        self.shift_pressed = pressed[pygame.K_LSHIFT]
