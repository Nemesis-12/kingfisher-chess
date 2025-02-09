#include "bitboard.hpp"
#include "move_gen.hpp"
#include <vector>
#include <cstdlib>

// Bishop and rook occupancy tables
const std::vector<int> bishopOccupancy = {
    6, 6, 6, 6, 6, 6, 6, 6,
    6, 5, 5, 5, 5, 5, 5, 6,
    6, 5, 7, 7, 7, 7, 5, 6,
    6, 5, 7, 9, 9, 7, 5, 6,
    6, 5, 7, 9, 9, 7, 5, 6,
    6, 5, 7, 7, 7, 7, 5, 6,
    6, 5, 5, 5, 5, 5, 5, 6,
    6, 6, 6, 6, 6, 6, 6, 6
};

const std::vector<int> rookOccupancy = {
    12, 11, 11, 11, 11, 11, 11, 12,
    11, 10, 10, 10, 10, 10, 10, 11,
    11, 10, 10, 10, 10, 10, 10, 11,
    11, 10, 10, 10, 10, 10, 10, 11,
    11, 10, 10, 10, 10, 10, 10, 11,
    11, 10, 10, 10, 10, 10, 10, 11,
    11, 10, 10, 10, 10, 10, 10, 11,
    12, 11, 11, 11, 11, 11, 11, 12
};

// Push a pawn forward by one square
uint64_t singlePushPawn(bool isWhite, uint64_t occupied) {
    if (isWhite) {
        return north(WHITE_PAWNS) & ~occupied & ~RANK_8;
    } else {
        return south(BLACK_PAWNS) & ~occupied & ~RANK_1;
    }
}

// Push a pawn forward by two squares
uint64_t doublePushPawn(bool isWhite, uint64_t occupied) {
    if (isWhite) {
        uint64_t singlePush = north(WHITE_PAWNS) & ~occupied;
        return (singlePush << 8) & ~occupied & RANK_4;
    } else {
        uint64_t singlePush = south(BLACK_PAWNS) & ~occupied;
        return (singlePush >> 8) & ~occupied & RANK_5;
    }
}

// Generate pawn attacks
uint64_t generatePawnAttacks(bool isWhite, uint64_t bb) {
    if (isWhite) {
        return (northEast(bb) | northWest(bb)) & ~RANK_8;
    } else {
        return (southWest(bb) | southEast(bb)) & ~RANK_1;
    }
}

// Generate knight attacks
std::vector<uint64_t> generateKnightAttacks() {
    std::vector<uint64_t> attacks(64, 0);

    for (int sq = 0; sq < 64; ++sq) {
        uint64_t square = SQUARES[sq];
        attacks[sq] = (northNE(square) | northNW(square) |
                       northEE(square) | northWW(square) |
                       southSE(square) | southSW(square) |
                       southEE(square) | southWW(square)) &
                      ~(RANK_1 | RANK_8 | FILE_A | FILE_H);
    }

    return attacks;
}


// Generate king attacks
std::vector<uint64_t> generateKingAttacks() {
    std::vector<uint64_t> attacks(64, 0);

    for (int sq = 0; sq < 64; ++sq) {
        uint64_t square = SQUARES[sq];
        attacks[sq] = north(square) | south(square) |
                      east(square) | west(square) |
                      northEast(square) | northWest(square) |
                      southEast(square) | southWest(square);
    }

    return attacks;
}

// Generate bishop mask
uint64_t generateBishopMask(int square, uint64_t blockers) {
    uint64_t mask = 0;
    std::vector<uint64_t (*)(uint64_t)> directions = { northEast, northWest, southEast, southWest };

    for (auto direction : directions) {
        uint64_t bb = SQUARES[square];
        while (true) {
            bb = direction(bb);
            if (bb == 0) break;
            mask |= bb;
            if (bb & blockers) break;
        }
    }

    return mask;
}

// Generate rook mask
uint64_t generateRookMask(int square, uint64_t blockers) {
    uint64_t mask = 0;
    std::vector<uint64_t (*)(uint64_t)> directions = { north, south, east, west };

    for (auto direction : directions) {
        uint64_t bb = SQUARES[square];
        while (true) {
            bb = direction(bb);
            if (bb == 0) break;
            mask |= bb;
            if (bb & blockers) break;
        }
    }

    return mask;
}

// Generate queen mask
uint64_t initQueenMask(int square, uint64_t blockers) {
    return generateBishopMask(square, blockers) | generateRookMask(square, blockers);
}

// Set occupancy bits
uint64_t setOccupancy(int index, int bits, uint64_t attacks) {
    uint64_t occupancy = 0;

    for (int i = 0; i < bits; ++i) {
        int square = getLSB(attacks);
        attacks = clearPiece(attacks, square);

        if (index & (1 << i)) {
            occupancy |= 1ULL << square;
        }
    }

    return occupancy;
}

// Pseudo-random number generator (32-bit)
uint32_t xorshift32RNG(uint32_t& state) {
    state ^= state << 13;
    state ^= state >> 7;
    state ^= state << 17;
    return state & 0xFFFFFFFF;
}

// Pseudo-random number generator (64-bit)
uint64_t xorshift64RNG(uint32_t& state) {
    uint64_t num1 = xorshift32RNG(state) & 0xFFFF;
    uint64_t num2 = xorshift32RNG(state) & 0xFFFF;
    uint64_t num3 = xorshift32RNG(state) & 0xFFFF;
    uint64_t num4 = xorshift32RNG(state) & 0xFFFF;

    return (num1 << 48) | (num2 << 32) | (num3 << 16) | num4;
}

// Generate magic number
uint64_t getMagicNumber(uint32_t& state) {
    return xorshift64RNG(state) & xorshift64RNG(state) & xorshift64RNG(state);
}