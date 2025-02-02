class Player:
    def __init__(self):
        self.turn = "White"
        self.white_pieces = 0x000000000000FFFF
        self.black_pieces = 0xFFFF000000000000

    def player_turn(self):
        self.turn = "Black" if self.turn == "White" else "White"
        return self.turn
    
    def occupied_squares(self):
        return self.white_pieces | self.black_pieces