import pyglet
from pyglet import shapes, window
from utils import WINDOW_WIDTH, WINDOW_HEIGHT
from audio_input import listen

win = window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)

RECT_WIDTH = 100
RECT_HEIGHT = 50
TOP_Y = 0 + 6 * RECT_HEIGHT
REG_COLOR = (255, 0, 255)
SELECTED_COLOR = (0, 255, 0)

rects = []
selected_index = 0

for i in range(5):
    rects.append(shapes.Rectangle(WINDOW_WIDTH // 2, TOP_Y - i * (RECT_HEIGHT + 10), RECT_WIDTH, RECT_HEIGHT, REG_COLOR))


# If a chirp is detected, move selected_index up/down and highlight the associated rectangle

def update(dt):
    global selected_index
    result = listen()
    if result == 'down':
        selected_index = selected_index + 1 if selected_index < len(rects) - 1 else 0
    elif result == 'up':
        selected_index = selected_index - 1 if selected_index > 0 else len(rects) - 1

    for i, r in enumerate(rects):
        if i == selected_index:
            r.color = SELECTED_COLOR
        else:
            r.color = REG_COLOR

pyglet.clock.schedule_interval(update, 0.1)

@win.event
def on_draw():
    win.clear()
    
    for r in rects:
        r.draw()

pyglet.app.run()