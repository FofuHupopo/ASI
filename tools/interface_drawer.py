import pygame
from tkinter import Tk, Button, Entry, Label, LabelFrame, Frame, Scrollbar, Canvas
from _tkinter import TclError


PYGAME_WINDOW_SIZE = (750, 500)
PROGRAM_NAME = "Проектировщик интерфейса"

BASE_CODE = (
    "import pygame\n\n\n"
    "def draw(surface: pygame.Surface):\n"
)

TKINTER_SETTINGS = {
    "TKINTER_WINDOW_SIZE": "600x700",
    
    "BUTTON_WIDTH": 15,
    "LABEL_WIDTH": 5,
    "ENTRY_WIDTH": 10,
    
    "DEFAULT_HEIGHT": 2
}
COLOR_BUTTONS = {
    "Красный": (255, 0, 0, 255),
    "Зеленый": (0, 255, 0, 255),
    "Синий": (0, 0, 255, 255)
}


class BaseFigure:
    TYPE: str

    def draw(self) -> callable:
        ...
    
    def export(self) -> str:
        ...
    
    def update(self) -> None: ...
        
    def __call__(self, **kwargs):
        for var in kwargs:
            self.__dict__[var] = kwargs[var]

    @property
    def need_enter(self):
        return False
    

class LineFigure(BaseFigure):
    TYPE: str = "Линия"

    def __init__(self, color, start_pos, width) -> None:
        self.color = color
        self.start_pos = start_pos
        self.end_pos = start_pos
        self.width = width
    
    def draw(self, surface: pygame.Surface):
        pygame.draw.line(
            surface, self.color,
            self.start_pos, self.end_pos, self.width
        )

    def export(self) -> str:
        if type(self.color) is not pygame.Color:
            self.color = pygame.Color(self.color)

        return (
            f"pygame.draw.line(\n"
            f"    surface, pygame.Color({self.color}),\n"
            f"    {self.start_pos}, {self.end_pos}, {self.width}\n"
            f")"
        )
        
        
class RectangleFigure(BaseFigure):
    TYPE: str = "Прямоугольник"

    def __init__(self, color, start_pos, width) -> None:
        self.color = color
        self.start_pos = start_pos
        self.size = [0, 0]
        self.width = width
    
    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(
            surface, self.color,
            pygame.Rect(
                self.start_pos, self.size
            ), self.width
        )

    def export(self) -> str:
        if type(self.color) is not pygame.Color:
            self.color = pygame.Color(self.color)

        return (
            f"pygame.draw.rect(\n"
            f"    surface, pygame.Color({self.color}),\n"
            f"    pygame.Rect(\n"
            f"        {self.start_pos}, {self.size}\n"
            f"    )\n"
            f"), {self.width}"
        )
        

class CircleFigure(BaseFigure):
    TYPE: str = "Окружность"

    def __init__(self, color, center_pos, width) -> None:
        self.color = color
        self.center_pos = center_pos
        self.radius = 0
        self.width = width
    
    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(
            surface, self.color,
            self.center_pos, self.radius, self.width
        )

    def export(self) -> str:
        if type(self.color) is not pygame.Color:
            self.color = pygame.Color(self.color)

        return (
            f"pygame.draw.circle(\n"
            f"    surface, pygame.Color({self.color}),\n"
            f"    {self.center_pos}, {self.radius}, {self.width}\n"
            f")"
        )
        

class PolygonFigure(BaseFigure):
    TYPE: str = "Полигон"

    def __init__(self, color, start_point, width) -> None:
        self.color = color
        self.__points = [start_point]
        self.tmp_point = None
        self.width = width
        self.drawing = True

    def update(self, point):
        self.__points.append(point)

    def draw(self, surface: pygame.Surface):
        if self.drawing:
            points = [*self.__points, self.tmp_point]
        else:
            points = self.__points

        if len(points) > 1:
            pygame.draw.polygon(
                surface, self.color,
                points, self.width
            )

    def export(self) -> str:
        if type(self.color) is not pygame.Color:
            self.color = pygame.Color(self.color)

        return (
            f"pygame.draw.polygon(\n"
            f"    surface, pygame.Color({self.color}),\n"
            f"    {self.__points}, {self.width}\n"
            f")"
        )
    
    @property
    def need_enter(self):
        return True


