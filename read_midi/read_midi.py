from mido import MidiFile
import math
import json
import os

# Convert MIDI note to Hz

def note_to_frequency(note):
    return round(440 * math.pow(2, (note - 69)/12), 2)


# Save notes to .json

def save_notes_to_json(filename, notes):
    file = f"{filename}_notes.json"
    with open(file, 'w') as file:
        json.dump(notes, file)


# Load notes if they have been previously saved

def load_notes_from_json(filename):
    file = f"{filename}_notes.json"
    if os.path.exists(file):
        with open(file, 'r') as file:
            return json.load(file)
    else:
        return None


# Save MIDI notes as frequencies with their time stamps and duration. Check if there is already a .json file
# containing the notes to save time

def load_notes(filename):
    notes = load_notes_from_json(filename)

    if notes == None:
        notes = []
        current_time = 0
        note_on_times = {}

        for msg in MidiFile(filename).play():
            current_time += msg.time

            # Save all note_on times of the current message in case of overlapping notes
            if msg.type == 'note_on':
                note_on_times[msg.note] = current_time
            elif msg.type == 'note_off':
                note_start = note_on_times[msg.note]
                note_duration = current_time - note_start   # duration is needed to determine the visual width of the Note object
                notes.append({'start': note_start, 'freq': note_to_frequency(msg.note), 'duration': round(note_duration, 2)})
                del note_on_times[msg.note]
        save_notes_to_json(filename, notes)
        
    return notes