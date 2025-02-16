from player import Player

# Calculate the best move for current player and opponent
def negamax_search(board, curr_player, max_depth, eval_function, alpha=float('-inf'), beta=float('inf')):    
    # Evaluate the position until you reach depth or game is over
    if max_depth == 0 or board.is_game_over():
        return eval_function(board, curr_player)

    # Calculate the best move from all possible moves
    curr_eval = float('-inf')
    for move in board.legal_moves:
        board.push(move)
        
        # Search using negamax algorithm
        score = -negamax_search(board, Player(board), max_depth - 1, 
                                eval_function, -beta, -alpha
                                )

        board.pop()

        # Check if current move is better than the searched move
        curr_eval = max(curr_eval, score)
        alpha = max(alpha, score)

        # If you already have best result, prune the search
        if alpha >= beta:
            break

    return curr_eval