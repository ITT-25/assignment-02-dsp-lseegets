import pyglet
from pyglet import window, shapes, text
from audio_sample import freq_generator

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 1000

win = window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)

label = text.Label("Press Space To Start", font_name='Courier New', font_size=20, x=WINDOW_WIDTH//2, y=WINDOW_HEIGHT//2, anchor_x='center')
note = shapes.Rectangle(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, 100, 50, (255, 0, 0))

started = False
freq_gen = None

@win.event
def on_key_press(symbol, modifiers):
    global started, freq_gen
    if symbol == window.key.SPACE and not started:
        started = True
        freq_gen = freq_generator()
        label.text = "Listening..."

def update(dt):
    global current_freq
    if started and freq_gen:
        try:
            current_freq = next(freq_gen)
            label.text = f"Freq: {next(freq_gen)} Hz"
            if current_freq >= 80:
                note.y = float(current_freq)
        except StopIteration:
            label.text = "Done!"

pyglet.clock.schedule_interval(update, 1/20.0)

@win.event
def on_draw():
    win.clear()
    label.draw()
    note.draw()

pyglet.app.run()