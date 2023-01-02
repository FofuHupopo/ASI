import pygame

from engine.objects.update import scene_update
from engine.core.event_handler import  SceneEventHandler
from engine.core.stack import SceneGameStack
from engine.core.settings import EngineSettings


class BaseScene:
    def __init__(self) -> None:
        self.__running = True
        self.__game_stack = SceneGameStack()

        self.__event_handler = SceneEventHandler(self.__game_stack)
        self.__load_pygame_vars()

        self.init()

    def init(self) -> None: ...
    
    def update(self) -> None: ...
    
    def __update(self):
        self.update()

    def __load_pygame_vars(self):
        self.__size = EngineSettings.get_var("SIZE")
        self.__clock = pygame.time.Clock()
        self.__fps = EngineSettings.get_var("FPS")
        self.__background_color = pygame.Color(EngineSettings.get_var("BACKGROUND_COLOR"))

        self.__screen = pygame.display.set_mode(self.__size)
        self.__screen.fill(self.__background_color)
        
        pygame.display.flip()
        
    def run(self):
        self.__mainloop()

    def stop(self):
        """Метод остановки сцены.
        """
        self.__running = False
    
    def pause(self):
        """Методы паузы сцены.
        """
        self.__running = False

    def load_object(self, object):
        self.__game_stack.object_stack.append(object(scene=self))

    def load_sprite(self, sprite_class, **kwargs):
        self.__game_stack.sprite_group.add(sprite_class(scene=self, **kwargs))
    
    @property
    def sprite_group(self):
        return self.__game_stack.sprite_group

    def __mainloop(self):
        while self.__running:
            self.__events_handler()
            self.__pressed_handler()

            self.__update()
            scene_update(self.__screen, self.__game_stack, self.__background_color)

            pygame.display.flip()
            self.__clock.tick(self.__fps)

    def __events_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()

            self.__event_handler.event(event)
            self.events_handler(event)
    
    def __pressed_handler(self):
        pressed = pygame.key.get_pressed()
        
        self.__event_handler.key_pressed(pressed)
        self.key_pressed_handler(pressed)
        
    def events_handler(self, event: pygame.event.Event): ...

    def key_pressed_handler(self, pressed): ...
