from pyglet import window, text
import pygame
import threading
import time
import os

from karaoke_game.note import Note
from karaoke_game.utils import WINDOW_WIDTH, WINDOW_HEIGHT, FONT_NAME, LEAD_TIME, NOTE_SPEED, AUDIO_BUFFER, MIDI_DIRECTORY
from karaoke_game.audio_sample import freq_generator
from read_midi.read_midi import load_notes

class Game:

    def __init__(self):
        self.started = False
        self.finished = False
        self.loading = False
        self.songs = []
        self.song_labels = []
        self.selected_song = None
        self.selected_song_index = 0
        self.notes = []
        self.song_notes = []
        self.current_song_note = None
        self.score = 0
        self.freq_gen = None

        self.get_songnames()

    def get_songnames(self):
        for file in os.listdir(MIDI_DIRECTORY):
            if file.endswith('.mid'):
                self.songs.append(file)

    def on_key_press(self, symbol, modifiers):
        if symbol == window.key.SPACE and self.started and self.finished:
            self.started = False
            self.finished = False
        if symbol == window.key.DOWN:
            self.selected_song_index = self.selected_song_index + 1 if self.selected_song_index < len(self.songs) - 1 else 0
        if symbol == window.key.UP:
            self.selected_song_index = self.selected_song_index - 1 if self.selected_song_index > 0 else len(self.songs) - 1
        if symbol == window.key.ENTER and not self.started:
            self.selected_song = self.songs[self.selected_song_index]
            self.start_game()

    def start_game(self):
        self.load_notes()
        self.score = 0
        self.finished = False
        self.started = True
        self.freq_gen = freq_generator()
        threading.Timer(LEAD_TIME, self.play_midi).start()

    def load_notes(self):
        print("Loading notes...")
        self.notes = load_notes(MIDI_DIRECTORY + self.selected_song)
        self.song_notes.clear()

        offset = NOTE_SPEED * (self.notes[0]["start"] - LEAD_TIME - AUDIO_BUFFER)

        for note_data in self.notes:
            x = WINDOW_WIDTH + NOTE_SPEED * (note_data["start"] - LEAD_TIME) - offset
            note = Note(x, note_data["freq"], NOTE_SPEED * note_data["duration"])
            self.song_notes.append(note)

        print("Done loading!")

    def play_midi(self):
        pygame.mixer.init()
        pygame.mixer.music.load(MIDI_DIRECTORY + self.selected_song)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        time.sleep(2)
        self.finished = True

    def draw_song_list(self, offset):
        distance = 50
        for i in range(0, len(self.songs)):
            y = offset - (i + 1) * distance
            font_size = 30 if i == self.selected_song_index else 20
            song_label = text.Label(str(i + 1) + ". " + os.path.splitext(self.songs[i])[0], font_name=FONT_NAME, font_size=font_size, x=WINDOW_WIDTH//2, y=y, anchor_x='center')
            
            song_label.draw()
            self.song_labels.append(song_label)

    def draw_start_screen(self):
        header = text.Label("Welcome to Karaoke!", font_name=FONT_NAME, font_size=36, x=WINDOW_WIDTH//2, y=WINDOW_HEIGHT - 80, anchor_x='center')
        subtitle = text.Label("Use Arrow Keys to Pick a Song From the List and press ENTER:", font_name=FONT_NAME, font_size=20, x=WINDOW_WIDTH//2, y=header.y - 80, anchor_x='center')

        header.draw()
        subtitle.draw()
        self.draw_song_list(subtitle.y)

    def draw_score(self):
        text.Label(f'Score: {self.score}', font_name=FONT_NAME, font_size=20, x=WINDOW_WIDTH-100, y=WINDOW_HEIGHT-30, anchor_x='center').draw()

    def draw_loading_screen(self):
        text.Label(f'Brace your vocal chords...', font_name=FONT_NAME, font_size=20, x=WINDOW_WIDTH//2, y=WINDOW_HEIGHT//2 + 40, anchor_x='center').draw()

    def draw_finish_screen(self):
        text.Label(f'Your Score: {self.score}', font_name=FONT_NAME, font_size=20, x=WINDOW_WIDTH//2, y=WINDOW_HEIGHT//2, anchor_x='center', anchor_y='center').draw()
        text.Label('You certainly gave it your best.', font_name=FONT_NAME, font_size=36, x=WINDOW_WIDTH//2, y=WINDOW_HEIGHT//2 + 40, anchor_x='center', anchor_y='center').draw()
        text.Label('Press SPACE to Go Back to Main Menu', font_name=FONT_NAME, font_size=20, x=WINDOW_WIDTH//2, y=WINDOW_HEIGHT//2 - 40, anchor_x='center', anchor_y='center').draw()