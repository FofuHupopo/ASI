import pygame
import random

from typing import Sequence

from engine.objects import BaseSprite


class TreeSprite(BaseSprite):
    def init(self):
        self.load_image("tree/tree.png")
        self.scale_image((100, 100), coords=(100, 100))
        
        self.is_small = False
    
    def update(self):
        if random.randint(0, 10) > 8:
            self.rect.x += random.randint(-1, 1)
            self.rect.y += random.randint(-1, 1)

    def events_handler(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_small:
                self.scale_image((100, 100))
                
                self.is_small = False
            else:
                self.scale_image((10, 10))
                
                self.is_small = True
                
    def key_pressed_handler(self, pressed: Sequence[bool]):
        if pressed[pygame.K_RIGHT]:
            self.scale_image((self.rect.width + 5, self.rect.height + 5))
        
        if pressed[pygame.K_LEFT]:
            self.scale_image((self.rect.width - 5, self.rect.height - 5))
