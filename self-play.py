import chess
from kingfisher import Kingfisher
import chess.polyglot
from player import Player
import chess.pgn
from export_pgn import export_pgn

# Print the move played and the side
def print_move(player, move, board):
    piece = board.piece_at(move.from_square)

    player_name = "White" if player == chess.WHITE else "Black"
    print(f"{player_name} plays {piece_unicode[str(piece)]} {move.uci()[-2:]}")

# Print chess board
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
    print()

# Define variables
board = chess.Board()
game = chess.pgn.Game()
node = game

bots = {
    chess.WHITE: Kingfisher(),
    chess.BLACK: Kingfisher()
}

piece_unicode = {
    "r": "♜", "n": "♞", "b": "♝", "q": "♛", "k": "♚", "p": "♟",
    "R": "♖", "N": "♘", "B": "♗", "Q": "♕", "K": "♔", "P": "♙", "None": " . "
}

transposition_table = {}

# Play the game until it is over
print_board(board)
while not board.is_game_over():
    curr_player = Player(board)

    move = bots[curr_player.player].select_move(board)
    print_move(curr_player.player, move, board)

    board.push(move)
    print_board(board)
    print()

    node = node.add_variation(move)

    # Use zobrist hash to save board state
    zobrist_hash = chess.polyglot.zobrist_hash(board)
    if zobrist_hash not in transposition_table:
        transposition_table[zobrist_hash] = {
            "position_count": 1
        }
    else:
        transposition_table[zobrist_hash]["position_count"] += 1

# Print board after game ends
print_board(board)
export_pgn(game)

# Display outcome of the game
if board.is_checkmate():
    print(f"Checkmate! {curr_player.player_name} wins!")
elif board.is_stalemate():
    print("Stalemate! It's a draw!")
elif board.is_insufficient_material():
    print("Draw: Insufficient material!")
elif board.is_fivefold_repetition():
    print("Draw: Fivefold repetition!")