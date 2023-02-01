import pygame
from pathlib import Path

from engine.objects import BaseScene

from .button_sprite import ButtonSprite
from .objects.loader import LoaderSprite
from asi import settings


def open_image(name):
    image = pygame.image.load(Path(__file__).parent / name)
    return image


class StartScene(BaseScene):
    image_background = open_image("ui_start_components/back.jpg")
    # image_exit = open_image("ui_start_components/exit.png")
    # image_play = open_image("ui_start_components/play.png")
    # image_sett = open_image("ui_start_components/sett.png")

    def init(self) -> None:
        self.load_sprite(
            LoaderSprite,
            coords=(
                settings.WIDTH,
                settings.HEIGHT
            )
        )
        self.load_sprite(
            ButtonSprite,
            coordinates=(55, 200),
            image_path="start/play.png",
            callback=lambda: print(111),
            type_button="play"
        )
        self.load_sprite(
            ButtonSprite,
            coordinates=(55, 280),
            image_path="start/sett.png",
            callback=lambda: print(222),
            type_button="setting"
        )
        self.load_sprite(
            ButtonSprite,
            coordinates=(55, 350),
            image_path="start/exit.png",
            callback=lambda: print(333),
            type_button="exit"
        )

    def render(self, surface: pygame.Surface):
        surface.blit(StartScene.image_background, (0, 0))
        # surface.blit(StartScene.image_play, (50, 100))
        # surface.blit(StartScene.image_exit, (50, 300))
        # surface.blit(StartScene.image_sett, (50, 450))

    def update(self) -> None:
        self.write("Нажмите 'space' для начала игры", "white", (50, 500), 24)

    def events_handler(self, event: pygame.event.Event):
        pressed = pygame.key.get_pressed()

        if event.type == pygame.KEYDOWN and pressed[pygame.K_SPACE]:
            self.stop("main")

    def key_pressed_handler(self, pressed):
        ...


class PauseScene(BaseScene):
    def init(self) -> None:
        ...

    def render(self, surface: pygame.Surface):
        ...
        
    def update(self) -> None:
        self.write("ПАУЗА", "red", (50, 50), 48)
        self.write("Нажмите 'space' или 'esc' для возобновления игры", "red", (50, 500), 24)

    def events_handler(self, event: pygame.event.Event):
        pressed = pygame.key.get_pressed()

        if event.type == pygame.KEYDOWN and (pressed[pygame.K_SPACE] or pressed[pygame.K_ESCAPE]):
            self.pause("main")


class DieScene(BaseScene):
    ...
