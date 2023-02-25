from asi.main.sprites.environment.obstacle import Obstacle


class PlatformBlock(Obstacle):
    def init(self, coords, **kwargs):
        Obstacle.init(self, coords, image=r"map\platforms\platform_block.png")
