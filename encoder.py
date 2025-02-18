import numpy as np
import chess

class Encoder:
    def __init__(self):
        pass

    def encode(self, board):
        encoded_board = np.zeros((6, 8, 8), dtype=np.float32)

        encoded_pieces = {
            chess.PAWN: 0,
            chess.KNIGHT: 1,
            chess.BISHOP: 2,
            chess.ROOK: 3,
            chess.QUEEN: 4,
            chess.KING: 5
        }

        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                encoded_piece = encoded_pieces[piece.piece_type]
                row = chess.square_rank(square)
                col = chess.square_file(square)
                encoded_board[encoded_piece, row, col] = 1.0 if chess.WHITE else -1.0

        return encoded_board
    
    def decode(self, encoded_board):
        board = chess.Board()
        board.clear()

        decoded_pieces = {
            0: chess.PAWN,
            1: chess.KNIGHT,
            2: chess.BISHOP,
            3: chess.ROOK,
            4: chess.QUEEN,
            5: chess.KING
        }

        for square in chess.SQUARES:
            row = chess.square_rank(square)
            col = chess.square_file(square)
            for piece, piece_type in decoded_pieces.items():
                piece_color = encoded_board[piece, row, col]
                if piece_color != 0:
                    color = chess.WHITE if piece_color == 1.0 else chess.BLACK
                    board.set_piece_at(square, chess.Piece(piece_type, color))

        return board