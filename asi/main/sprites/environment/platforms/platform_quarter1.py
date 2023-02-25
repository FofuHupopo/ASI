from asi.main.sprites.environment.obstacle import Obstacle


class PlatformCornerFirst(Obstacle):
    def init(self, coords, **kwargs):
        Obstacle.init(self, coords, image=r"map\platforms\platform_corner_1.png")
