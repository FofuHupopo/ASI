import pygame

from typing import Sequence

from asi import settings
from .throwing_arms import Arms
from .player import PlayerSprite
from .obstacle import Obstacle
from .storage import Storage
from .trader import Trader
from .kamikaze import Kamikaze


def load_level(filename):  # загрузка уровня
    filename = r"asi/main/resources/map/" + filename

    with open(filename, "r") as mapFile:
        level_map = [line for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: list(x.ljust(max_width, ".")), level_map))  # возвращаем список списков карты


class Map:
    SYMBOL_DECODER = {
        "#": Obstacle,
        "-": Obstacle,
        "$": Storage,
        "t": Trader,
        "k": Kamikaze
    }

    def __init__(self, scene):
        self.__sprite_group = pygame.sprite.Group()
        self.__scene = scene

        self.block_size = 50

    def create_map(self, level_map):
        player_pos = self.__preload_player(level_map)
        offset = [
            player_pos[0] - 10,
            player_pos[0] - 16,
        ]

        for y in range(len(level_map)):
            for x in range(len(level_map[y])):
                symbol = level_map[y][x]
                
                if symbol in Map.SYMBOL_DECODER:
                    self.add_game_object(
                        Map.SYMBOL_DECODER[symbol],
                        [self.block_size * (x - offset[0]), self.block_size * (y - offset[1])]
                    )
                    
                if level_map[y][x] == "p":
                    self.__scene.player = self.__scene.load_sprite(PlayerSprite, coords=[self.block_size * (x - offset[0]), self.block_size * (y - offset[1])])

    def __preload_player(self, level_map):
        for y in range(len(level_map)):
            for x in range(len(level_map[y])):
                if level_map[y][x] == "p":
                    return (x, y)

        raise ValueError("Игрок не обнаружен на карте")
        
    def add_game_object(self, sprite_class, coords):
        sprite = sprite_class(self.__scene, coords=coords)
        self.__sprite_group.add(sprite)
        self.__scene._game_stack.sprite_group.add(sprite)
    
    def render(self, player_coords):
        self.__move_map_for_player(player_coords)

    def __move_map_for_player(self, player_coords):
        if (
            settings.WIDTH * 20 / 100 >= player_coords[0] or
            player_coords[0] >= settings.WIDTH * 80 / 100 or
            settings.HEIGHT * 20 / 100 >= player_coords[1] or
            player_coords[1] >= settings.HEIGHT * 80 / 100
            ):

            x, y = 0, 0

            if settings.WIDTH * 20 / 100 >= player_coords[0]:
                x = settings.WIDTH * 20 / 100 - player_coords[0]
            elif player_coords[0] >= settings.WIDTH * 80 / 100:
                x = settings.WIDTH * 80 / 100 - player_coords[0]
                
            if settings.HEIGHT * 20 / 100 >= player_coords[1]:
                y = settings.HEIGHT * 20 / 100 - player_coords[1]
            elif player_coords[1] >= settings.HEIGHT * 80 / 100:
                y = settings.HEIGHT * 80 / 100 - player_coords[1]
            
            self.move_map((x, y))

    def move_map(self, coords):
        x, y = coords

        self.__scene.move_all_sprites((x, y))

        self.__sprite_group.update()
        self.__sprite_group.draw(self.__scene._surface)
