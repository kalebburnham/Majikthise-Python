import sys
sys.path.append('../majikthise')

import unittest

from bitboard import *
from board import *
from movegen import *
from rays import *

class PositionTests(unittest.TestCase):
    def test_score_StartingPosition(self):
        position = Position()
        self.assertEqual(position.score(), 0)

    def test_score_e4d5exd5(self):
        # This test will likely break when mobility is added to eval function.
        position = Position()
        position.board.whitePawns = (SECOND_RANK & ~Square.E2.bitboard()) | Square.D5.bitboard()
        position.board.blackPawns = (SEVENTH_RANK & ~Square.D7.bitboard())
        position.sideToMove = Color.BLACK

        # White has 2 doubled pawns and is up a pawn. Score is still even.
        self.assertEqual(position.score(), 0)


if __name__ == '__main__':
	unittest.main()