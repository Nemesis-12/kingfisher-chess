# Define pieces for white and black
WHITE_PAWNS   = ((1 << 8) - 1) << 8
WHITE_KNIGHTS = (1 << 1) | (1 << 6)
WHITE_BISHOPS = (1 << 2) | (1 << 5)
WHITE_ROOKS   = (1 << 0) | (1 << 7)
WHITE_QUEEN   = (1 << 3)
WHITE_KING    = (1 << 4)

BLACK_PAWNS   = ((1 << 8) - 1) << 48
BLACK_KNIGHTS = (1 << 57) | (1 << 62)
BLACK_BISHOPS = (1 << 58) | (1 << 61)
BLACK_ROOKS   = (1 << 56) | (1 << 63)
BLACK_QUEEN   = (1 << 59)
BLACK_KING    = (1 << 60)

WHITE_PIECES = WHITE_PAWNS | WHITE_BISHOPS | WHITE_KING | \
               WHITE_KNIGHTS | WHITE_QUEEN | WHITE_ROOKS

BLACK_PIECES = BLACK_PAWNS | BLACK_BISHOPS | BLACK_KING | \
               BLACK_KNIGHTS | BLACK_QUEEN | BLACK_ROOKS

# Define rank and files for chessboard
RANK_1 = 0x00000000000000FF
RANK_2 = RANK_1 << 8
RANK_3 = RANK_2 << 8
RANK_4 = RANK_3 << 8
RANK_5 = RANK_4 << 8
RANK_6 = RANK_5 << 8
RANK_7 = RANK_6 << 8
RANK_8 = RANK_7 << 8

FILE_A = 0x0101010101010101
FILE_B = FILE_A << 1
FILE_C = FILE_B << 2
FILE_D = FILE_C << 3
FILE_E = FILE_D << 4
FILE_F = FILE_E << 5
FILE_G = FILE_F << 6
FILE_H = FILE_G << 7

# Generate pre-computed squares
SQUARES = [1 << square for square in range(64)]

# Define actions that a player can take
class Move():
    def __init__(self, square=None, is_resign=False):
        assert (square is not None) ^ is_resign
        self.square = square
        self.play = self.square is not None
        self.is_resign = is_resign

    @classmethod
    def play(cls, square):
        return Move(square=square)
    
    @classmethod
    def is_resign(cls):
        return Move(is_resign=True)

# Print a bitboard
def show_bitboard(bitboard):
    print("  +-----------------+")

    for row in range(7, -1, -1):
        print(f"{row + 1} |", end=" ")
        for col in range(8):
            square = row * 8 + col
            if bitboard & SQUARES[square]:
                print(1, end=" ")
            else:
                print(".", end=" ")
        print(f"|", end=" ")
        print()

    print("  +-----------------+")
    print("    a b c d e f g h")
    print()

# Set a piece on the board
def set_piece(bitboard, square):
    return bitboard | SQUARES[square]

# Clear the piece from the board if it is occupied
def clear_piece(bitboard, square):
    return bitboard & ~SQUARES[square]
# Toggle a piece
def toggle_piece(bitboard, square):
    return bitboard ^ SQUARES[square]

# Check if square is occupied
def is_occupied(bitboard, square):
    return bitboard & SQUARES[square]

# Function to get all occupied squares
def occupied_squares():
    return (WHITE_PIECES | BLACK_PIECES)

# Find LSB in a bitboard
def get_LSB(bitboard):
    if bitboard == 0:
        return -1
    return (bitboard & -bitboard).bit_length() - 1

# Find MSB in a bitboard
def get_MSB(bitboard):
    if bitboard == 0:
        return -1
    return bitboard.bit_length() - 1

# Define population count (check no of pieces)
def popcount(bitboard):
    return bin(bitboard).count("1")

# Flip board vertically
def flip_vertical(bitboard):
    k1 = 0x00FF00FF00FF00FF
    k2 = 0x0000FFFF0000FFFF

    bitboard = ((bitboard >>  8) & k1) | ((bitboard & k1) <<  8)
    bitboard = ((bitboard >> 16) & k2) | ((bitboard & k2) << 16)
    bitboard = (bitboard >> 32) | (bitboard << 32)

    return bitboard

# Mirror board horizontally
def mirror_horizontal(bitboard):
    k1 = 0x5555555555555555
    k2 = 0x3333333333333333
    k4 = 0x0F0F0F0F0F0F0F0F

    bitboard = ((bitboard >> 1) & k1) | ((bitboard & k1) << 1)
    bitboard = ((bitboard >> 2) & k2) | ((bitboard & k2) << 2)
    bitboard = ((bitboard >> 4) & k4) | ((bitboard & k4) << 4)

    return bitboard

# Flip board along A1-H8 diagonal
def flip_diagonal(bitboard):
    k1 = 0x5500550055005500
    k2 = 0x3333000033330000
    k4 = 0x0f0f0f0f00000000

    t = k4 & (bitboard ^ (bitboard << 28))
    bitboard ^= t ^ (t >> 28)
    t = k2 & (bitboard ^ (bitboard << 14))
    bitboard ^= t ^ (t >> 14)
    t = k1 & (bitboard ^ (bitboard << 7))
    bitboard ^= t ^ (t >> 7)

    return bitboard

# Flip board along A8-H1 diagonal
def flip_anti_diagonal(bitboard):
    k1 = 0xaa00aa00aa00aa00
    k2 = 0xcccc0000cccc0000
    k4 = 0xf0f0f0f00f0f0f0f

    t = bitboard ^ (bitboard << 36)
    bitboard ^= k4 & (t ^ (bitboard >> 36))
    t = k2 & (bitboard ^ (bitboard << 18))
    bitboard ^= t ^ (t >> 18)
    t = k1 & (bitboard ^ (bitboard << 9))
    bitboard ^= t ^ (t >> 9)

    return bitboard

# Functions for moving one step in any direction
def north(bitboard):
    return bitboard << 8

def south(bitboard):
    return bitboard >> 8

def north_east(bitboard):
    return (bitboard << 9) & ~FILE_A

def south_east(bitboard):
    return (bitboard >> 7) & ~FILE_A

def north_west(bitboard):
    return (bitboard << 7) & ~FILE_H

def south_west(bitboard):
    return (bitboard >> 9) & ~FILE_H

def east(bitboard):
    return (bitboard << 1) & ~FILE_A

def west(bitboard):
    return (bitboard >> 1) & ~FILE_H