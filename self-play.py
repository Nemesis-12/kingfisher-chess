import chess
from kingfisher import Kingfisher
import time
import chess.polyglot
from player import Player
from evaluation import evaluation

def print_move(player, move, board, eval_function):
    piece = board.piece_at(move.from_square)

    player_name = "White" if player == chess.WHITE else "Black"
    print(f"{player_name} plays {piece_unicode[str(piece)]} {move.uci()[-2:]}")
    print(f"Evaluation: {eval_function}")

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

while not board.is_game_over():
    time.sleep(0.3)

    print_board(board)

    curr_player = Player(board)

    move = bots[curr_player.player].select_move(board)
    board.push(move)
    score = evaluation(board, curr_player)
    
    print_move(curr_player.player, move, board, score)
    print()

    zobrist_hash = chess.polyglot.zobrist_hash(board)
    if zobrist_hash not in transposition_table:
        transposition_table[zobrist_hash] = {
            "position_count": 1
        }
    else:
        transposition_table[zobrist_hash]["position_count"] += 1

print_board(board)

if board.is_checkmate():
    print(f"Checkmate! {curr_player.player_name} wins!")
elif board.is_stalemate():
    print("Stalemate! It's a draw!")
elif board.is_insufficient_material():
    print("Draw: Insufficient material!")
elif board.is_fivefold_repetition():
    print("Draw: Fivefold repetition!")