import random

import pygame
from pathlib import Path

from engine.objects import BaseScene
from engine.core import EngineSettings

from .button_sprite import ButtonSprite
from .objects.loader import LoaderSprite
from asi import settings


def open_image(name):
    image = pygame.image.load(Path(__file__).parent / name)
    return image


def exit_game():
    pygame.quit()
    exit(0)


class StartScene(BaseScene):
    image_background = open_image("ui_start_components/back.jpg")

    def init(self) -> None:
        # self.load_sprite(
        #     LoaderSprite,
        #     coords=(
        #         settings.WIDTH,
        #         settings.HEIGHT
        #     )
        # )

        self.play_button = self.load_sprite(
            ButtonSprite,
            coordinates=(55, 200),
            image_path="start/play.png",
            callback=lambda: print(111),
            type_button="play",
            action="main"
        )

        self.setting_buttons = self.load_sprite(
            ButtonSprite,
            coordinates=(53, 280),
            image_path="start/sett.png",
            callback=lambda: print(222),
            type_button="setting",
            action="settings"
        )

        self.exit_buttons = self.load_sprite(
            ButtonSprite,
            coordinates=(55, 350),
            image_path="start/exit.png",
            callback=lambda: print(333),
            type_button="exit",
            action="exit"
        )
        
        self.__tutorial_finished = False

        self.buttons = [self.play_button, self.setting_buttons, self.exit_buttons]
        self.index_button = 0

    @staticmethod
    def draw_rect_button(surface, data):
        coord, size = data["coord"], data["size"]
        top_left, top, width, height = coord[0] - 8, coord[1] - 4, -10, size[1] + 10
        thickness, corner = 1, 3

        pygame.draw.rect(surface, (230, 230, 230),
                         (top_left, top, width, height), thickness, corner)

    def render(self, surface: pygame.Surface):
        image_background = pygame.transform.scale(StartScene.image_background, settings.SIZE)
        surface.blit(image_background, (0, 0))

        for button in self.buttons:
            if button.is_hover:
                self.draw_rect_button(surface, button.draw_line())

    def update(self) -> None:
        ...
        # self.write("Нажмите 'space' для начала игры", "white", (50, 500), 24)

    def reset_hover(self):
        for button in self.buttons:
            button.is_hover = False

    def pressed_arrows(self, value):
        self.buttons[self.index_button].is_hover = False
        self.index_button = (self.index_button + value) % len(self.buttons)
        self.buttons[self.index_button].is_hover = True

    def events_handler(self, event: pygame.event.Event):
        pressed = pygame.key.get_pressed()

        if event.type == pygame.KEYDOWN:
            if pressed[pygame.K_RETURN]:
                if self.buttons[self.index_button].action == "exit":
                    exit_game()
                elif self.buttons[self.index_button].action == "main":
                    self.__run_main_scene()
                elif self.buttons[self.index_button].action == "settings":
                    self.pause("settings")

            elif pressed[pygame.K_UP]:
                self.pressed_arrows(-1)

            elif pressed[pygame.K_DOWN]:
                self.pressed_arrows(1)

        pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:

            for button in self.buttons:
                if button.rect.collidepoint(pos):
                    if button.action == "exit":
                        exit_game()
                    elif button.action == "main":
                        self.__run_main_scene()
                    elif button.action == "settings":
                        self.pause("settings")

        if event.type == pygame.MOUSEMOTION:
            for i, button in enumerate(self.buttons):
                if (button.rect.x <= pos[0] <= button.rect.x + button.rect.width) and \
                        (button.rect.y <= pos[1] <= button.rect.y + button.rect.height):
                    self.buttons[self.index_button].is_hover = False
                    self.index_button = i
                    button.is_hover = True
                    
    def __run_main_scene(self):
        if self.__tutorial_finished:
            self.pause("main")
        else:
            self.__tutorial_finished = True
            self.pause("tutorial")

    def key_pressed_handler(self, pressed):
        ...


class PauseScene(BaseScene):
    def init(self) -> None:
        ...

    def render(self, surface: pygame.Surface):
        ...
        
    def update(self) -> None:
        self.write("ПАУЗА", "red", (50, 50), 48)
        self.write("Нажмите 'space' или 'esc' для возобновления игры", "red", (50, 500), 24)

    def events_handler(self, event: pygame.event.Event):
        pressed = pygame.key.get_pressed()

        if event.type == pygame.KEYDOWN and (pressed[pygame.K_SPACE] or pressed[pygame.K_ESCAPE]):
            self.pause("main")


