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
def generate_pawn_attacks(player, bb):
    attacks = [0, 0]
        
    # Check white pawn attacks
    if player == 0:
        attacks[0] = bitboard.north_west(bb) | bitboard.north_east(bb)

    # Check black pawn attacks
    else:
        attacks[1] = bitboard.south_east(bb) | bitboard.south_west(bb)

    return attacks

# Initialize attack tables
def init_attack_pawn_table():
    attacks = [[0 for _ in range(64)] for _ in range(2)]

    for sq in range(64):
        square = bitboard.SQUARES[sq]
        attacks[0][sq] = generate_pawn_attacks(0, square)[0]
        attacks[1][sq] = generate_pawn_attacks(1, square)[1]

    return attacks
