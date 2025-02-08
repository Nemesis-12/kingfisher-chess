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
        attacks[0] = bitboard.north_east(bb) | bitboard.north_west(bb)

    # Check black pawn attacks
    elif player == 1:
        attacks[1] = bitboard.south_west(bb) | bitboard.south_east(bb)

    return attacks

# Initialize attack tables
def init_attack_table_pawn():
    attacks = [[0 for _ in range(64)] for _ in range(2)]

    for sq in range(64):
        square = bitboard.SQUARES[sq]
        attacks[0][sq] = generate_pawn_attacks(0, square)[0]
        attacks[1][sq] = generate_pawn_attacks(1, square)[1]

    return attacks

# Generate an attack table for knight attacks
def generate_knight_attacks():
    attacks = [0] * 64
    
    for sq in range(64):
        square = bitboard.SQUARES[sq]
        attacks[sq] = bitboard.north_ne(square) | bitboard.north_nw(square) | \
                      bitboard.north_ee(square) | bitboard.north_ww(square) | \
                      bitboard.south_se(square) | bitboard.south_sw(square) | \
                      bitboard.south_ee(square) | bitboard.south_ww(square)

    return attacks

# Generate an attack table for king attacks
def generate_king_attacks():
    attacks = [0] * 64

    for sq in range(64):
        square = bitboard.SQUARES[sq]
        attacks[sq] = bitboard.north(square) | bitboard.south(square) | \
                      bitboard.east(square) | bitboard.west(square) | \
                      bitboard.north_east(square) | bitboard.north_west(square) | \
                      bitboard.south_east(square) | bitboard.south_west(square)
        
    return attacks

# Generate bishop masks
def generate_bishop_mask(square):
    mask = 0
    file_mask = square % 8
    rank_mask = square // 8

    for i in range(1, 7):
        if (rank_mask + i <= 6) & (file_mask + i <= 6):
            mask |= bitboard.SQUARES[(rank_mask + i) * 8 + (file_mask + i)]
        if rank_mask - i >= 1 and file_mask - i >= 1:
            mask |= bitboard.SQUARES[(rank_mask - i) * 8 + (file_mask - i)]
        if rank_mask + i <= 6 and file_mask - i >= 1:
            mask |= bitboard.SQUARES[(rank_mask + i) * 8 + (file_mask - i)]
        if rank_mask - i >= 1 and file_mask + i <= 6: 
            mask |= bitboard.SQUARES[(rank_mask - i) * 8 + (file_mask + i)]

    return mask

# Initialize bishop mask table
def init_bishop_mask():
    mask = [0] * 64

    for sq in range(64):
        mask[sq] = generate_bishop_mask(sq)

    return mask

# Generate rook masks
def generate_rook_mask(square):
    mask = 0
    file_mask = square % 8
    rank_mask = square // 8

    for i in range(1, 7):
        if rank_mask + i <= 6:
            mask |= bitboard.SQUARES[(rank_mask + i) * 8 + file_mask]
        if rank_mask - i >= 1:
            mask |= bitboard.SQUARES[(rank_mask - i) * 8 + file_mask]
        if file_mask - i >= 1:
            mask |= bitboard.SQUARES[rank_mask * 8 + (file_mask - i)]
        if file_mask + i <= 6: 
            mask |= bitboard.SQUARES[rank_mask * 8 + (file_mask + i)]

    return mask

# Initialize rook mask table
def init_rook_mask():
    mask = [0] * 64

    for sq in range(64):
        mask[sq] = generate_rook_mask(sq)

    return mask