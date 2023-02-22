from screeninfo import get_monitors


ALL_WINDOW_SIZES = (
    (3820, 2160),
    (3440, 1440),
    (2560, 1600),
    (2560, 1440),
    (1920, 1080),
    (1920, 1200),
    (1600, 900),
    (1366, 768),
    (1000, 800),
)

AVAILABLE_WINDOW_SIZES: list[tuple[int, int]] = []

WINDOW_SHIFT = WINDOW_WIDTH_SHIFT, WINDOW_HEIGHT_SHIFT = 0, 50


for monitor in get_monitors():
    if monitor.is_primary:
        for width, height in ALL_WINDOW_SIZES:
            if monitor.width >= width and monitor.height >= height:
                AVAILABLE_WINDOW_SIZES.append((
                    width - WINDOW_WIDTH_SHIFT,
                    height - WINDOW_HEIGHT_SHIFT
                ))


SIZE = WIDTH, HEIGHT = AVAILABLE_WINDOW_SIZES[-1]

RENDER_DISTANCE = (20, 10)

WINDOW_NAME = "ASI"
BACKGROUND_COLOR = "black"

BLOCK_SIZE = 50

DRAW_ANIMATIONS = True
DRAW_BACKGROUND = False
PLAY_SOUNDS = False

FPS = 60
