import pygame
import math

from engine.objects import BaseObject
from engine.core import EngineEvent

from asi.settings import WIDTH, HEIGHT

hp_bar_lenght = int(WIDTH * 0.3)
hp_bar_left_indient = hp_bar_lenght // 2
hp_bar_top_indient = int(HEIGHT * 0.96)
hp_bar_width = 8

class HPBar(BaseObject):
    def init(self, hp=100):
        self.hp = hp
    
    def render(self, surface: pygame.Surface):
        hp_lenght = self.hp / 100 * hp_bar_lenght

        pygame.draw.rect(
            surface, (255, 80, 80),
            pygame.Rect(
                (hp_bar_left_indient, hp_bar_top_indient),
                (hp_lenght, hp_bar_width)
            )
        )
        pygame.draw.rect(
            surface, (0, 0, 0),
            pygame.Rect(
                (hp_bar_left_indient - 1, hp_bar_top_indient - 1),
                (hp_bar_lenght + 1, hp_bar_width + 1)
            ), 1
        )
        pygame.draw.rect(
            surface, (255, 100, 100),
            pygame.Rect(
                (hp_bar_left_indient, hp_bar_top_indient),
                (hp_bar_lenght, hp_bar_width)
            ), 2
        )
        
        # self.__render_circle(surface)

        font = pygame.font.SysFont('serif', 14, bold=True)
        text_surface = font.render(f"{round(self.hp)} HP", False, "white")
        surface.blit(text_surface, (hp_bar_left_indient + hp_bar_lenght + 10, hp_bar_top_indient))
        
    def __render_circle(self, surface):
        pygame.draw.arc(
            surface, (255, 200, 100),
            (850, 450, 100, 100), math.radians(-120), math.radians(30), 6
        )
        
        pygame.draw.arc(
            surface, (0, 0, 0),
            (850, 450, 100, 100), math.radians(-120), math.radians(30), 5
        )
        
        pygame.draw.arc(
            surface, (255, 200, 100),
            (850, 450, 100, 100), math.radians(-120), math.radians(30), 5
        )
    
    def update(self) -> None:
        for event in self.get_events():
            if event["type"] == "info" and event["name"] == "hp":
                self.hp = event["data"]["value"]
                # print(self.hp)


stamina_bar_lenght = int(WIDTH * 0.2)
stamina_bar_left_indient = hp_bar_lenght + hp_bar_left_indient + 80
stamina_bar_top_indient = int(HEIGHT * 0.96)
stamina_bar_width = 8


class StaminaBar(BaseObject):
    def init(self, stamina=100):
        self.stamina = stamina
    
    def render(self, surface: pygame.Surface):
        bar_lenght = self.stamina / 100 * stamina_bar_lenght

        pygame.draw.rect(
            surface, (255, 180, 180),
            pygame.Rect(
                (stamina_bar_left_indient, stamina_bar_top_indient),
                (bar_lenght, stamina_bar_width)
            )
        )
        pygame.draw.rect(
            surface, (0, 0, 0),
            pygame.Rect(
                (stamina_bar_left_indient - 1, stamina_bar_top_indient - 1),
                (stamina_bar_lenght + 1, stamina_bar_width + 1)
            ), 1
        )
        pygame.draw.rect(
            surface, (255, 200, 100),
            pygame.Rect(
                (stamina_bar_left_indient, stamina_bar_top_indient),
                (stamina_bar_lenght, stamina_bar_width)
            ), 2
        )
        
        # self.__render_circle(surface)

        font = pygame.font.SysFont('serif', 14, bold=True)
        text_surface = font.render(f"{round(self.stamina)} E", False, "white")
        surface.blit(text_surface, (stamina_bar_left_indient + stamina_bar_lenght + 10, stamina_bar_top_indient))
        
    def __render_circle(self, surface):
        
        pygame.draw.arc(
            surface, (255, 200, 100),
            (850 - 4, 450 - 4, 100 + 4, 100 + 4), math.radians(-120), math.radians(30), 8
        )
        
        pygame.draw.arc(
            surface, (0, 0, 0),
            (850, 450, 100, 100), math.radians(-120), math.radians(30), 5
        )
        
        pygame.draw.arc(
            surface, (255, 200, 100),
            (850, 450, 100, 100), math.radians(-120), math.radians(-30), 5
        )

    def update(self) -> None:
        for event in self.get_events():
            if event["type"] == "info" and event["name"] == "stamina":
                self.stamina = event["data"]["value"]
                # print(self.stamina)


class MoneyField(BaseObject):
    def init(self, money=0):
        self.money = money
        self.image = pygame.image.load("asi/main/resources/money/money.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
    
    def render(self, surface: pygame.Surface):
        surface.blit(self.image, (20, 20))
        
        font = pygame.font.SysFont('serif', 20, bold=True)
        text_surface = font.render(f"{self.money}", False, "white")
        surface.blit(text_surface, (65, 25))

    def update(self) -> None:
        for event in self.get_events():
            if event["type"] == "info" and event["name"] == "money":
                self.money = event["data"]["value"]
