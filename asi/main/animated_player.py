import pygame

from engine.objects import AnimatedSprite
from engine.objects.sprite import SpriteTypes


class AimatedPlayerSprite(AnimatedSprite):
    def init(self, coords):
        self.set_type(SpriteTypes.PLAYER)

        self.register_animations(
            {
                "stand": {
                    "path": "player/player_stand.png",
                    "frames": [
                        (7, 4)
                    ],
                    "width": 16,
                    "height": 28
                },
            }
        )

        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.x, self.rect.y = coords
    
    def events_handler(self, event: pygame.event.Event):
        pressed = pygame.key.get_pressed()
        
        if event.type == pygame.KEYDOWN and pressed[pygame.K_f]:
            start
            