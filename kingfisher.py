import random
import search
from player import Player
from evaluation import evaluation

# Define the AI
class Kingfisher():
    # Initialize
    def __init__(self, max_depth=5):
        self.max_depth = max_depth

    # Select a move to play
    def select_move(self, board):
        best_moves = []
        best_score = float('-inf')

        # Check for legal moves and evaluate them
        for move in board.legal_moves:
            board.push(move)

            score = -search.negamax_search(board, Player(board), 
                                           self.max_depth -1, evaluation)

            board.pop()

            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)

        # Play the best move according to the current position
        return random.choice(best_moves)
