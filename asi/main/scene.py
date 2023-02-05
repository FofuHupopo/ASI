import pygame
import random

from engine.objects import BaseScene
from engine.shortcuts.dialog import DialogObject

from asi import settings
from .map import Map, load_level
from .ui import HPBar, StaminaBar, ImageAndTextField


class MainScene(BaseScene):
    def init(self) -> None:
        self.map = Map(self)
        self.map.create_map(load_level("map.txt"))
        
        self.background = pygame.image.load("asi/main/resources/background.png")
        # self.background = pygame.transform.scale2x(self.background)
        
        self.load_object(HPBar)
        self.load_object(StaminaBar)

        self.load_object(
            ImageAndTextField,
            image_path="asi/main/resources/money/money.png",
            index=0,
            event_name="money"
        )
        self.load_object(
            ImageAndTextField,
            image_path="asi/main/resources/heal/little_heal.png",
            index=1,
            event_name="little_heal"
        )
        self.load_object(
            ImageAndTextField,
            image_path="asi/main/resources/heal/big_heal.png",
            index=2,
            event_name="big_heal"
        )


        # self.player = self.load_sprite(PlayerObject)

    def update(self) -> None:
        self.map.render(self.player.rect.center)
    
    def render(self, surface: pygame.Surface):
        surface.blit(self.background, (0, 0))

    def events_handler(self, event: pygame.event.Event):
        pressed = pygame.key.get_pressed()

        if event.type == pygame.KEYDOWN and pressed[pygame.K_ESCAPE]:
            self.pause("start")

        if event.type == pygame.KEYDOWN and pressed[pygame.K_b]:
            self.load_object(DialogObject, text="Это какой-то текст в диалоговом окне", size=(500, 200))

    def key_pressed_handler(self, pressed):
        if pressed[pygame.K_UP]:
            self.map.move_map((0, 10))
        if pressed[pygame.K_DOWN]:
            self.map.move_map((0, -10))

        if pressed[pygame.K_RIGHT]:
            self.map.move_map((-10, 0))
        if pressed[pygame.K_LEFT]:
            self.map.move_map((10, 0))


class ArtifactsScene(BaseScene):
    def init(self) -> None:
        ...
    
    def update(self) -> None:
        ...
    
    def events_handler(self, event: pygame.event.Event):
        ...