class TutorialScene(BaseScene):
    def init(self) -> None:
        self.__tutorial_page = 1
        self.__max_tutorial_page = 4

    def render(self, surface: pygame.Surface):
        ...
        
    def update(self) -> None:
        if self.__tutorial_page == 1:
            self.write("Сюрикен опасен лишь когда летит прямо,", "green", (50, 50), 48)
            self.write("чем сильнее он падает, тем меньше он ", "green", (50, 100), 48)
            self.write("наносит урона. ", "green", (50, 150), 48)
        if self.__tutorial_page == 2:
            self.write("Используйте клавишу SHIFT при движении,", "green", (50, 50), 48)
            self.write("чтобы двигаться быстрее. Но помните, энергия ", "green", (50, 100), 48)
            self.write("быстро заканчивается и долго восстанавливается,", "green", (50, 150), 48)
            self.write("поэтому не тратьте её зря, чтобы не остаться ", "green", (50, 200), 48)
            self.write("без неё в критической ситуации.", "green", (50, 250), 48)
        if self.__tutorial_page == 3:
            self.write("Чем выше ты взлетаешь, тем больнее будет", "green", (50, 50), 48)
            self.write("приземление.", "green", (50, 100), 48)
        if self.__tutorial_page == 4:
            self.write("Если у вас не получается победить врага,", "green", (50, 50), 48)
            self.write("не расстраивайтесь, пробуйте разные тактики и", "green", (50, 100), 48)
            self.write("разный подход, умирайте и пробуйте ещё раз", "green", (50, 150), 48)
            self.write("сразиться с ним, и когда ни будь вы его одолеете.", "green", (50, 200), 48)
        y = settings.HEIGHT - 40
        x = settings.WIDTH - 180
        
        self.write(f"Страница {self.__tutorial_page} из {self.__max_tutorial_page}", "white", (x, y), 24)
        self.write(f"Используйте <- и -> для перемещения по страницам туториала", "white", (40, y), 24)

    def events_handler(self, event: pygame.event.Event):
        pressed = pygame.key.get_pressed()

        if (event.type == pygame.KEYDOWN and pressed[pygame.K_RIGHT]):
            self.__tutorial_page += 1
            
            if self.__tutorial_page > self.__max_tutorial_page:
                self.__tutorial_page = self.__max_tutorial_page
                self.stop("main")
        
        if (event.type == pygame.KEYDOWN and pressed[pygame.K_LEFT]):
            self.__tutorial_page = max(self.__tutorial_page - 1, 1)


class SettingsScene(BaseScene):
    def init(self) -> None:
        ...

    def render(self, surface: pygame.Surface):
        pygame.draw.rect(
            surface, "white",
            pygame.Rect(100, 100, 150, 50), 1
        )
        pygame.draw.rect(
            surface, "blue" if settings.DRAW_ANIMATIONS else "red",
            pygame.Rect(101, 101, 148, 48)
        )
        self.write("Анимации", "white", (110, 110), 24)
        
        pygame.draw.rect(
            surface, "white",
            pygame.Rect(100, 200, 150, 50), 1
        )
        pygame.draw.rect(
            surface, "blue" if settings.PLAY_SOUNDS else "red",
            pygame.Rect(101, 201, 148, 48)
        )
        self.write("Музыка", "white", (110, 210), 24)
        
    def update(self) -> None:
        self.write("Настройки: ", "white", (50, 50), 48)

    def events_handler(self, event: pygame.event.Event):
        pressed = pygame.key.get_pressed()

        if event.type == pygame.KEYDOWN and (pressed[pygame.K_SPACE] or pressed[pygame.K_ESCAPE]):
            self.stop("start")

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if (
                100 <= event.pos[0] <= 250 and
                100 <= event.pos[1] <= 150
            ):
                change_to = not settings.DRAW_ANIMATIONS
                settings.DRAW_ANIMATIONS = change_to
                EngineSettings.DEFAULT_VARIABLES["DRAW_ANIMATIONS"] = change_to
                EngineSettings.VARIABLES["DRAW_ANIMATIONS"] = change_to
                
            if (
                100 <= event.pos[0] <= 250 and
                200 <= event.pos[1] <= 250
            ):
                change_to = not settings.PLAY_SOUNDS
                settings.PLAY_SOUNDS = change_to
                EngineSettings.DEFAULT_VARIABLES["PLAY_SOUNDS"] = change_to
                EngineSettings.VARIABLES["PLAY_SOUNDS"] = change_to
