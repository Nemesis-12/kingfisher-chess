#pragma once

#include <cstdint>
#include <vector>
#include <array>

// Bishop and Rook Occupancy Tables
extern const std::vector<int> bishopOccupancy;
extern const std::vector<int> rookOccupancy;

// Pawn Movement Functions
uint64_t singlePushPawn(bool isWhite, uint64_t occupied);
uint64_t doublePushPawn(bool isWhite, uint64_t occupied);

// Pawn Attack Generation
uint64_t generatePawnAttacks(bool isWhite, uint64_t bb);
extern std::vector<std::vector<uint64_t>> pawnAttackTable;

// Knight Attack Generation
std::array<uint64_t, 64> generateKnightAttacks();
extern std::array<uint64_t, 64> knightAttackTable;

// King Attack Generation
std::array<uint64_t, 64> generateKingAttacks();
extern std::array<uint64_t, 64> kingAttackTable;

// Bishop, Rook, and Queen Mask Generators
uint64_t generateBishopMask(int square, uint64_t blockers);
uint64_t generateRookMask(int square, uint64_t blockers);
uint64_t generateQueenMask(int square, uint64_t blockers);

extern std::array<uint64_t, 64> bishopMaskTable;
extern std::array<uint64_t, 64> rookMaskTable;
extern std::array<uint64_t, 64> queenMaskTable;

extern void initAttackTables();
extern void initMaskTables();

// Occupancy Management
uint64_t setOccupancy(int index, int bits, uint64_t attacks);

// Random Number Generators
uint32_t xorshift32RNG(uint32_t& state);
uint64_t xorshift64RNG(uint32_t& state);

// Magic Number Generator
uint64_t getMagicNumber(uint32_t& state);