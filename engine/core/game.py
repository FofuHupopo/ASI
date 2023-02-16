import pygame

from .global_data import Resources
from .settings import EngineSettings


class Game:
    def __init__(self, scenes: dict = {}) -> None:
        if type(scenes) is not dict:
            raise ValueError("Сцены передаются не словарем")
        
        Resources.load()

        self.__scenes = scenes
        self.__current_scene_name = None

        self.__next_scene = None
        self.__stop_prev = False

        self.__pygame_init()

    def __del__(self):
        self.__terminate()

    def add_scene(self, scene_name: str, scene) -> None:
        self.__scenes[scene_name] = scene
    
    @property
    def scenes(self):
        return self.__scenes
    
    def del_scene(self, scene_name: str):
        if scene_name in self.__scenes:
            scene = self.__scenes[scene_name]
            del self.__scenes[scene_name]
            
            self.__scenes[scene_name] = scene.__class__
            self.__current_scene_name = None
            
            
    def set_start_scene(self, scene_name):
        self.__next_scene = scene_name

    def run(self):
        while True:
            self.__next_scene, self.__stop_prev = self.__run_scene()
            
            if not self.__next_scene:
                break

    def __run_scene(self, stop_current=False) -> None:
        """Запуск сцены

        Args:
            scene_name (str): Название сцены.

        Raises:
            ValueError: Ошибка с названием сцены.
        """

        if self.__next_scene not in self.__scenes:
            raise ValueError(f"Сцена с названием {self.__next_scene} отсутствует.")

        if self.__current_scene_name:
            if stop_current:
                self.current_scene.stop()
            else:
                self.current_scene.pause()

        self.__current_scene_name = self.__next_scene

        if type(self.current_scene) is type:
            self.__scenes[self.__current_scene_name] = self.current_scene(
                self, self.__current_scene_name
            )

        return self.current_scene.run()

    @property
    def current_scene(self):
        return self.__scenes[self.__current_scene_name]

    def close(self):
        """Остановка игры
        """

        self.__terminate()

    def __pygame_init(self):
        pygame.init()
        
        pygame.display.set_caption(EngineSettings.get_var("WINDOW_NAME"))
        
        if pygame.joystick.get_count():
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

    def __terminate(self):
        pygame.quit()

        if self.__current_scene_name:
            self.current_scene.stop()
