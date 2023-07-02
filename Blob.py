from Position import Position


class Blob:

    position = Position(-1, -1)
    player = None
    color = None

    def __init__(self, position, player):
        self.position = position
        self.player = player
        if self.player.get_type() == 'Human':
            self.color = 'B'  # Blue
        else:
            self.color = 'P'  # Pink

    def set_position(self, position):
        self.position = position

    def set_player(self, player):
        self.player = player
        if self.player.get_type() == 'Human':
            self.color = 'B'
        if self.player.get_type() == 'AI':
            self.color = 'P'

    def get_player(self):
        return self.player

    def get_position(self):
        return self.position

    def get_color(self):
        return self.color