from asi.main.sprites.environment.obstacle import Obstacle


class PlatformUpper(Obstacle):
    def init(self, coords, **kwargs):
        Obstacle.init(self, coords, image=r"map\platforms\platform_upper.png")
