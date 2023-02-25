from asi.main.sprites.environment.obstacle import Obstacle


class PlatformCornerThird(Obstacle):
    def init(self, coords, **kwargs):
        Obstacle.init(self, coords, image=r"map\platforms\platform_corner_3.png")
