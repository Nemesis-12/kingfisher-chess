#pragma once

#include <cstdint>
#include <vector>

// Bishop and Rook Occupancy Tables
extern const std::vector<int> bishopOccupancy;
extern const std::vector<int> rookOccupancy;

// Pawn Movement Functions
uint64_t singlePushPawn(bool isWhite, uint64_t occupied);
uint64_t doublePushPawn(bool isWhite, uint64_t occupied);

// Pawn Attack Generation
uint64_t generatePawnAttacks(bool isWhite, uint64_t bb);

// Knight Attack Generation
std::vector<uint64_t> generateKnightAttacks();

// King Attack Generation
std::vector<uint64_t> generateKingAttacks();

// Bishop, Rook, and Queen Mask Generators
uint64_t generateBishopMask(int square, uint64_t blockers);
uint64_t generateRookMask(int square, uint64_t blockers);
uint64_t initQueenMask(int square, uint64_t blockers);

// Occupancy Management
uint64_t setOccupancy(int index, int bits, uint64_t attacks);

// Random Number Generators
uint32_t xorshift32RNG(uint32_t& state);
uint64_t xorshift64RNG(uint32_t& state);

// Magic Number Generator
uint64_t getMagicNumber(uint32_t& state);