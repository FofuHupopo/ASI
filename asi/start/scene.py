import pygame
from pathlib import Path

from engine.objects import BaseScene
from engine.core import EngineSettings

from .sprites.button_sprite import ButtonSprite
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
        self.play_button = self.load_sprite(
            ButtonSprite,
            coordinates=(55, 200),
            size=(190, 66),
            image_path="start/play.png",
            action="main",
            callback=lambda: self.__run_main_scene(),
        )

        self.setting_buttons = self.load_sprite(
            ButtonSprite,
            coordinates=(55, 320),
            size=(400, 66),
            image_path="start/sett.png",
            action="settings",
            callback=lambda: self.pause("settings"),
        )

        self.exit_buttons = self.load_sprite(
            ButtonSprite,
            coordinates=(55, 440),
            size=(170, 66),
            image_path="start/exit.png",
            action="exit",
            callback=lambda: exit_game(),
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
                self.buttons[self.index_button].callback()                    

            elif pressed[pygame.K_UP]:
                self.pressed_arrows(-1)

            elif pressed[pygame.K_DOWN]:
                self.pressed_arrows(1)

        pos = pygame.mouse.get_pos()

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
        
        self.__main_color = pygame.Color("#FB2576")
        self.__background_color = "#20262E"

    def render(self, surface: pygame.Surface):
        width, height = EngineSettings.get_var("SIZE")
        
        surface.fill(self.__background_color)

        if self.__tutorial_page == 1:
            self.write("Сюрикен опасен лишь когда летит прямо,", self.__main_color, (50, 50), 48)
            self.write("чем сильнее он падает, тем меньше он ", self.__main_color, (50, 100), 48)
            self.write("наносит урона. ", self.__main_color, (50, 150), 48)
        if self.__tutorial_page == 2:
            self.write("Используйте клавишу SHIFT при движении,", self.__main_color, (50, 50), 48)
            self.write("чтобы двигаться быстрее. Но помните, ", self.__main_color, (50, 100), 48)
            self.write("энергия быстро заканчивается и долго,", self.__main_color, (50, 150), 48)
            self.write("восстанавливается поэтому не тратьте ", self.__main_color, (50, 200), 48)
            self.write("её зря, чтобы не остаться без неё в ", self.__main_color, (50, 250), 48)
            self.write("критической ситуации. ", self.__main_color, (50, 300), 48)
        if self.__tutorial_page == 3:
            self.write("Чем выше ты взлетаешь, тем больнее будет", self.__main_color, (50, 50), 48)
            self.write("приземление.", self.__main_color, (50, 100), 48)
        if self.__tutorial_page == 4:
            self.write("Если у вас не получается победить врага,", self.__main_color, (50, 50), 48)
            self.write("не расстраивайтесь, пробуйте разные ", self.__main_color, (50, 100), 48)
            self.write("тактики и разный подход, умирайте и ", self.__main_color, (50, 150), 48)
            self.write("пробуйте ещё раз сразиться с ним, и", self.__main_color, (50, 200), 48)
            self.write("когда ни будь вы его одолеете.", self.__main_color, (50, 250), 48)
        
        x = width - 180
        y = height - 40
        
        self.write(f"Страница {self.__tutorial_page} из {self.__max_tutorial_page}", "white", (x, y), 24)
        self.write(f"Используйте <- и -> для перемещения по страницам туториала", "white", (40, y), 24)
        
    def update(self) -> None:
        ...

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
        self.settings_btns = [
            {
                "title": "Анимации",
                "pos": (50, 175),
                "size": (150, 50),
                "callback": self.__animation_btn_pressed,
                "var_name": "DRAW_ANIMATIONS",
                "type": "submit",
            },
            {
                "title": "Музыка",
                "pos": (250, 175),
                "size": (150, 50),
                "callback": self.__sounds_btn_pressed,
                "var_name": "PLAY_SOUNDS",
                "type": "submit",
            },
            {
                "title": "Фон",
                "pos": (450, 175),
                "size": (150, 50),
                "callback": self.__background_btn_pressed,
                "var_name": "DRAW_BACKGROUND",
                "type": "submit",
            },
        ]
        
        window_size_shift = EngineSettings.get_var("WINDOW_SHIFT")
        
        for ind, window_size in enumerate(EngineSettings.get_var("AVAILABLE_WINDOW_SIZES")):
            y_pos = 325 + ind // 3 * 75
            x_pos = (ind % 3) * 200 + 50

            self.settings_btns.append({
                "title": f"{window_size[0] + window_size_shift[0]}x{window_size[1] + window_size_shift[1]}",
                "pos": (x_pos, y_pos),
                "size": (150, 50),
                "callback": self.__set_window_size,
                "var_name": "WINDOW_SIZE",
                "type": "select",
                "active": EngineSettings.get_var("WINDOW_SIZE") == window_size
            })

        self.__on_color = pygame.Color("#332FD0")
        self.__off_color = pygame.Color("#FB2576")
        self.__background_color = "#20262E"

    def render(self, surface: pygame.Surface):
        surface.fill(self.__background_color)
        
        self.write("Настройки: ", "white", (50, 50), 48)
        self.write("Основные: ", "white", (50, 125), 30)
        self.write("Размеры экрана: ", "white", (50, 275), 30)
        
        height = EngineSettings.get_var("HEIGHT")
        self.write("Нажмите 'esc' для выхода в главное меню", "white", (50, height - 50), 24)

        for btn in self.settings_btns:
            pygame.draw.rect(
                surface, "white",
                pygame.Rect(btn["pos"], btn["size"]), 1
            )

            if btn["type"] == "submit":
                pygame.draw.rect(
                    surface, self.__on_color if settings.__dict__[btn["var_name"]] else self.__off_color,
                    pygame.Rect(
                        btn["pos"][0] + 1, btn["pos"][1] + 1,
                        btn["size"][0] - 2, btn["size"][1] - 2
                    )
                )
            else:
                pygame.draw.rect(
                    surface, self.__on_color if btn["active"] else self.__off_color,
                    pygame.Rect(
                        btn["pos"][0] + 1, btn["pos"][1] + 1,
                        btn["size"][0] - 2, btn["size"][1] - 2
                    )
                )

            self.write(btn["title"], "white", (btn["pos"][0] + 15, btn["pos"][1] + 15), 24)
        
    def update(self) -> None:
        ...

    def events_handler(self, event: pygame.event.Event):
        pressed = pygame.key.get_pressed()

        if event.type == pygame.KEYDOWN and (pressed[pygame.K_SPACE] or pressed[pygame.K_ESCAPE]):
            self.stop("start")
            
        if event.type == pygame.KEYDOWN and pressed[pygame.K_g]:
            pygame.display.set_mode((1000, 600))

            settings.HEIGHT = 1000
            EngineSettings.VARIABLES["HEIGHT"] = 1000
            
            settings.WIDTH = 600
            EngineSettings.VARIABLES["WIDTH"] = 600
            
            settings.SIZE = (1000, 600)
            EngineSettings.VARIABLES["SIZE"] = (1000, 600)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for ind, btn in enumerate(self.settings_btns):
                if (
                    btn["pos"][0] <= event.pos[0] <= btn["pos"][0] + btn["size"][0] and
                    btn["pos"][1] <= event.pos[1] <= btn["pos"][1] + btn["size"][1]
                ):
                    btn["callback"](ind)

    def __animation_btn_pressed(self, ind):
        change_to = not settings.DRAW_ANIMATIONS

        settings.DRAW_ANIMATIONS = change_to
        EngineSettings.DEFAULT_VARIABLES["DRAW_ANIMATIONS"] = change_to
        EngineSettings.VARIABLES["DRAW_ANIMATIONS"] = change_to
    
    def __sounds_btn_pressed(self, ind):
        pygame.mixer.stop()
        change_to = not settings.PLAY_SOUNDS

        settings.PLAY_SOUNDS = change_to
        EngineSettings.VARIABLES["PLAY_SOUNDS"] = change_to
    
    def __background_btn_pressed(self, ind):
        change_to = not settings.DRAW_BACKGROUND

        settings.DRAW_BACKGROUND = change_to
        EngineSettings.VARIABLES["DRAW_BACKGROUND"] = change_to
    
    def __set_window_size(self, ind):
        width_shift, height_shift = EngineSettings.get_var("WINDOW_SHIFT")
        
        width, height = tuple(map(int, self.settings_btns[ind]["title"].split("x")))
        width -= width_shift
        height -= height_shift
        
        size = width, height
        
        pygame.display.set_mode(size)
        
        settings.SIZE = size
        EngineSettings.VARIABLES["SIZE"] = size
        
        settings.WIDTH = width
        EngineSettings.VARIABLES["WIDTH"] = width
        
        settings.HEIGHT = height
        EngineSettings.VARIABLES["HEIGHT"] = height
        
        for btn in self.settings_btns:
            if btn["var_name"] == "WINDOW_SIZE":
                self.settings_btns[ind]["active"] = False

        self.settings_btns[ind]["active"] = True

        render_distance = (
            width // EngineSettings.get_var("BLOCK_SIZE"),
            height // EngineSettings.get_var("BLOCK_SIZE")
        )

        settings.RENDER_DISTANCE = render_distance
        EngineSettings.VARIABLES["RENDER_DISTANCE"] = render_distance
