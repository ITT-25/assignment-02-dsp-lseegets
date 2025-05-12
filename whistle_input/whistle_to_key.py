from pynput.keyboard import Controller, Key
from whistle_input.audio_input import listen

keyboard = Controller()

def whistle_to_key():
    result = listen()
    if result == "down":
        keyboard.press(Key.down)
        keyboard.release(Key.down)
    elif result == "up":
        keyboard.press(Key.up)
        keyboard.release(Key.up)

while True: 
    whistle_to_key()