import random

class Kingfisher():
    def __init__(self):
        pass

    def select_move(self, board):
        is_legal = list(board.legal_moves)

        if not is_legal:
            return None
        
        random_move = random.choice(is_legal)

        return random_move
