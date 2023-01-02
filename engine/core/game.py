import pygame

# from engine.core import WorldVariables
from .settings import EngineSettings


class Game:
    def __init__(self, scenes: dict = {}) -> None:
        if type(scenes) is not dict:
            raise ValueError("Сцены передаются не словарем")

        self.__scenes = scenes
        self.__current_scene_name = None
        # WorldVariables.game = self

        self.__pygame_init()

    def __del__(self):
        self.__terminate()

    def add_scene(self, scene_name: str, scene) -> None:
        self.__scenes[scene_name] = scene
        
    def run_scene(self, scene_name: str) -> None:
        """Запуск сцены

        Args:
            scene_name (str): Название сцены.

        Raises:
            ValueError: Ошибка с названием сцены.
        """

        if scene_name not in self.__scenes:
            raise ValueError(f"Сцена с названием {scene_name} отсутствует.")
        
        if self.__current_scene_name:
            self.current_scene.stop()
        
        self.__current_scene_name = scene_name
        self.__scenes[scene_name].run()
                
    @property
    def current_scene(self):
        return self.__scenes[self.__current_scene_name]

    # def start(self):
    #     """Запуск игры

    #     Raises:
    #         ValueError: _description_
    #         Exception: _description_
    #     """
    #     if not self.__scenes:
    #         raise ValueError("Сцены не зарегистрированы")
        
    #     if len(self.__scenes) <= self.__scene_index:
    #         raise Exception("сцены закончились")

    #     self.__current_scene = self.__scenes[self.__scene_index]()
    #     self.__current_scene.run()
        
    #     self.next()

    def close(self):
        """Остановка игры
        """

        self.__terminate()

    def __pygame_init(self):
        pygame.init()

        pygame.display.set_caption(EngineSettings.get_var("WINDOW_NAME"))

    def __terminate(self):
        pygame.quit()
