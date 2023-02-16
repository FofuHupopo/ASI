from engine.core import EngineSettings, Game
from .start.scene import StartScene, PauseScene, TutorialScene
from .main.scene import MainScene, ArtifactsScene

from . import settings


class App:
    def run(self):
        self.__run_game()

    def __run_game(self):
        EngineSettings.load_file(settings)

        game = Game({
            "main": MainScene,
            "pause": PauseScene,
            "start": StartScene,
            "artifacts": ArtifactsScene,
            "tutorial": TutorialScene,
        })

        game.set_start_scene("main")

        game.run()

        game.close()
