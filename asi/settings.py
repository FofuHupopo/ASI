from screeninfo import get_monitors


for m in get_monitors():
    if m.is_primary:
        HEIGHT, WIDTH = int(0.8 * m.height),int(0.8 * m.width)
        
WIDTH, HEIGHT = 1000, 600
SIZE = WIDTH, HEIGHT

WINDOW_NAME = "ASI"
BACKGROUND_COLOR = "black"

DRAW_ANIMATIONS = False
PLAY_SOUNDS = False

FPS = 100
