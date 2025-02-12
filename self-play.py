import chess
from kingfisher import Kingfisher
import time
import chess.polyglot

board = chess.Board()

bots = {
    chess.WHITE: Kingfisher(),
    chess.BLACK: Kingfisher()
}

piece_unicode = {
    "r": "♜", "n": "♞", "b": "♝", "q": "♛", "k": "♚", "p": "♟",
    "R": "♖", "N": "♘", "B": "♗", "Q": "♕", "K": "♔", "P": "♙", None: " . "
}

transposition_table = {}

def print_move(player, move, board):
    piece = board.piece_at(move.from_square)

    player_name = "White" if player == chess.WHITE else "Black"
    print(f"{player_name} plays {piece_unicode[str(piece)]} {move.uci()[-2:]}")

def print_board(board):
    print("    a   b   c   d   e   f   g   h")
    print("  +" + "---+" * 8)

    for rank in range(8, 0, -1):
        row = []
        for file in range(8):
            square = chess.square(file, rank - 1)
            piece = board.piece_at(square)
            row.append(f" {piece_unicode[str(piece)] if piece else ' '} ")

        print(f"{rank} |" + "|".join(row) + f"| {rank}")
        print("  +" + "---+" * 8)

    print("    a   b   c   d   e   f   g   h")

while not board.is_game_over():
    time.sleep(0.3)

    print_board(board)

    player = chess.WHITE if board.turn else chess.BLACK

    bot_move = bots[player].select_move(board)
    print_move(player, bot_move, board)

    board.push(bot_move)
    print()

    zobrist_hash = chess.polyglot.zobrist_hash(board)

    # Add the Zobrist hash to the transposition table
    if zobrist_hash not in transposition_table:
        transposition_table[zobrist_hash] = {
            "position_count": 1
        }
    else:
        transposition_table[zobrist_hash]["position_count"] += 1

print_board(board)

if board.is_checkmate():
        print(f"Checkmate! {player} wins!")
elif board.is_stalemate():
    print("Stalemate! It's a draw!")
elif board.is_insufficient_material():
    print("Draw: Insufficient material!")
elif board.is_fivefold_repetition():
    print("Draw: Fivefold repetition!")