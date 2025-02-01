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

def is_occupied(bitboard, square):
    return (bitboard >> square) & 1