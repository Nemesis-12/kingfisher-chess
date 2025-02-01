def show_bitboard(bitboard):
    for row in range(7, -1, -1):
        for col in range(8):
            square = row * 8 + col
            if (bitboard >> square) & 1:
                print(1, end=" ")
            else:
                print(".", end=" ")
        print()
    print()

def set_piece(bitboard, square):
    return bitboard | (1 << square)

def clear_piece(bitboard, square):
    return bitboard & ~(1 << square)

def toggle_piece(bitboard, square):
    return bitboard ^ (1 << square)

bitboard = 0
bitboard = set_piece(bitboard, 3)
bitboard = set_piece(bitboard, 32)
show_bitboard(bitboard)

bitboard = clear_piece(bitboard, 3)
show_bitboard(bitboard)

bitboard = toggle_piece(bitboard, 10)
show_bitboard(bitboard)