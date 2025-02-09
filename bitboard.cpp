#include "bitboard.hpp"
#include <iostream>
#include <bitset>
#include <vector>
#include <algorithm>
#include <cstdint>

// Define pieces for white and black
constexpr uint64_t WHITE_PAWNS   = ((1ULL << 8) - 1) << 8;
constexpr uint64_t WHITE_KNIGHTS = (1ULL << 1) | (1ULL << 6);
constexpr uint64_t WHITE_BISHOPS = (1ULL << 2) | (1ULL << 5);
constexpr uint64_t WHITE_ROOKS   = (1ULL << 0) | (1ULL << 7);
constexpr uint64_t WHITE_QUEEN   = (1ULL << 3);
constexpr uint64_t WHITE_KING    = (1ULL << 4);

constexpr uint64_t BLACK_PAWNS   = ((1ULL << 8) - 1) << 48;
constexpr uint64_t BLACK_KNIGHTS = (1ULL << 57) | (1ULL << 62);
constexpr uint64_t BLACK_BISHOPS = (1ULL << 58) | (1ULL << 61);
constexpr uint64_t BLACK_ROOKS   = (1ULL << 56) | (1ULL << 63);
constexpr uint64_t BLACK_QUEEN   = (1ULL << 59);
constexpr uint64_t BLACK_KING    = (1ULL << 60);

constexpr uint64_t WHITE_PIECES = WHITE_PAWNS | WHITE_BISHOPS | WHITE_KING |
                                   WHITE_KNIGHTS | WHITE_QUEEN | WHITE_ROOKS;

constexpr uint64_t BLACK_PIECES = BLACK_PAWNS | BLACK_BISHOPS | BLACK_KING |
                                   BLACK_KNIGHTS | BLACK_QUEEN | BLACK_ROOKS;

// Define rank and files for chessboard
constexpr uint64_t RANK_1 = 0x00000000000000FF;
constexpr uint64_t RANK_2 = RANK_1 << 8;
constexpr uint64_t RANK_3 = RANK_2 << 8;
constexpr uint64_t RANK_4 = RANK_3 << 8;
constexpr uint64_t RANK_5 = RANK_4 << 8;
constexpr uint64_t RANK_6 = RANK_5 << 8;
constexpr uint64_t RANK_7 = RANK_6 << 8;
constexpr uint64_t RANK_8 = RANK_7 << 8;

constexpr uint64_t FILE_A = 0x0101010101010101;
constexpr uint64_t FILE_B = FILE_A << 1;
constexpr uint64_t FILE_C = FILE_B << 1;
constexpr uint64_t FILE_D = FILE_C << 1;
constexpr uint64_t FILE_E = FILE_D << 1;
constexpr uint64_t FILE_F = FILE_E << 1;
constexpr uint64_t FILE_G = FILE_F << 1;
constexpr uint64_t FILE_H = FILE_G << 1;

constexpr uint64_t NOT_A_FILE = ~FILE_A;
constexpr uint64_t NOT_H_FILE = ~FILE_H;
constexpr uint64_t NOT_AB_FILE = ~FILE_A & ~FILE_B;
constexpr uint64_t NOT_HG_FILE = ~FILE_H & ~FILE_G;

// Define co-ordinate map
std::vector<std::string> coord = {
    "a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1",
    "a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2",
    "a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3",
    "a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4",
    "a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5",
    "a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6",
    "a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7",
    "a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8"
};

uint64_t coordToBitboard(const std::string& square) {
    // Search for the square in the `coord` vector
    auto it = std::find(coord.begin(), coord.end(), square);

    // If the square is not found, throw an exception
    if (it == coord.end()) {
        throw std::invalid_argument("Invalid coordinate: " + square);
    }

    // Calculate the index of the square and return the corresponding bitboard
    int index = std::distance(coord.begin(), it);
    return 1ULL << index;
}

// Precomputed squares
std::vector<uint64_t> initSquares() {
    std::vector<uint64_t> squares(64);
    for (int i = 0; i < 64; ++i) {
        squares[i] = 1ULL << i;
    }
    return squares;
}
std::vector<uint64_t> SQUARES = initSquares();

// Display a bitboard
void showBitboard(uint64_t bb) {
    std::cout << "  +-----------------+\n";
    for (int row = 7; row >= 0; --row) {
        std::cout << row + 1 << " | ";
        for (int col = 0; col < 8; ++col) {
            int square = row * 8 + col;
            if (bb & SQUARES[square]) {
                std::cout << "1 ";
            } else {
                std::cout << ". ";
            }
        }
        std::cout << "|\n";
    }
    std::cout << "  +-----------------+\n";
    std::cout << "    a b c d e f g h\n\n";
}

// Set a piece on the board
uint64_t setPiece(uint64_t bb, int square) {
    return bb | SQUARES[square];
}

