from mcts import MCTS

# Define the AI
class Kingfisher():
    # Initialize
    def __init__(self, time_limit=5.0):
        self.mcts = MCTS(max_time=time_limit)

    # Select a move to play
    def select_move(self, board):
        return self.mcts.search(board)
