#pragma once

#include <cstdint>
#include <vector>
#include <string>

// Predefined constants for white and black pieces
extern const uint64_t WHITE_PAWNS;
extern const uint64_t WHITE_KNIGHTS;
extern const uint64_t WHITE_BISHOPS;
extern const uint64_t WHITE_ROOKS;
extern const uint64_t WHITE_QUEEN;
extern const uint64_t WHITE_KING;

extern const uint64_t BLACK_PAWNS;
extern const uint64_t BLACK_KNIGHTS;
extern const uint64_t BLACK_BISHOPS;
extern const uint64_t BLACK_ROOKS;
extern const uint64_t BLACK_QUEEN;
extern const uint64_t BLACK_KING;

// Combined piece bitboards
extern const uint64_t WHITE_PIECES;
extern const uint64_t BLACK_PIECES;

// Rank and file bitboards
extern const uint64_t RANK_1, RANK_2, RANK_3, RANK_4, RANK_5, RANK_6, RANK_7, RANK_8;
extern const uint64_t FILE_A, FILE_B, FILE_C, FILE_D, FILE_E, FILE_F, FILE_G, FILE_H;
extern const uint64_t NOT_A_FILE, NOT_H_FILE, NOT_AB_FILE, NOT_HG_FILE;

// Coordinate map
extern std::vector<std::string> coord;
uint64_t coordToBitboard(const std::string& square);

// Precomputed squares
extern std::vector<uint64_t> SQUARES;

// Functions
void showBitboard(uint64_t bb);
uint64_t setPiece(uint64_t bb, int square);
uint64_t clearPiece(uint64_t bb, int square);
uint64_t togglePiece(uint64_t bb, int square);
uint64_t occupiedSquares();
bool isOccupied(uint64_t bb, int square);
int getLSB(uint64_t bb);
int getMSB(uint64_t bb);
int popcount(uint64_t bb);

uint64_t flip_vertical(uint64_t bb);
uint64_t mirror_horizontal(uint64_t bb);
uint64_t flip_diagonal(uint64_t bb);
uint64_t flip_anti_diagonal(uint64_t bb);

// Directional movement functions
uint64_t north(uint64_t bb);
uint64_t south(uint64_t bb);
uint64_t east(uint64_t bb);
uint64_t west(uint64_t bb);
uint64_t northEast(uint64_t bb);
uint64_t northWest(uint64_t bb);
uint64_t southEast(uint64_t bb);
uint64_t southWest(uint64_t bb);
uint64_t northNE(uint64_t bb);
uint64_t northEE(uint64_t bb);
uint64_t northNW(uint64_t bb);
uint64_t northWW(uint64_t bb);
uint64_t southEE(uint64_t bb);
uint64_t southSE(uint64_t bb);
uint64_t southWW(uint64_t bb);
uint64_t southSW(uint64_t bb);