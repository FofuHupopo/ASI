from asi.main.sprites.environment.obstacle import Obstacle
from engine.objects.sprite import SpriteTypes


class PlatformRight(Obstacle):
    def init(self, coords, **kwargs):
        self.set_type(SpriteTypes.OBSTACLE)
        Obstacle.init(self, coords, image="map/platforms/platform_right.png")
