import pygame

from engine.objects import BaseObject
from engine.core import EngineEvent


class HPBar(BaseObject):
    def init(self, hp=100, stamina=100):
        self.hp = hp
        self.stamina = stamina
    
    def render(self, surface: pygame.Surface):
        # HP
        hp_bar_lenght = self.hp / 100 * 400

        pygame.draw.rect(
            surface, (255, 80, 80),
            pygame.Rect(150, 560, hp_bar_lenght, 10)
        )
        pygame.draw.rect(
            surface, (0, 0, 0),
            pygame.Rect(149, 559, 401, 11), 1
        )
        pygame.draw.rect(
            surface, (255, 100, 100),
            pygame.Rect(150, 560, 400, 10), 2
        )
        
        font = pygame.font.SysFont('serif', 14, bold=True)
        text_surface = font.render(f"{round(self.hp)} HP", False, "white")
        surface.blit(text_surface, (150 + 400 + 10, 560))
        
        # Stamina
        stamina_bar_lenght = self.stamina / 100 * 200
        stamina_bar_indient = 150 + 400 + 10 + 80

        pygame.draw.rect(
            surface, (255, 180, 180),
            pygame.Rect(stamina_bar_indient, 560, stamina_bar_lenght, 10)
        )
        pygame.draw.rect(
            surface, (0, 0, 0),
            pygame.Rect(stamina_bar_indient - 1, 559, 201, 11), 1
        )
        pygame.draw.rect(
            surface, (255, 200, 100),
            pygame.Rect(stamina_bar_indient, 560, 200, 10), 2
        )
        
        font = pygame.font.SysFont('serif', 14, bold=True)
        text_surface = font.render(f"{round(self.stamina)} E", False, "white")
        surface.blit(text_surface, (stamina_bar_indient + 210, 560))
    
    def update(self) -> None:
        for event in self.get_events():
            if event["type"] == "info" and event["name"] == "hp":
                self.hp = event["data"]["value"]
                # print(self.hp)s
            
            if event["type"] == "info" and event["name"] == "stamina":
                self.stamina = event["data"]["value"]
                # print(self.stamina)
