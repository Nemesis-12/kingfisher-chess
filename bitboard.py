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

# Define rank and files for chessboard
RANK_1 = RANK_1 = 0x00000000000000FF
RANK_2 = RANK_1 << 8
RANK_3 = RANK_2 << 8
RANK_4 = RANK_3 << 8
RANK_5 = RANK_4 << 8
RANK_6 = RANK_5 << 8
RANK_7 = RANK_6 << 8
RANK_8 = RANK_7 << 8

FILE_1 = 0x0101010101010101
FILE_2 = FILE_1 << 1
FILE_3 = FILE_2 << 2
FILE_4 = FILE_3 << 3
FILE_5 = FILE_4 << 4
FILE_6 = FILE_5 << 5
FILE_7 = FILE_6 << 6
FILE_8 = FILE_7 << 7

# Print a bitboard
def show_bitboard(bitboard):
    print("  +-----------------+")

    for row in range(7, -1, -1):
        print(f"{row + 1} |", end=" ")
        for col in range(8):
            square = row * 8 + col
            if (bitboard >> square) & 1:
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
    return bitboard | (1 << square)

# Clear the piece from the board if it is occupied
def clear_piece(bitboard, square):
    return bitboard & ~(1 << square)

# Toggle a piece
def toggle_piece(bitboard, square):
    return bitboard ^ (1 << square)

# Check if square is occupied
def is_occupied(bitboard, square):
    return (bitboard >> square) & 1

# Function to get all occupied squares
def occupied_squares():
    return (WHITE_PAWNS | BLACK_PAWNS |
            WHITE_KNIGHTS | BLACK_KNIGHTS |
            WHITE_BISHOPS | BLACK_BISHOPS |
            WHITE_ROOKS | BLACK_ROOKS |
            WHITE_QUEEN | BLACK_QUEEN |
            WHITE_KING | BLACK_KING)

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
    count = 0
    while bitboard:
        bitboard &= bitboard - 1
        count += 1
    return count

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

# Functions for moving one step in any direction
def north(bitboard):
    return bitboard << 8

def south(bitboard):
    return bitboard >> 8

def north_east(bitboard):
    return bitboard << 9

def south_east(bitboard):
    return bitboard >> 7

def north_west(bitboard):
    return bitboard << 7

def south_west(bitboard):
    return bitboard >> 9

def east(bitboard):
    return bitboard << 1

def west(bitboard):
    return bitboard >> 1
