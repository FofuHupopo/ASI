import pygame

from engine.objects import BaseScene

from .objects.loader import LoaderSprite
from asi import settings


class StartScene(BaseScene):
    def init(self) -> None:
        self.load_sprite(
            LoaderSprite,
            coords=(
                settings.WIDTH,
                settings.HEIGHT
            )
        )

    def render(self, surface: pygame.Surface):
        ...

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