# class TextFigure(BaseFigure):
#     TYPE: str = "Текст"

#     def __init__(self, color, pos, text) -> None:
#         self.color = color
#         self.pos = pos
#         self.drawing = True
#         self.text = text
#         self.__font = pygame.font.SysFont('serif', 16)

#     def update(self, pos=None, text=None):
#         self.pos = pos

#     def draw(self, surface: pygame.Surface):
#         text_surface = self.__font.render(self.text, False, self.color)
#         surface.blit(text_surface, self.pos)

#     def export(self) -> str:
#         if type(self.color) is not pygame.Color:
#             self.color = pygame.Color(self.color)

#         return (
#             "text"
#         )

#     @property
#     def need_enter(self):
#         return True


class InterfaceDrawer:
    def __init__(self) -> None:
        self.__current_width = 1
        self.__current_color = (255, 255, 255)
        self.__background_color = (0, 0, 0)
        
        self.__need_enter = False
        self.start_draw = False
        self.__mouse_pos = [0, 0]
        
        self.__figures: list[BaseFigure] = []
        self.__current_figure = None

        self.__current_figure_class = None

    def event_handler(self, event: pygame.event.Event, pressed):

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.__need_enter:
                self.__update_need_enter_figure()
            else:
                self.start_draw = True
                self.__mouse_pos = event.pos
            
                self.__create_figure()

        if event.type == pygame.MOUSEBUTTONUP:
            if not self.__need_enter:
                self.start_draw = False
                self.__current_figure = None

        if event.type == pygame.MOUSEMOTION:
            self.__mouse_pos = event.pos
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            self.__stop_need_enter()

        if event.type == pygame.QUIT:
            self.export_ui()
            
    def __create_figure(self):
        if isinstance(self.__current_figure_class, type(None)):
            return

        if self.__current_figure_class is LineFigure:
            self.__current_figure = self.__current_figure_class(color=self.__current_color, start_pos=self.__mouse_pos, width=self.__current_width)
        
        if self.__current_figure_class is RectangleFigure:
            self.__current_figure = self.__current_figure_class(color=self.__current_color, start_pos=self.__mouse_pos, width=self.__current_width)
            
        if self.__current_figure_class is CircleFigure:
            self.__current_figure = self.__current_figure_class(color=self.__current_color, center_pos=self.__mouse_pos, width=self.__current_width)
            
        if self.__current_figure_class is PolygonFigure:
            self.__current_figure = self.__current_figure_class(color=self.__current_color, start_point=self.__mouse_pos, width=self.__current_width)

        if self.__current_figure:
            self.__figures.append(self.__current_figure)
            self.__need_enter = self.__current_figure.need_enter

    def __update_figure(self):
        if isinstance(self.__current_figure, LineFigure):
            self.__current_figure(end_pos=self.__mouse_pos)
        
        if isinstance(self.__current_figure, RectangleFigure):
            start_pos = self.__current_figure.start_pos
            self.__current_figure(
                size=(
                    self.__mouse_pos[0] - start_pos[0],
                    self.__mouse_pos[1] - start_pos[1],
                )
            )

        if isinstance(self.__current_figure, CircleFigure):
            center_pos = self.__current_figure.center_pos
            radius: float = ((center_pos[0] - self.__mouse_pos[0]) ** 2 + (center_pos[1] - self.__mouse_pos[1])) ** .5
            self.__current_figure(radius=radius.real)
        
        if isinstance(self.__current_figure, PolygonFigure):
            self.__current_figure(tmp_point=self.__mouse_pos)
    
    def __update_need_enter_figure(self):
        if not self.__need_enter:
            return

        if isinstance(self.__current_figure, PolygonFigure):
            self.__current_figure.update(point=self.__mouse_pos)
    
    def __stop_need_enter(self):
        if self.__need_enter and self.__current_figure:
            self.__current_figure(drawing=False)
        
        self.start_draw = False
        
        self.__current_figure = None
        self.__need_enter = False

    def draw(self, surface: pygame.Surface):
        if self.__current_figure:
            self.__update_figure()

        for figure in self.__figures:
            figure.draw(surface)
    
    def get_figures(self):
        return self.__figures
            
    def set_current_figure_class(self, figure_class):
        self.__current_figure_class = figure_class
        
    def set_current_color(self, color):
        self.__current_color = color
    
    def set_current_width(self, width):
        self.__current_width = width
        
    def set_background_color(self, color):
        self.__background_color = color
    
    @property
    def background_color(self):
        return self.__background_color
    
    @property
    def width(self):
        return self.__current_width
    
    @property
    def mouse_pos(self):
        return self.__mouse_pos
    
    def export_ui(self):
        code = BASE_CODE
        
        code += " " * 4 + f"surface.fill({self.__background_color})\n\n"
        
        for figure in self.__figures:
            for code_line in figure.export().split("\n"):
                code += " " * 4 + code_line + "\n"

        with open("ui.py", "w") as file:
            file.write(code)
        
        print("\n" + code + "\n")


