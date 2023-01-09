import pygame
import random

from engine.objects import BaseScene

from .map import Map, load_level


class MainScene(BaseScene):
    def init(self) -> None:
        self.map = Map(self)
        self.map.create_map(load_level("map.txt"))

        # self.player = self.load_sprite(PlayerObject)

    def update(self) -> None:
        pressed = pygame.key.get_pressed()
        self.__prev_player_coords = self.player.rect.center

    def post_update(self) -> None:
        now_player_coords = self.player.rect.center
        
        if now_player_coords != self.__prev_player_coords:
            self.map.render(now_player_coords)

    def events_handler(self, event: pygame.event.Event):
        pressed = pygame.key.get_pressed()

        if event.type == pygame.KEYDOWN and pressed[pygame.K_ESCAPE]:
            self.pause("pause")
