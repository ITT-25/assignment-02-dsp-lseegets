from pyglet import shapes

from karaoke_game.utils import NOTE_HEIGHT, SLACK


# Note object representing one note from a song in the pyglet interface

class Note:

    def __init__(self, x, y, width):
        self.width = width

        # Frequencies are given some slack since hitting the exact same frequency is a bit unrealistic
        self.height = NOTE_HEIGHT + (2 * SLACK)
        self.x = x
        self.y = y - self.height // 2
        self.shape = shapes.Rectangle(x, self.y, width, self.height, (255, 0, 255))

    def update_pos(self, x):
        self.x = x
        self.shape.x = x