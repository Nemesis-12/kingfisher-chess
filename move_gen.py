import bitboard

# Push a pawn forward by a single square based on player turn
def single_push_pawn(player):
    occupied = bitboard.occupied_squares()

    if player.turn:
        return bitboard.north(bitboard.WHITE_PAWNS) & ~occupied & ~bitboard.RANK_8
    else:
        return bitboard.south(bitboard.BLACK_PAWNS) & ~occupied & ~bitboard.RANK_1

# Push a pawn forward by a two squares based on player turn
def double_push_pawn(player):
    occupied = bitboard.occupied_squares()

    if player.turn:
        single_push = bitboard.north(bitboard.WHITE_PAWNS) & ~occupied
        return (single_push << 8) & ~occupied & bitboard.RANK_4

    else:
        single_push = bitboard.south(bitboard.BLACK_PAWNS) & ~occupied
        return (single_push >> 8) & ~occupied & bitboard.RANK_5
    
# Generate an attack table for pawn attacks
def pawn_attacks():
    attacks = [[0] * 64 for _ in range(2)]

    for square in range(64):
        sq = bitboard.SQUARES[square]
        
        # Check white pawn attacks
        attacks[0][square] = (bitboard.north_east(sq) | bitboard.north_west(sq)) \
                             & ~bitboard.RANK_8

        # Check black pawn attacks
        attacks[1][square] = (bitboard.south_east(sq) | bitboard.south_west(sq)) \
                             & ~bitboard.RANK_1

    return attacks