class Player:

    player_type = None      # Player type: (Human or AI)

    def __init__(self, type):
        self.player_type = 'Human' if type == 'Human' else 'AI'

    def get_type(self):
        return self.player_type