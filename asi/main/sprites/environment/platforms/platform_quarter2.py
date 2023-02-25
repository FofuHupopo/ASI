from asi.main.sprites.environment.obstacle import Obstacle


class PlatformCornerSecond(Obstacle):
    def init(self, coords, **kwargs):
        Obstacle.init(self, coords, image=r"map\platforms\platform_corner_2.png")
