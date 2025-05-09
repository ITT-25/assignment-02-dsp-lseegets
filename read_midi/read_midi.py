from mido import MidiFile
import math

notes = []
current_time = 0


# Convert MIDI note to Hz

def note_to_frequency(note):
    return round(440 * math.pow(2, (note - 69)/12), 2)


# Save MIDI notes as frequencies with their time stamps

for msg in MidiFile('berge.mid').play():
    current_time += msg.time
    if msg.type == 'note_on':
        notes.append({'start': current_time, 'freq': note_to_frequency(msg.note)})