def load_pygame() -> tuple[pygame.Surface, pygame.time.Clock]:
    pygame.init()
    size = PYGAME_WINDOW_SIZE

    surface = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    pygame.display.set_caption(PROGRAM_NAME)

    return surface, clock


def load_tkinter(interface_drawer: InterfaceDrawer) -> Tk:
    window = Tk()
    window.title(PROGRAM_NAME)
    window.geometry(TKINTER_SETTINGS["TKINTER_WINDOW_SIZE"])
    window.resizable(False, False)
    
    
    def create_label_frame(text_field, side=None, anchor=None, relx=0, rely=0, width=None):
        label_frame = LabelFrame(window, text=text_field)
        label_frame.place(relx=relx, rely=rely, width=width)
        
        return label_frame
    
    def create_button(master, text_field, command):
        btn = Button(
            master, text=text_field,
            width=TKINTER_SETTINGS["BUTTON_WIDTH"], height=TKINTER_SETTINGS["DEFAULT_HEIGHT"]
        )
        btn.config(command=command)
        btn.pack()
        
    def create_retry(retry_name, master=window):
        frame = Frame(master)
        frame.pack()

        Label(frame, text=f"{retry_name}:", width=5).pack(side="left")
        color_input = Entry(frame, width=10)
        color_input.pack(side="right")
        
        return color_input


    # Фигуры

    figure_label = create_label_frame("Фигуры", side="left", relx=0, rely=0)

    def add_figure_btn(figure_class):
        create_button(
            figure_label, figure_class.TYPE,
            lambda: interface_drawer.set_current_figure_class(figure_class)
        )

    add_figure_btn(LineFigure)
    add_figure_btn(RectangleFigure)
    add_figure_btn(CircleFigure)
    add_figure_btn(PolygonFigure)


    # Цвета
    
    color_label = create_label_frame("Цвета", side="right", relx=0, rely=0.33)

    def create_color_btn(color_name, color_value):    
        create_button(
            color_label, color_name,
            lambda: interface_drawer.set_current_color(pygame.Color(color_value))
        )
        
    create_color_btn("Красный", COLOR_BUTTONS["Красный"])
    create_color_btn("Зеленый", COLOR_BUTTONS["Зеленый"])
    create_color_btn("Синий", COLOR_BUTTONS["Синий"])


    # Ввод цвета
    
    input_color_label = create_label_frame("Введите цвет", anchor="n", relx=0.33, rely=0)

    def rgba_entry(text_field, callback):
        colors = [
            create_retry(color_name, input_color_label)
            for color_name in ("r", "g", "b", "alpha")
        ]

        def get_color():
            color = [255, 255, 255, 255]

            for ind, color_ in enumerate(colors):
                if not color_.get():
                    continue

                color[ind] = int(color_.get())

            return color

        create_button(
            input_color_label, text_field,
            lambda: callback(pygame.Color(get_color()))
        )

    rgba_entry("Изменить цвет", interface_drawer.set_current_color)
    rgba_entry("Изменить фон", interface_drawer.set_background_color)


    # Изменение значений
    
    one_value_label = create_label_frame("Значения", relx=0.66, rely=0)

    def one_value_entry(label_text, btn_text, callback):
        value = create_retry(
            label_text, one_value_label
        )
        value.pack(side="left")
    
        create_button(
            one_value_label, btn_text,
            lambda: callback(int(value.get()))
        )
    
    one_value_entry("Ширина", "Изменить ширину", interface_drawer.set_current_width)
    
    
    # Информация
    
    info_label = create_label_frame("Информация", side="bottom", relx=0, rely=0.55, width=600)
    
    def info():
        labels = dict()
        
        def create_label(name, text):
            label = Label(info_label, text=text())
            label.pack()

            labels[name] = {
                "text": text,
                "object": label
            }
        
        create_label("mouse_coords", lambda: f"Координата мышки: {tuple(interface_drawer.mouse_pos)}")
        create_label("current_width", lambda: f"Текущая ширина: {interface_drawer.width}")
        create_label("current_color", lambda: f"Текущий цвет: {interface_drawer._InterfaceDrawer__current_color}")
        
        def update_label():
            for label in labels.values():
                text, object_ = label["text"], label["object"]
                
                object_["text"] = text()

            info_label.after(50, update_label)
    
        info_label.after(50, update_label)
    
    info()
    
    
    # Список объектов
    
    # figures_info_label = create_label_frame("Фигуры", relx=0, rely=0.7)

    # canvas = Canvas(figures_info_label, height=100, width=590)
    # canvas.pack()
    
    # frame = Frame(canvas)
    # frame.pack()
    
    # scrollbar = Scrollbar(figures_info_label, command=canvas.yview)
    
    # canvas.configure(yscrollcommand=scrollbar.set)
    # canvas.pack()
    # scrollbar.pack()

    # def figures_info():
    #     def load_figures():
    #         figures = []

    #         for figure in interface_drawer.get_figures():
    #             figures.append(
    #                 f"{figure.TYPE}, {figure.color}, {figure.width}"
    #             )
                
    #         figures_info_label.after(100, load_figures)
            
    #         draw_figures_info(figures)
        
    #     def draw_figures_info(figures: list):
    #         for widget in frame.winfo_children():
    #             widget.destroy()
            
    #         for figure in figures:
    #             create_label(figure)
    
    #     def create_label(figure):
    #         label = Label(frame, text=figure)
    #         label.pack()`
    
    #     figures_info_label.after(100, load_figures)

    # figures_info()
    
    return window


def mainloop(window: Tk, surface: pygame.Surface, clock: pygame.time.Clock, interface_drawer: InterfaceDrawer):
    running = True

    while running:
        pressed = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            
            interface_drawer.event_handler(event, pressed)
            
        surface.fill(interface_drawer.background_color)

        interface_drawer.draw(surface)

        pygame.display.flip()
        clock.tick(60)

        window.update()
        
        try:
            window.wm_state()
        except TclError:
            running = False


def main():
    interface_drawer = InterfaceDrawer()

    window = load_tkinter(interface_drawer)
    surface, clock = load_pygame()
    
    mainloop(window, surface, clock, interface_drawer)

    pygame.quit()


if __name__ == "__main__":
    main()
