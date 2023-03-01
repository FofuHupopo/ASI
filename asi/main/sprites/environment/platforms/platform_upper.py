from asi.main.sprites.environment.obstacle import Obstacle
from engine.objects.sprite import SpriteTypes


class PlatformUpper(Obstacle):
    def init(self, coords, **kwargs):
        self.set_type(SpriteTypes.OBSTACLE)
        Obstacle.init(self, coords, image=r"map\platforms\platform_upper.png")