// Clear a piece from the board
uint64_t clearPiece(uint64_t bb, int square) {
    return bb & ~SQUARES[square];
}

// Toggle a piece on the board
uint64_t togglePiece(uint64_t bb, int square) {
    return bb ^ SQUARES[square];
}

// Function to get all occupied squares
uint64_t occupiedSquares() {
    return WHITE_PIECES | BLACK_PIECES;
}

// Check if a square is occupied
bool isOccupied(uint64_t bb, int square) {
    return bb & SQUARES[square];
}

// Get least significant bit (LSB)
int getLSB(uint64_t bb) {
    if (bb == 0) return -1;
    return __builtin_ctzll(bb);
}

// Get most significant bit (MSB)
int getMSB(uint64_t bb) {
    if (bb == 0) return -1;
    return 63 - __builtin_clzll(bb);
}

// Population count (number of set bits)
int popcount(uint64_t bb) {
    return __builtin_popcountll(bb);
}

// Flip board vertically
uint64_t flip_vertical(uint64_t bb) {
    const uint64_t k1 = 0x00FF00FF00FF00FFULL;
    const uint64_t k2 = 0x0000FFFF0000FFFFULL;

    bb = ((bb >> 8) & k1) | ((bb & k1) << 8);
    bb = ((bb >> 16) & k2) | ((bb & k2) << 16);
    bb = (bb >> 32) | (bb << 32);

    return bb;
}

// Mirror board horizontally
uint64_t mirror_horizontal(uint64_t bb) {
    const uint64_t k1 = 0x5555555555555555ULL;
    const uint64_t k2 = 0x3333333333333333ULL;
    const uint64_t k4 = 0x0F0F0F0F0F0F0F0FULL;

    bb = ((bb >> 1) & k1) | ((bb & k1) << 1);
    bb = ((bb >> 2) & k2) | ((bb & k2) << 2);
    bb = ((bb >> 4) & k4) | ((bb & k4) << 4);

    return bb;
}

// Flip board along A1-H8 diagonal
uint64_t flip_diagonal(uint64_t bb) {
    const uint64_t k1 = 0x5500550055005500ULL;
    const uint64_t k2 = 0x3333000033330000ULL;
    const uint64_t k4 = 0x0f0f0f0f00000000ULL;

    uint64_t t;
    t = k4 & (bb ^ (bb << 28));
    bb ^= t ^ (t >> 28);
    t = k2 & (bb ^ (bb << 14));
    bb ^= t ^ (t >> 14);
    t = k1 & (bb ^ (bb << 7));
    bb ^= t ^ (t >> 7);

    return bb;
}

// Flip board along A8-H1 diagonal
uint64_t flip_anti_diagonal(uint64_t bb) {
    const uint64_t k1 = 0xaa00aa00aa00aa00ULL;
    const uint64_t k2 = 0xcccc0000cccc0000ULL;
    const uint64_t k4 = 0xf0f0f0f00f0f0f0fULL;

    uint64_t t;
    t = bb ^ (bb << 36);
    bb ^= k4 & (t ^ (bb >> 36));
    t = k2 & (bb ^ (bb << 18));
    bb ^= t ^ (t >> 18);
    t = k1 & (bb ^ (bb << 9));
    bb ^= t ^ (t >> 9);

    return bb;
}

// Directions for piece movement
uint64_t north(uint64_t bb) {
    return bb << 8;
}

uint64_t south(uint64_t bb) {
    return bb >> 8;
}

uint64_t east(uint64_t bb) {
    return (bb << 1) & NOT_A_FILE;
}

uint64_t west(uint64_t bb) {
    return (bb >> 1) & NOT_H_FILE;
}

uint64_t northEast(uint64_t bb) {
    return (bb << 9) & NOT_A_FILE;
}

uint64_t northWest(uint64_t bb) {
    return (bb << 7) & NOT_H_FILE;
}

uint64_t southEast(uint64_t bb) {
    return (bb >> 7) & NOT_A_FILE;
}

uint64_t southWest(uint64_t bb) {
    return (bb >> 9) & NOT_H_FILE;
}

uint64_t northNE(uint64_t bb) {
    return (bb << 17) & NOT_A_FILE;
}

uint64_t northEE(uint64_t bb) {
    return (bb << 10) & NOT_AB_FILE;
}

uint64_t northNW(uint64_t bb) {
    return (bb << 15) & NOT_H_FILE;
}

uint64_t northWW(uint64_t bb) {
    return (bb << 6) & NOT_HG_FILE;
}

uint64_t southEE(uint64_t bb) {
    return (bb >> 6) & NOT_AB_FILE;
}

uint64_t southSE(uint64_t bb) {
    return (bb >> 15) & NOT_A_FILE;
}

uint64_t southWW(uint64_t bb) {
    return (bb >> 10) & NOT_HG_FILE;
}

uint64_t southSW(uint64_t bb) {
    return (bb >> 17) & NOT_H_FILE;
}