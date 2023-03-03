from engine.core import EngineSettings, Game

from . import settings
from .start.scene import StartScene, PauseScene, TutorialScene, SettingsScene
from .main.scene import MainScene, ArtifactsScene


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
            "settings": SettingsScene,
        })

        game.set_start_scene("start")
        game.run()

        game.close()
