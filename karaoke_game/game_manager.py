from pyglet import window, text
import pygame
import threading
import time
import os

from karaoke_game.note import Note
from karaoke_game.utils import WINDOW_WIDTH, WINDOW_HEIGHT, FONT_NAME, LEAD_TIME, NOTE_SPEED, SINGING_LINE_X, MIDI_DIRECTORY
from karaoke_game.audio_input import freq_generator
from read_midi.read_midi import load_notes

class Game:

    def __init__(self):
        self.started = False
        self.finished = False
        self.loading = False
        self.songs = self.get_songnames()   # All available songs
        self.song_labels = []               # The pyglet text objects representing the songs in a list
        self.selected_song = None           # The selected song for the current session
        self.selected_song_index = 0        # The index of the selected song
        self.notes = []                     # An array of JSON objects containing data for each note in the song
        self.song_notes = []                # An array of Note objects for the current song
        self.current_song_note = None       # The note that is currently playing
        self.score = 0
        self.freq_gen = None                # The current frequency from the user input device


    # Get all .mid files in the read_midi directory

    def get_songnames(self):
        songs = []
        for file in os.listdir(MIDI_DIRECTORY):
            if file.endswith('.mid'):
                songs.append(file)
        return songs


    def on_key_press(self, symbol, modifiers):
        if symbol == window.key.SPACE and self.started and self.finished:
            self.started = False
            self.finished = False
            self.current_song_note = None
        if symbol == window.key.DOWN:
            self.selected_song_index = self.selected_song_index + 1 if self.selected_song_index < len(self.songs) - 1 else 0
        if symbol == window.key.UP:
            self.selected_song_index = self.selected_song_index - 1 if self.selected_song_index > 0 else len(self.songs) - 1
        if symbol == window.key.ENTER and not self.started:
            self.selected_song = self.songs[self.selected_song_index]
            self.start_game()


    def start_game(self):
        self.loading = True
        threading.Thread(target=self.load_notes, daemon=True).start()
        self.score = 0
        self.finished = False
        self.started = True
        self.freq_gen = freq_generator()


    # Load notes from the selected midi file and create Note objects. Once loading has finished,
    # wait for [LEAD_TIME] seconds to start playing the song

    def load_notes(self):
        print("Loading notes...")
        self.notes = load_notes(MIDI_DIRECTORY + self.selected_song)
        self.song_notes.clear()

        for note_data in self.notes:
            # Add a small offset to the x position for better alignment with the singing line (6 * note_data["start"])
            x = SINGING_LINE_X + (NOTE_SPEED * (note_data["start"] + LEAD_TIME) + 6 * note_data["start"])

            # The width of a Note object depends on its duration and the speed at which the Note objects move
            note = Note(x, note_data["freq"], NOTE_SPEED * note_data["duration"])
            self.song_notes.append(note)

        print("Done loading!")
        self.loading = False
        threading.Timer(LEAD_TIME, self.play_midi).start()


    # Play the midi file. Once it's done playing, wait for one second before displaying the finish screen

    def play_midi(self):
        pygame.mixer.init()
        pygame.mixer.music.load(MIDI_DIRECTORY + self.selected_song)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        time.sleep(1)
        self.finished = True

    
    def write_final_message(self):
        if self.score <= 0:
            return "Come on now, did you even try?"
        elif self.score > 0 and self.score < 800:
            return "You certainly gave it your best!"
        else:
            return "Great job!"


    # Drawing a list of available songs in the main menu

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
        subtitle = text.Label("Use arrow keys to pick a song from the list and press ENTER:", font_name=FONT_NAME, font_size=20, x=WINDOW_WIDTH//2, y=header.y - 80, anchor_x='center')

        header.draw()
        subtitle.draw()
        self.draw_song_list(subtitle.y)


    def draw_score(self):
        text.Label(f'Score: {self.score}', font_name=FONT_NAME, font_size=20, x=WINDOW_WIDTH-100, y=WINDOW_HEIGHT-30, anchor_x='center').draw()


    def draw_loading_screen(self):
        text.Label(f'Preparing ' + str(os.path.splitext(self.songs[self.selected_song_index])[0]), font_name=FONT_NAME, font_size=20, x=WINDOW_WIDTH//2, y=WINDOW_HEIGHT//2 + 80, anchor_x='center').draw()
        text.Label(f'Brace your vocal chords...', font_name=FONT_NAME, font_size=20, x=WINDOW_WIDTH//2, y=WINDOW_HEIGHT//2 + 40, anchor_x='center').draw()
        

    def draw_finish_screen(self):
        text.Label(f'Your Score: {self.score}', font_name=FONT_NAME, font_size=20, x=WINDOW_WIDTH//2, y=WINDOW_HEIGHT//2, anchor_x='center', anchor_y='center').draw()
        text.Label(self.write_final_message(), font_name=FONT_NAME, font_size=36, x=WINDOW_WIDTH//2, y=WINDOW_HEIGHT//2 + 40, anchor_x='center', anchor_y='center').draw()
        text.Label('Press SPACE to go back to main menu', font_name=FONT_NAME, font_size=20, x=WINDOW_WIDTH//2, y=WINDOW_HEIGHT//2 - 40, anchor_x='center', anchor_y='center').draw()