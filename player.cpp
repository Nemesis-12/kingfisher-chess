#include "bitboard.hpp"

class Player {
public:
    Player() : turn(true) {}

    bool playerTurn() {
        turn = !turn;
        return turn;
    }

private:
    bool turn;
};