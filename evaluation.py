import chess

# Evaluate the current board position and return who's winning
def evaluation(board, curr_player):
    # Initialize piece scores
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0
    }

    # Initialize material count
    material_count = 0

    # Count the value of pieces on board and determine who is leading
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        
        if piece:
            value = piece_values[piece.piece_type]
            if piece.color == curr_player.player:
                material_count += value
            else:
                material_count -= value

    return material_count