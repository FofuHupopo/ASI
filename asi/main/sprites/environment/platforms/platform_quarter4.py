from asi.main.sprites.environment.obstacle import Obstacle


class PlatformCornerFourth(Obstacle):
    def init(self, coords, **kwargs):
        Obstacle.init(self, coords, image=r"map\platforms\platform_corner_4.png")
