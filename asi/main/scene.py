import pygame
import random

from engine.objects import BaseScene
from engine.shortcuts.dialog import StartDialogObject
from engine.core import EngineSettings

from asi import settings
from .map import Map, load_level
from .objects.ui import HPBar, StaminaBar, ImageAndTextField


class MainScene(BaseScene):
    def init(self) -> None:
        self.map = Map(self, self._surface)
        
        if EngineSettings.VARIABLES["continue_game"]:
            self.map.load_map_dump(EngineSettings.get_var("DUMP_PATH"))
        else:
            self.map.create_map_2(load_level(EngineSettings.get_var("MAP_NAME")))
            self.map.save_map_dump()

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
        self.load_object(
            ImageAndTextField,
            image_path="asi/main/resources/player/weapons/shuriken.png",
            index=3,
            event_name="shuriken_count"
        )
        
        self.set_stack_sprite_update(False)
        
        self.auto_save_timer_mx = EngineSettings.get_var("FPS") * EngineSettings.get_var("AUTO_SAVE_SECONDS")
        self.auto_save_timer = 0
        self.is_auto_save = True

    def update(self) -> None:
        self.map.update()
        
        if self.is_auto_save:
            self.auto_save_timer += 1

        if self.auto_save_timer >= self.auto_save_timer_mx:
            self.auto_save_timer = 0
            self.map.save_map_dump()
    
    def respawn(self):
        self.set_auto_save(True)
        self.map.load_map_dump(EngineSettings.get_var("DUMP_PATH"))

    def render(self, surface: pygame.Surface):
        ...

    def events_handler(self, event: pygame.event.Event):
        pressed = pygame.key.get_pressed()

        if event.type == pygame.KEYDOWN and pressed[pygame.K_ESCAPE]:
            self.pause("start")
            
        if event.type == pygame.KEYDOWN and pressed[pygame.K_g]:
            self.map.save_map_dump()
    
    def set_auto_save(self, value: bool):
        self.is_auto_save = value

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
