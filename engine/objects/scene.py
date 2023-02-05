import pygame

from typing import Sequence

from engine.objects.update import scene_update
from engine.core.event_handler import SceneEventHandler
from engine.core.events import EngineEvents
from engine.core.stack import SceneGameStack
from engine.core.settings import EngineSettings


class BaseScene:
    def __init__(self, game, scene_name) -> None:
        self.__running = True
        self.__frozen = False
        self.__next_scene = None
        
        self.__game = game
        self.__scene_name = scene_name
        
        self._game_stack = SceneGameStack()        
        self.__event_handler = SceneEventHandler(self._game_stack)
        self.__events = EngineEvents()
        
        self.__load_pygame_vars()
        self.init()

    def init(self) -> None: ...
    
    def update(self) -> None: ...
    
    def post_update(self) -> None: ...
    
    def __update(self):
        self.update()

    def __load_pygame_vars(self):
        self.__size = EngineSettings.get_var("SIZE")
        self.__clock = pygame.time.Clock()
        self.__fps = EngineSettings.get_var("FPS")
        self.__background_color = pygame.Color(EngineSettings.get_var("BACKGROUND_COLOR"))

        self._surface = pygame.display.set_mode(self.__size)
        self._surface.fill(self.__background_color)
        
        pygame.display.flip()
        
    def add_event(self, event):
        self.__events.add_event(event)
    
    def get_events(self):
        return self.__events.get_events()

    def run(self):
        self.__frozen = False
        self.__mainloop()
        
        return self.__next_scene, self.__frozen

    def stop(self, next_scene=None):
        """Остановка сцены.
        """

        self.__running = False
        self.__next_scene = next_scene
    
        self.__game.del_scene(self.__scene_name)

    def pause(self, next_scene=None):
        """Пауза сцены.
        """

        self.__frozen = True
        self.__next_scene = next_scene

    def load_object(self, object_class, **kwargs):
        object = object_class(scene=self, **kwargs)
        self._game_stack.object_stack.append(object)
        
        return object

    def load_sprite(self, sprite_class, **kwargs):
        sprite = sprite_class(scene=self, scene_update=True, **kwargs)
        self._game_stack.sprite_group.add(sprite)

        return sprite

    def remove_object(self, object):
        if object in self._game_stack.object_stack:
            self._game_stack.object_stack.remove(object)
    
    def remove_sprite(self, sprite):
        self._game_stack.sprite_group.remove(sprite)
        sprite.kill()
    
    def move_all_sprites(self, coords):
        for sprite in self._game_stack.sprite_group.sprites():
            sprite.rect.x += coords[0]
            sprite.rect.y += coords[1]
            
    def write(self, text: str, color="white", coords=(0, 0), font_size=48):
        font = pygame.font.SysFont('serif', font_size)
        text_surface = font.render(text, False, color)
        self._surface.blit(text_surface, coords)

    def find_sprites(self, sprite_type):
        sprites = []

        for sprite in self._game_stack.sprite_group.sprites():
            if sprite.get_type() == sprite_type:
                sprites.append(sprite)
        
        return sprites
    
    @property
    def sprite_group(self):
        return self._game_stack.sprite_group

    def __mainloop(self):
        while self.__running and not self.__frozen:
            self.__events_handler()
            self.__pressed_handler()

            self._surface.fill("black")
            self.__update()

            self.__render()
            scene_update(self._surface, self._game_stack, self.__background_color)
            
            self.post_update()
            self.__events.clear_events()

            pygame.display.flip()
            self.__clock.tick(self.__fps)
    
    def __render(self):
        self.render(self._surface)

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

    def key_pressed_handler(self, pressed: Sequence): ...
    
    def render(self, surface: pygame.Surface): ...
