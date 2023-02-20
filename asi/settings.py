from screeninfo import get_monitors


for m in get_monitors():
    if m.is_primary:
        HEIGHT, WIDTH = int(0.8 * m.height),int(0.8 * m.width)

# WIDTH, HEIGHT = 1000, 600
SIZE = WIDTH, HEIGHT

RENDER_DISTANCE = (20, 10)

WINDOW_NAME = "ASI"
BACKGROUND_COLOR = "black"

DRAW_ANIMATIONS = True
DRAW_BACKGROUND = False
PLAY_SOUNDS = False

FPS = 100
