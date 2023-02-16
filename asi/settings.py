from screeninfo import get_monitors


# for m in get_monitors():
#     if m.is_primary:
#         HEIGHT, WIDTH = int(0.8 * m.height),int(0.8 * m.width)
        
WIDTH, HEIGHT = 2000, 1000

CELL_SIZE = WIDTH // 20

SIZE = WIDTH, HEIGHT

WINDOW_NAME = "ASI"
BACKGROUND_COLOR = "black"

DRAW_ANIMATIONS = True

FPS = 100
