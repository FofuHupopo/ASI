from asi.main.sprites.environment.obstacle import Obstacle


class PlatformHorizontally(Obstacle):
    def init(self, coords, **kwargs):
        Obstacle.init(self, coords, image=r"map\platforms\platform.png")
