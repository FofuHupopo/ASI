from time import sleep

from engine.core import EngineSettings, Game
from .start.scene import StartScene
from .main.scene import MainScene

from . import settings


class App:
    def run(self):
        self.__run_game()

    def __run_game(self):
        EngineSettings.load_file(settings)

        game = Game({
            "start": StartScene
        })

        game.set_start_scene("start")
        game.run()

        game.close()
