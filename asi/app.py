import pygame

from engine.core import update, EventHandler
from .objects import load_objects
from . import settings


class App:
    def run(self):
        self.run_game()

    def run_game(self):
        pygame.init()

        size = settings.SIZE

        screen = pygame.display.set_mode(size)
        screen.fill(pygame.Color("black"))

        pygame.display.set_caption(settings.WINDOW_NAME)
        pygame.display.flip()
        
        event_handler = EventHandler()
        load_objects()

        clock = pygame.time.Clock()
        fps = settings.FPS

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                event_handler.event(event)
                
            pressed = pygame.key.get_pressed()
            event_handler.key_pressed(pressed)

            update(screen, settings.BACKGROUND_COLOR)

            pygame.display.flip()
            clock.tick(fps)

        pygame.quit()
