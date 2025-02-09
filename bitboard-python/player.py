class Player:
    def __init__(self):
        self.turn = True

    def player_turn(self):
        self.turn = not self.turn
        return self.turn