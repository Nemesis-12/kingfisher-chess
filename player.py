import chess

class Player:
    def __init__(self, board):
        self.player = chess.WHITE if board.turn else chess.BLACK
        self.player_name = "White" if self.player == chess.WHITE else "Black"