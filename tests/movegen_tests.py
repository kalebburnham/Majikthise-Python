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

	def test_wGenerateKnightMoves_StartingPosition(self):
		'''
		At the very first move, test the moves the white knights can make.
		'''
		board = CBoard()
		moves = generateKnightMoves(board, Color.WHITE)
		expected = [
			Move(origin=Square.B1, destination=Square.A3),
			Move(origin=Square.B1, destination=Square.C3),
			Move(origin=Square.G1, destination=Square.F3),
			Move(origin=Square.G1, destination=Square.H3)
		]

		self.assertCountEqual(moves, expected)

	def test_wGenerateKnightMoves_NoKnightsExist(self):
		board = CBoard()
		board.whiteKnights = np.uint64(0)
		moves = generateKnightMoves(board, Color.WHITE)
		expected = []
		self.assertEqual(moves, expected)

	def test_wGenerateKnightMoves_CombinationAttackBlocked(self):
		# simulate game after moves 1. Nc3 e5 2. Nf3 d5 3. Ng5 e4
		board = CBoard()
		board.whiteKnights = Square.C3.bitboard() | Square.G5.bitboard()
		board.blackPawns = np.uint64(0x00E7000810000000) # E4 and D5
		moves = generateKnightMoves(board, Color.WHITE)

		expected = [
			Move(origin=Square.C3, destination=Square.B1),
			Move(origin=Square.C3, destination=Square.A4),
			Move(origin=Square.C3, destination=Square.B5),
			Move(origin=Square.C3, destination=Square.D5, flag=0x04),
			Move(origin=Square.C3, destination=Square.E4, flag=0x04),
			Move(origin=Square.G5, destination=Square.H3),
			Move(origin=Square.G5, destination=Square.F3),
			Move(origin=Square.G5, destination=Square.E4, flag=0x04),
			Move(origin=Square.G5, destination=Square.E6),
			Move(origin=Square.G5, destination=Square.F7, flag=0x04),
			Move(origin=Square.G5, destination=Square.H7, flag=0x04)
		]

		self.assertCountEqual(moves, expected)

	def test_bGenerateKnightMoves_StartingPosition(self):
		'''
		At the very first move, test the moves the black knights can make.
		'''
		board = CBoard()
		moves = generateKnightMoves(board, Color.BLACK)
		expected = [
			Move(origin=Square.B8, destination=Square.A6),
			Move(origin=Square.B8, destination=Square.C6),
			Move(origin=Square.G8, destination=Square.F6),
			Move(origin=Square.G8, destination=Square.H6)
		]

		self.assertCountEqual(moves, expected)

	def test_bGenerateKnightMoves_NoKnightsExist(self):
		board = CBoard()
		board.blackKnights = np.uint64(0)
		moves = generateKnightMoves(board, Color.BLACK)
		expected = []
		self.assertEqual(moves, expected)

	def test_bGenerateKnightMoves_CombinationAttackBlocked(self):
		self.maxDiff = None
		# simulate game after moves 1. e4 Nc6 2. d4 Nf6
		board = CBoard()
		board.blackKnights = Square.C6.bitboard() | Square.F6.bitboard()
		board.whitePawns = np.uint64(0x0000000018000000) # D4 and E4
		moves = generateKnightMoves(board, Color.BLACK)

		expected = [
			Move(origin=Square.C6, destination=Square.B8),
			Move(origin=Square.C6, destination=Square.A5),
			Move(origin=Square.C6, destination=Square.B4),
			Move(origin=Square.C6, destination=Square.D4, flag=0x04),
			Move(origin=Square.C6, destination=Square.E5),
			Move(origin=Square.F6, destination=Square.G8),
			Move(origin=Square.F6, destination=Square.D5),
			Move(origin=Square.F6, destination=Square.E4, flag=0x04),
			Move(origin=Square.F6, destination=Square.G4),
			Move(origin=Square.F6, destination=Square.H5)
		]

		self.assertCountEqual(moves, expected)

class KingMoveTests(unittest.TestCase):
	def test_wGenerateKingMoves_StartingPosition(self):
		position = Position()
		moves = generateKingMoves(position)
		expected = []
		self.assertCountEqual(moves, expected)

	def test_wGenerateKingMoves_e4e5(self):
		position = Position()
		position.board.whitePawns = (SECOND_RANK ^ Square.E2.bitboard()) | Square.E4.bitboard() # 1. e4
		position.board.blackPawns = (SEVENTH_RANK ^ Square.E7.bitboard()) | Square.E5.bitboard() # 1. e4 e5

		moves = generateKingMoves(position)
		expected = [Move(Square.E1, Square.E2)]
		self.assertCountEqual(moves, expected)

	def test_bGenerateKingMoves_StartingPosition(self):
		position = Position()
		position.board.whitePawns = (SECOND_RANK ^ Square.E2.bitboard()) | Square.E4.bitboard() # 1. e4
		position.sideToMove = Color.BLACK
		moves = generateKingMoves(position)
		expected = []
		self.assertCountEqual(moves, expected)

	def test_bGenerateKingMoves_e4e5(self):
		'''
		Test black's options after 1. e4 e5. Not a valid game, but all that matters is that the e7 pawn is moved.
		'''
		position = Position()
		position.board.whitePawns = (SECOND_RANK ^ Square.E2.bitboard()) | Square.E4.bitboard() # 1. e4
		position.board.blackPawns = (SEVENTH_RANK ^ Square.E7.bitboard()) | Square.E5.bitboard() # 1. e4 e5
		position.sideToMove = Color.BLACK

		moves = generateKingMoves(position)
		expected = [Move(Square.E8, Square.E7)]

		self.assertCountEqual(moves, expected)

	def test_wGenerateKingMoves_KingsideCastle(self):
		position = Position()
		position.board.whiteKnights = Square.B1.bitboard()
		position.board.whiteBishops = Square.C1.bitboard()

		moves = generateKingMoves(position)
		expected = [
			Move(Square.E1, Square.F1),
			Move(Square.E1, Square.G1, 0x02)
		]

		self.assertCountEqual(moves, expected)

	def test_wGenerateKingMoves_QueensideCastle(self):
		pass

	def test_bGenerateKingMoves_KingsideCastle(self):
		pass

	def test_bGenerateKingMoves_QueensideCastle(self):
		pass


if __name__ == '__main__':
	unittest.main()