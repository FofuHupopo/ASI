import pygame
import random

from enum import Enum
from dataclasses import dataclass
from engine.objects import BaseSprite


BASE_ARTEFACTS_STATS = {
    "value": ("hp", "danage", "stamina"),
    "percent": ("hp", "danage", "stamina")
}

TYPES = (
    "head", "necklace", "armor",
    "weapon", "bracelet", "boots"
)


class FiveStarsArtefact:
    def __init__(self) -> None:
        self.__stats = []
        self.__type = random.choice(TYPES)

    def __gen_stats(self):
        self.stats_count = random.randint(4, 6)
        
        for i in range(self.stats_count):
            category = random.choice(BASE_ARTEFACTS_STATS)
            
            coef = random.randint(100, 1000)

            if category == "percent":
                coef /= 100
            
