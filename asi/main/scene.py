import pygame
import random

from engine.objects import BaseScene

from .map import Map, load_level
from .ui import HPBar


class MainScene(BaseScene):
    def init(self) -> None:
        self.map = Map(self)
        self.map.create_map(load_level("map.txt"))
        self.load_object(HPBar)

        # self.player = self.load_sprite(PlayerObject)

    def update(self) -> None:
        pressed = pygame.key.get_pressed()
        self.map.render(self.player.rect.center)

    def events_handler(self, event: pygame.event.Event):
        pressed = pygame.key.get_pressed()

        if event.type == pygame.KEYDOWN and pressed[pygame.K_ESCAPE]:
            self.pause("pause")


class ArtifactsScene(BaseScene):
    def init(self) -> None:
        ...
    
    def update(self) -> None:
        ...
    
    def events_handler(self, event: pygame.event.Event):
        ...
