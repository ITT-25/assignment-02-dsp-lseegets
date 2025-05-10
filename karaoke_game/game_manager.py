from pyglet import window, text
import pygame
import threading
import time

from karaoke_game.note import Note
from karaoke_game.utils import WINDOW_WIDTH, WINDOW_HEIGHT, FONT_NAME, LEAD_TIME, NOTE_SPEED, AUDIO_BUFFER
from karaoke_game.audio_sample import freq_generator
from read_midi.read_midi import load_notes

class Game:

    def __init__(self):
        self.started = False
        self.finished = False
        self.loading = False
        self.song = None
        self.notes = []
        self.song_notes = []
        self.current_song_note = None
        self.elapsed_time = 0
        self.note_index = 0
        self.score = 0
        self.freq_gen = None

    def on_key_press(self, symbol, modifiers):
        if symbol == window.key.SPACE and not self.started:
            self.load_notes()
            self.score = 0
            self.finished = False
            self.started = True
            self.freq_gen = freq_generator()
            threading.Timer(LEAD_TIME, self.play_midi, args=(self.song,)).start()

    def load_notes(self):
        print("Loading notes...")
        self.notes = load_notes('read_midi/berge.mid')
        self.song_notes.clear()

        offset = NOTE_SPEED * (self.notes[0]["start"] - LEAD_TIME - AUDIO_BUFFER)

        for note_data in self.notes:
            x = WINDOW_WIDTH + NOTE_SPEED * (note_data["start"] - LEAD_TIME) - offset
            note = Note(x, note_data["freq"], NOTE_SPEED * note_data["duration"])
            self.song_notes.append(note)

        print("Done loading!")

    def play_midi(self, midi):
        pygame.mixer.init()
        pygame.mixer.music.load(midi)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        time.sleep(2)
        self.started = False
        self.finished = True

    def draw_start_screen(self):
        text.Label("Welcome to Karaoke!", font_name=FONT_NAME, font_size=36, x=WINDOW_WIDTH//2, y=WINDOW_HEIGHT//2 + 40, anchor_x='center').draw()
        text.Label("Press SPACE to Start", font_name=FONT_NAME, font_size=20, x=WINDOW_WIDTH//2, y=WINDOW_HEIGHT//2 - 40, anchor_x='center').draw()

    def draw_score(self):
        text.Label(f'Score: {self.score}', font_name=FONT_NAME, font_size=20, x=WINDOW_WIDTH-100, y=WINDOW_HEIGHT-30, anchor_x='center').draw()

    def draw_loading_screen(self):
        text.Label(f'Brace your vocal chords...', font_name=FONT_NAME, font_size=20, x=WINDOW_WIDTH//2, y=WINDOW_HEIGHT//2 + 40, anchor_x='center').draw()

    def draw_finish_screen(self):
        text.Label(f'Your Score: {self.score}', font_name=FONT_NAME, font_size=20, x=WINDOW_WIDTH//2, y=WINDOW_HEIGHT//2, anchor_x='center', anchor_y='center').draw()
        text.Label('You certainly gave it your best.', font_name=FONT_NAME, font_size=36, x=WINDOW_WIDTH//2, y=WINDOW_HEIGHT//2 + 40, anchor_x='center', anchor_y='center').draw()
        text.Label('Press SPACE to restart', font_name=FONT_NAME, font_size=20, x=WINDOW_WIDTH//2, y=WINDOW_HEIGHT//2 - 40, anchor_x='center', anchor_y='center').draw()