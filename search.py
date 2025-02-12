from player import Player

# Calculate the best move for current player and opponent
def best_move(board, curr_player, max_depth, eval_function):
    outcome = board.outcome()

    # Calculate if game is over
    if board.is_game_over():
        if outcome.winner == curr_player.player:
            return float('inf')
        elif outcome.winner is None:
            return 0
        else:
            return float('-inf')
        
    if max_depth == 0:
        return eval_function(board, curr_player)
    
    # Calculate the best move from all possible moves
    best_result = float('-inf')
    for move in board.legal_moves:
        board.push(move)
        opp_state = best_move(board, Player(board), max_depth - 1, eval_function)
        curr_state = -opp_state

        if curr_state > best_result:
            best_result = curr_state

        board.pop()
    
    return best_result