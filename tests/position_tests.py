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

class MakeMoveTests(unittest.TestCase):
    def test_MakeMoveOnBoard_e4(self):
        position = Position()
        move = Move(Square.E2, Square.E4)
        position.board.makeMove(move)

        expected = CBoard('rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1')
        self.assertEqual(position.board, expected)

    def test_BoardMakeMove_e4(self):
        position = Position()
        move = Move(Square.E2, Square.E4)
        position.board.makeMove(move)
        position.board.unmakeMove(move)

        expected = CBoard('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
        self.assertEqual(position.board, expected)

    def test_BoardMakeMove_e4e5(self):
        position = Position()
        whiteMove = Move(Square.E2, Square.E4)
        blackMove = Move(Square.E7, Square.E5)
        position.board.makeMove(whiteMove)
        position.board.makeMove(blackMove)

        expected = CBoard('rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1')
        self.assertEqual(position.board, expected)

    def test_BoardUnMakeMove_e4e5(self):
        position = Position()
        whiteMove = Move(Square.E2, Square.E4)
        blackMove = Move(Square.E7, Square.E5)
        position.board.makeMove(whiteMove)
        position.board.makeMove(blackMove)
        position.board.unmakeMove(blackMove)
        position.board.unmakeMove(whiteMove)

        expected = CBoard('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
        self.assertEqual(position.board, expected)

    def test_PositionMakeMove_e4(self):
        position = Position()
        move = Move(Square.E2, Square.E4)
        position.makeMove(move)

        expected = Position('rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1')
        self.assertEqual(position, expected)

    def test_PositionUnmakeMove_e4e5(self):
        position = Position()
        whiteMove = Move(Square.E2, Square.E4)
        blackMove = Move(Square.E7, Square.E5)
        position.makeMove(whiteMove)
        position.makeMove(blackMove)
        position.unmakeMove(blackMove)
        position.unmakeMove(whiteMove)

        expected = Position()
        self.assertEqual(position, expected)

    def test_KingsideCastle_makeMove(self):
        position = Position('rnbqk2r/ppppbppp/5n2/4p3/4P3/5N2/PPPPBPPP/RNBQK2R w KQkq - 0 1')
        position.makeMove(Move(Square.E1, Square.G1, flag=0x02))
        position.makeMove(Move(Square.E8, Square.G8, flag=0x02))

        expected = Position('rnbq1rk1/ppppbppp/5n2/4p3/4P3/5N2/PPPPBPPP/RNBQ1RK1 w - - 0 1')

        self.assertEqual(position, expected)

    def test_KingsideCastle_unmakeMove(self):
        position = Position('rnbqk2r/ppppbppp/5n2/4p3/4P3/5N2/PPPPBPPP/RNBQK2R w KQkq - 0 1')
        move1 = Move(Square.E1, Square.G1, flag=0x02)
        move2 = Move(Square.E8, Square.G8, flag=0x02)
        position.makeMove(move1)
        position.makeMove(move2)

        position.unmakeMove(move2)
        position.unmakeMove(move1)
        expected = Position('rnbqk2r/ppppbppp/5n2/4p3/4P3/5N2/PPPPBPPP/RNBQK2R w KQkq - 0 1')

        self.assertEqual(position, expected)

    def test_QueensideCastle_makeMove(self):
        position = Position('r3kbnr/ppp1pppp/2nqb3/3p4/3P4/2NQB3/PPP1PPPP/R3KBNR w KQkq - 0 1')
        move1 = Move(Square.E1, Square.C1, flag=0x03)
        move2 = Move(Square.E8, Square.C8, flag=0x03)
        position.makeMove(move1)
        position.makeMove(move2)

        expected = Position('2kr1bnr/ppp1pppp/2nqb3/3p4/3P4/2NQB3/PPP1PPPP/2KR1BNR w - - 0 1')
        self.assertEqual(position, expected)

    def test_QueensideCastle_unmakeMove(self):
        position = Position('r3kbnr/ppp1pppp/2nqb3/3p4/3P4/2NQB3/PPP1PPPP/R3KBNR w KQkq - 0 1')
        move1 = Move(Square.E1, Square.C1, flag=0x03)
        move2 = Move(Square.E8, Square.C8, flag=0x03)
        position.makeMove(move1)
        position.makeMove(move2)
        position.unmakeMove(move2)
        position.unmakeMove(move1)

        expected = Position('r3kbnr/ppp1pppp/2nqb3/3p4/3P4/2NQB3/PPP1PPPP/R3KBNR w KQkq - 0 1')
        self.assertEqual(position, expected)

    
class FenTests(unittest.TestCase):
    def test_Fen_StartingPosition(self):
        position = Position()
        # TODO Finish this test
        return

if __name__ == '__main__':
	unittest.main()