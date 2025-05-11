from pyglet import shapes

from karaoke_game.utils import NOTE_HEIGHT, SLACK

class Note:

    def __init__(self, x, y, width):
        self.width = width
        self.height = NOTE_HEIGHT + (2 * SLACK)
        self.x = x
        self.y = y - self.height // 2
        self.shape = shapes.Rectangle(x, self.y, width, self.height, (255, 0, 255))

    def update_pos(self, x):
        self.x = x
        self.shape.x = x