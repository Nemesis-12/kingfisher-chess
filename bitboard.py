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
FILE_C = FILE_B << 1
FILE_D = FILE_C << 1
FILE_E = FILE_D << 1
FILE_F = FILE_E << 1
FILE_G = FILE_F << 1
FILE_H = FILE_G << 1

NOT_A_FILE = ~FILE_A
NOT_H_FILE = ~FILE_H
NOT_AB_FILE = ~FILE_A & ~FILE_B
NOT_HG_FILE = ~FILE_H & ~FILE_G

# Generate pre-computed squares
SQUARES = [1 << square for square in range(64)]

# Define co-ordinate map
coord = [
    "a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1",
    "a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2",
    "a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3",
    "a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4",
    "a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5",
    "a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6",
    "a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7",
    "a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8",
]

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
def show_bitboard(bb):
    print("  +-----------------+")

    for row in range(7, -1, -1):
        print(f"{row + 1} |", end=" ")
        for col in range(8):
            square = row * 8 + col
            if bb & SQUARES[square]:
                print(1, end=" ")
            else:
                print(".", end=" ")
        print(f"|", end=" ")
        print()

    print("  +-----------------+")
    print("    a b c d e f g h")
    print()

# Set a piece on the board
def set_piece(bb, square):
    return bb | SQUARES[square]

# Clear the piece from the board if it is occupied
def clear_piece(bb, square):
    return bb & ~SQUARES[square]
# Toggle a piece
def toggle_piece(bb, square):
    return bb ^ SQUARES[square]

# Check if square is occupied
def is_occupied(bb, square):
    return bb & SQUARES[square]

# Function to get all occupied squares
def occupied_squares():
    return (WHITE_PIECES | BLACK_PIECES)

# Find LSB in a bitboard
def get_LSB(bb):
    if bb == 0:
        return -1
    return (bb & -bb).bit_length() - 1

# Find MSB in a bitboard
def get_MSB(bb):
    if bb == 0:
        return -1
    return bb.bit_length() - 1

# Define population count (check no of pieces)
def popcount(bb):
    return bin(bb).count("1")

# Flip board vertically
def flip_vertical(bb):
    k1 = 0x00FF00FF00FF00FF
    k2 = 0x0000FFFF0000FFFF

    bb = ((bb >>  8) & k1) | ((bb & k1) <<  8)
    bb = ((bb >> 16) & k2) | ((bb & k2) << 16)
    bb = (bb >> 32) | (bb << 32)

    return bb

# Mirror board horizontally
def mirror_horizontal(bb):
    k1 = 0x5555555555555555
    k2 = 0x3333333333333333
    k4 = 0x0F0F0F0F0F0F0F0F

    bb = ((bb >> 1) & k1) | ((bb & k1) << 1)
    bb = ((bb >> 2) & k2) | ((bb & k2) << 2)
    bb = ((bb >> 4) & k4) | ((bb & k4) << 4)

    return bb

# Flip board along A1-H8 diagonal
def flip_diagonal(bb):
    k1 = 0x5500550055005500
    k2 = 0x3333000033330000
    k4 = 0x0f0f0f0f00000000

    t = k4 & (bb ^ (bb << 28))
    bb ^= t ^ (t >> 28)
    t = k2 & (bb ^ (bb << 14))
    bb ^= t ^ (t >> 14)
    t = k1 & (bb ^ (bb << 7))
    bb ^= t ^ (t >> 7)

    return bb

# Flip board along A8-H1 diagonal
def flip_anti_diagonal(bb):
    k1 = 0xaa00aa00aa00aa00
    k2 = 0xcccc0000cccc0000
    k4 = 0xf0f0f0f00f0f0f0f

    t = bb ^ (bb << 36)
    bb ^= k4 & (t ^ (bb >> 36))
    t = k2 & (bb ^ (bb << 18))
    bb ^= t ^ (t >> 18)
    t = k1 & (bb ^ (bb << 9))
    bb ^= t ^ (t >> 9)

    return bb

# Define directions for pieces
def north(bb):
    return bb << 8

def south(bb):
    return bb >> 8

def east(bb):
    return (bb << 1) & NOT_A_FILE

def west(bb):
    return (bb >> 1) & NOT_H_FILE

def north_east(bb):
    return (bb << 9) & NOT_A_FILE

def north_west(bb):
    return (bb << 7) & NOT_H_FILE

def south_east(bb):
    return (bb >> 7) & NOT_A_FILE

def south_west(bb):
    return (bb >> 9) & NOT_H_FILE

def north_ne(bb):
    return (bb << 17) & NOT_A_FILE

def north_ee(bb):
    return (bb << 10) & NOT_AB_FILE

def north_nw(bb):
    return (bb << 15) & NOT_H_FILE

def north_ww(bb):
    return (bb << 6) & NOT_HG_FILE

def south_ee(bb):
    return (bb >> 6) & NOT_AB_FILE

def south_se(bb):
    return (bb >> 15) & NOT_A_FILE

def south_ww(bb):
    return (bb >> 10) & NOT_HG_FILE

def south_sw(bb):
    return (bb >> 17) & NOT_H_FILE