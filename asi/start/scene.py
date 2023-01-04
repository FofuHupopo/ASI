import pygame

from engine.objects import BaseScene

from .objects.loader import LoaderSprite


class StartScene(BaseScene):
    def init(self) -> None:
        self.load_sprite(LoaderSprite)
    
    def render(self, surface: pygame.Surface):
        pygame.draw.rect(
            surface, "white",
            pygame.Rect((50, 50), (100, 100))
        )
    
    def update(self) -> None:
        ...

    def events_handler(self, event: pygame.event.Event):
        pressed = pygame.key.get_pressed()
        
        if event.type == pygame.KEYUP and pressed[pygame.K_SPACE]:
            self.stop()
