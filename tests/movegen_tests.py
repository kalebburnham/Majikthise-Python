import sys
sys.path.append('../majikthise')

import unittest

from bitboard import *
from board import *
from movegen import *

class MovegenTests(unittest.TestCase):

	def test_singularize_0b0000(self):
		b = np.uint64(0b0000)
		self.assertCountEqual(singularize(b), [])

	def test_singularize_0b0001(self):
		b = np.uint64(0b0010)
		self.assertCountEqual(singularize(b), [np.uint64(0b0010)])

	def test_singularize_0b0101(self):
		b = np.uint64(0b0101)
		self.assertCountEqual(singularize(b), [np.uint64(0b0100), np.uint64(0b0001)])

class PawnMoveTests(unittest.TestCase):

	def test_wPawnPush_noBlockers(self):
		'''
		Place unobstructed white pawns on A2 and D3 and generate their single
		space pushes.

		00000000
		00000000
		00000000
		00000000
		00000000
		00010000
		10000000
		00000000
		'''

		board = CBoard()
		board.whitePawns = np.uint64(0x080100)
		moves = wGeneratePawnPushMoves(board)
		move1 = Move(origin=Square.A2, destination=Square.A3)
		move2 = Move(origin=Square.D3, destination=Square.D4)
		self.assertCountEqual(moves, [move1, move2])

	def test_wPawnPush_Blockers(self):
		'''
		Place an obstructed white pawn on C4 and an unobstructed pawn on A5.
		Only one move should be generated.

		00000000
		00000000
		00000000
		P0p00000
		00P00000
		00000000
		00000000
		00000000
		'''
		board = CBoard()
		board.whitePawns = np.uint64(0x0104000000)
		board.blackPawns = np.uint64(0x0400000000)
		moves = wGeneratePawnPushMoves(board)
		expectedMove = Move(origin=Square.A5, destination=Square.A6)
		self.assertCountEqual(moves, [expectedMove])

	def test_wPawnPush_OnSeventh(self):
		'''
		A white pawn on the seventh rank cannot push to the eigth and remain
		a pawn. That case will be handled by wGeneratePawnPromotions.

		Place one pawn on A7. No moves should be returned.
		'''
		board = CBoard()
		board.whitePawns = np.uint64(0x0001000000000000)
		moves = wGeneratePawnPushMoves(board)
		self.assertCountEqual(moves, [])

	def test_bPawnPush_NoBlockers(self):
		'''
		Place unobstructed black pawns on C5 and H3 and generate their single
		space pushes.

		00000000
		00000000
		00000000
		00100000
		00000000
		00000001
		00000000
		00000000
		'''
		board = CBoard()
		board.blackPawns = np.uint64(0x0400800000)
		moves = bGeneratePawnPushMoves(board)
		move1 = Move(origin=Square.C5, destination=Square.C4)
		move2 = Move(origin=Square.H3, destination=Square.H2)

	def test_bPawnPush_Blockers(self):
		'''
		Place an unobstructed black pawn on C5 and an obstructed pawn on H3 and
		generate their single space pushes.
		'''
		board = CBoard()
		board.blackPawns = np.uint64(0x0400800000)
		board.whitePawns = SECOND_RANK
		moves = bGeneratePawnPushMoves(board)
		expectedMove = Move(origin=Square.C5, destination=Square.C4)
		self.assertCountEqual(moves, [expectedMove])

	def test_bPawnPush_OnSecond(self):
		'''
		A black pawn on the seventh rank cannot push to the second and remain a
		pawn. That case will be handled by bGeneratePawnPromotions.

		Place one pawn on A2. No moves should be returned.
		'''
		board = CBoard()
		board.blackPawns = np.uint64(0x100)
		moves = bGeneratePawnPushMoves(board)
		self.assertCountEqual(moves, [])

	def test_wDoublePawnPush_NoBlockers(self):
		'''
		Place all white pawns on the second rank with no blockers. Verify they
		all move to the fourth rank.
		'''
		board = CBoard()
		board.whitePawns = SECOND_RANK
		moves = wGenerateDoublePawnPushMoves(board)
		expectedMoves = [Move(Square.A2, Square.A4),
						Move(Square.B2, Square.B4),
						Move(Square.C2, Square.C4),
						Move(Square.D2, Square.D4),
						Move(Square.E2, Square.E4),
						Move(Square.F2, Square.F4),
						Move(Square.G2, Square.G4),
						Move(Square.H2, Square.H4)]
		self.assertCountEqual(moves, expectedMoves)

class KnightMoveTests(unittest.TestCase):

	def test_knightAttacks_CenterOfBoard(self):
		'''
		Square: E5
		
		Expected:
		00000000
		00010100
		00100010
		00000000
		00100010
		00010100
		00000000
		00000000
		'''
		sq = Square.G2
		expected = np.uint64(0x00000000A0100010)
		self.assertEqual(expected, knightAttacks(sq))

	def test_knightAttacks_CornerOfBoard(self):
		'''
		Square: G2

		Expected:
		00000000
		00000000
		00000000
		00000000
		00000101
		00001000
		000000N0
		00001000
		'''
		expected = np.uint64(0x00000000A0100010)
		self.assertEqual(expected, knightAttacks(Square.G2))


if __name__ == '__main__':
	unittest.main()