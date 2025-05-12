import pyglet
from pyglet import window, shapes

from karaoke_game.utils import WINDOW_WIDTH, WINDOW_HEIGHT, NOTE_HEIGHT, UPDATE_FREQ, SINGING_LINE_X, NOTE_SPEED, OFF_COLOR, ON_COLOR
from karaoke_game.game_manager import Game

# RUN WITH py -m karaoke_game.karaoke

FREQ_CUTOFF = 50
MOVE_PER_FRAME = NOTE_SPEED * UPDATE_FREQ

win = window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
game = Game()

singing_line = shapes.Rectangle(SINGING_LINE_X, 0, 1, WINDOW_HEIGHT, (50, 50, 50))
user_note = shapes.Rectangle(SINGING_LINE_X - NOTE_HEIGHT // 2, WINDOW_HEIGHT // 2, NOTE_HEIGHT, NOTE_HEIGHT, OFF_COLOR)

@win.event
def on_key_press(symbol, modifiers):
    game.on_key_press(symbol, modifiers)


# Gradually move the note objects from right to left

def move_notes(notes):
    for note in notes:
        note.update_pos(note.x - MOVE_PER_FRAME)


# Check if note object collides with singing line

def check_line_collision():
    for note in game.song_notes:
        if (singing_line.x < note.shape.x + note.shape.width and
            singing_line.x + singing_line.width >  note.shape.x and
            singing_line.y < note.shape.y + note.shape.height and
            singing_line.y + singing_line.height > note.shape.y):
            game.current_song_note = note


# Check if user_note collides with the current note from the song (i.e., they have the same frequency)

def check_collision():
    if game.current_song_note and not game.finished:
        if (user_note.x + user_note.width >  game.current_song_note.shape.x and
            user_note.y < game.current_song_note.shape.y + game.current_song_note.shape.height and
            user_note.y + user_note.height > game.current_song_note.shape.y):
            user_note.color = ON_COLOR
            game.score += 10
        else:
            user_note.color = OFF_COLOR

def update(dt):
    if game.started and game.freq_gen:
        move_notes(game.song_notes)
        user_note.color = OFF_COLOR

        current_freq = next(game.freq_gen)
        if current_freq >= FREQ_CUTOFF:
            user_note.y = current_freq

        check_line_collision()
        check_collision()

pyglet.clock.schedule_interval(update, UPDATE_FREQ)

@win.event
def on_draw():
    win.clear()

    if not game.started and not game.finished and not game.loading:
        game.draw_start_screen()
    elif game.loading and game.started and not game.finished:
        game.draw_loading_screen() 
    elif game.started and not game.finished and not game.loading:
        game.draw_score()
        for note in game.song_notes:
            note.shape.draw()
        user_note.draw()
        singing_line.draw()
    elif game.finished:
        game.draw_finish_screen()

pyglet.app.run()