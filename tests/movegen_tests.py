import sys
sys.path.append('../majikthise')

import unittest

from bitboard import *
from board import *
from movegen import *
from rays import *

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

		position = Position()
		position.board.whitePawns = np.uint64(0x080100)
		moves = wGeneratePawnPushMoves(position)
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
		position = Position()
		position.board.whitePawns = np.uint64(0x0104000000)
		position.board.blackPawns = np.uint64(0x0400000000)
		moves = wGeneratePawnPushMoves(position)
		expectedMove = Move(origin=Square.A5, destination=Square.A6)
		self.assertCountEqual(moves, [expectedMove])

	def test_wPawnPush_OnSeventh(self):
		'''
		A white pawn on the seventh rank cannot push to the eigth and remain
		a pawn. That case will be handled by wGeneratePawnPromotions.

		Place one pawn on A7. No moves should be returned.
		'''
		position = Position()
		position.board.whitePawns = np.uint64(0x0001000000000000)
		moves = wGeneratePawnPushMoves(position)
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
		position = Position()
		position.board.blackPawns = np.uint64(0x0400800000)
		moves = bGeneratePawnPushMoves(position)
		move1 = Move(origin=Square.C5, destination=Square.C4)
		move2 = Move(origin=Square.H3, destination=Square.H2)

	def test_bPawnPush_Blockers(self):
		'''
		Place an unobstructed black pawn on C5 and an obstructed pawn on H3 and
		generate their single space pushes.
		'''
		position = Position()
		position.board.blackPawns = np.uint64(0x0400800000)
		position.board.whitePawns = SECOND_RANK
		moves = bGeneratePawnPushMoves(position)
		expectedMove = Move(origin=Square.C5, destination=Square.C4)
		self.assertCountEqual(moves, [expectedMove])

	def test_bPawnPush_OnSecond(self):
		'''
		A black pawn on the seventh rank cannot push to the second and remain a
		pawn. That case will be handled by bGeneratePawnPromotions.

		Place one pawn on A2. No moves should be returned.
		'''
		position = Position()
		position.board.blackPawns = np.uint64(0x100)
		moves = bGeneratePawnPushMoves(position)
		self.assertCountEqual(moves, [])

	def test_wDoublePawnPush_NoBlockers(self):
		'''
		Place all white pawns on the second rank with no blockers. Verify they
		all move to the fourth rank.
		'''
		position = Position()
		position.board.whitePawns = SECOND_RANK
		moves = wGenerateDoublePawnPushMoves(position)
		expectedMoves = [Move(Square.A2, Square.A4, 0x01),
						Move(Square.B2, Square.B4, 0x01),
						Move(Square.C2, Square.C4, 0x01),
						Move(Square.D2, Square.D4, 0x01),
						Move(Square.E2, Square.E4, 0x01),
						Move(Square.F2, Square.F4, 0x01),
						Move(Square.G2, Square.G4, 0x01),
						Move(Square.H2, Square.H4, 0x01)]
		self.assertCountEqual(moves, expectedMoves)

	def test_wGeneratePawnCaptures_e4d5(self):
		position = Position('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
		position.makeMove(Move(origin=Square.E2, destination=Square.E4))
		position.makeMove(Move(origin=Square.D7, destination=Square.D5))
		moves = wGeneratePawnCaptures(position)
		expectedMoves = [Move(Square.E4, Square.D5, 0x04, capturedPieceType=Piece.P)]

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
		position = Position()
		moves = generateKnightMoves(position)
		expected = [
			Move(origin=Square.B1, destination=Square.A3),
			Move(origin=Square.B1, destination=Square.C3),
			Move(origin=Square.G1, destination=Square.F3),
			Move(origin=Square.G1, destination=Square.H3)
		]

		self.assertCountEqual(moves, expected)

	def test_wGenerateKnightMoves_NoKnightsExist(self):
		position = Position()
		position.board.whiteKnights = np.uint64(0)
		moves = generateKnightMoves(position)
		expected = []
		self.assertEqual(moves, expected)

	def test_wGenerateKnightMoves_CombinationAttackBlocked(self):
		# simulate game after moves 1. Nc3 e5 2. Nf3 d5 3. Ng5 e4
		position = Position()
		position.board.whiteKnights = Square.C3.bitboard() | Square.G5.bitboard()
		position.board.blackPawns = np.uint64(0x00E7000810000000) # E4 and D5
		moves = generateKnightMoves(position)

		expected = [
			Move(origin=Square.C3, destination=Square.B1),
			Move(origin=Square.C3, destination=Square.A4),
			Move(origin=Square.C3, destination=Square.B5),
			Move(origin=Square.C3, destination=Square.D5, flag=0x04, capturedPieceType=Piece.P),
			Move(origin=Square.C3, destination=Square.E4, flag=0x04, capturedPieceType=Piece.P),
			Move(origin=Square.G5, destination=Square.H3),
			Move(origin=Square.G5, destination=Square.F3),
			Move(origin=Square.G5, destination=Square.E4, flag=0x04, capturedPieceType=Piece.P),
			Move(origin=Square.G5, destination=Square.E6),
			Move(origin=Square.G5, destination=Square.F7, flag=0x04, capturedPieceType=Piece.P),
			Move(origin=Square.G5, destination=Square.H7, flag=0x04, capturedPieceType=Piece.P)
		]

		self.assertCountEqual(moves, expected)

	def test_bGenerateKnightMoves_StartingPosition(self):
		'''
		At the very first move, test the moves the black knights can make.
		'''
		position = Position()
		position.sideToMove = Color.BLACK
		moves = generateKnightMoves(position)
		expected = [
			Move(origin=Square.B8, destination=Square.A6),
			Move(origin=Square.B8, destination=Square.C6),
			Move(origin=Square.G8, destination=Square.F6),
			Move(origin=Square.G8, destination=Square.H6)
		]

		self.assertCountEqual(moves, expected)

	def test_bGenerateKnightMoves_NoKnightsExist(self):
		position = Position()
		position.sideToMove = Color.BLACK
		position.board.blackKnights = np.uint64(0)
		moves = generateKnightMoves(position)
		expected = []
		self.assertEqual(moves, expected)

	def test_bGenerateKnightMoves_CombinationAttackBlocked(self):
		# simulate game after moves 1. e4 Nc6 2. d4 Nf6
		position = Position()
		position.sideToMove = Color.BLACK
		position.board.blackKnights = Square.C6.bitboard() | Square.F6.bitboard()
		position.board.whitePawns = np.uint64(0x0000000018000000) # D4 and E4
		moves = generateKnightMoves(position)

		expected = [
			Move(origin=Square.C6, destination=Square.B8),
			Move(origin=Square.C6, destination=Square.A5),
			Move(origin=Square.C6, destination=Square.B4),
			Move(origin=Square.C6, destination=Square.D4, flag=0x04, capturedPieceType=Piece.P),
			Move(origin=Square.C6, destination=Square.E5),
			Move(origin=Square.F6, destination=Square.G8),
			Move(origin=Square.F6, destination=Square.D5),
			Move(origin=Square.F6, destination=Square.E4, flag=0x04, capturedPieceType=Piece.P),
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

class RookMoveTests(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		initRays()

	def test_rookAttacks_A1(self):
		blockers = np.uint64(0)
		sq = Square.A1
		bbAttacks = rookAttacks(sq, blockers)
		expected = np.uint64(0x0101010101010100 | 0xfe)
		self.assertEqual(bbAttacks, expected)

	def test_rookAttacks_A8Starting(self):
		position = Position()
		blockers = (WHITE_BOARD(position.board) | BLACK_BOARD(position.board)) ^ Square.A8.bitboard()
		sq = Square.A8
		bbAttacks = rookAttacks(sq, blockers)
		expected = Square.A7.bitboard() | Square.B8.bitboard()
		self.assertEqual(bbAttacks, expected)

	def test_rookAttacks_Trapped(self):
		blockers = Square.D4.bitboard() | Square.E5.bitboard() | Square.E3.bitboard() | Square.F4.bitboard()
		sq = Square.E4
		bbAttacks = rookAttacks(sq, blockers)
		expected = np.uint64(blockers)
		self.assertEqual(bbAttacks, expected)

	def test_rookAttacks_SemiTrapped(self):
		blockers = Square.D4.bitboard() | Square.E5.bitboard() | Square.E3.bitboard()
		sq = Square.E4
		bbAttacks = rookAttacks(sq, blockers)
		expected = np.uint64(blockers) | Square.F4.bitboard() | Square.G4.bitboard() | Square.H4.bitboard()
		self.assertEqual(bbAttacks, expected)

	def test_wGenerateRookMoves_StartingPosition(self):
		position = Position()
		moves = generateRookMoves(position)
		expected = []
		self.assertEqual(moves, expected)

	def test_wGenerateRookMoves_a2a4(self):
		position = Position()
		position.board.whitePawns = (SECOND_RANK ^ Square.A2.bitboard()) | Square.A4.bitboard()
		moves = generateRookMoves(position)
		expected = [
			Move(Square.A1, Square.A2),
			Move(Square.A1, Square.A3)
		]
		self.assertEqual(moves, expected)

	def test_wGenerateRookMoves_ComplexPosition(self):
		
		position = Position(fen='r2qk1nr/p1p3pp/2n1b3/b2p4/R2ppB2/2PB1N2/1P1N1PPP/3QR1K1 w kq - 0 12')
		moves = generateRookMoves(position)
		expected = [
			Move(Square.A4, Square.A1),
			Move(Square.A4, Square.A2),
			Move(Square.A4, Square.A3),
			Move(Square.A4, Square.A5, 0x04, capturedPieceType=Piece.B),
			Move(Square.A4, Square.B4),
			Move(Square.A4, Square.C4),
			Move(Square.A4, Square.D4, 0x04, capturedPieceType=Piece.P),
			Move(Square.E1, Square.F1),
			Move(Square.E1, Square.E2),
			Move(Square.E1, Square.E3),
			Move(Square.E1, Square.E4, 0x04, capturedPieceType=Piece.P)
		]
		self.assertCountEqual(moves, expected)

	def test_wGenerateRookMoves_NoRooksOnBoard(self):
		position = Position()
		position.board.whiteRooks = np.uint64(0)
		moves = generateRookMoves(position)
		expected = []
		
		self.assertEqual(moves, expected)

	def test_bGenerateRookMoves_StartingPosition(self):
		position = Position()
		position.sideToMove = Color.BLACK
		moves = generateRookMoves(position)
		expected = []
		self.assertEqual(moves, expected)

	def test_bGenerateRookMoves_h4h5(self):
		pass

	def test_bGenerateRookMoves_ComplexPosition(self):
		pass

	def test_bGenerateRookMoves_NoRooksOnBoard(self):
		pass

class BishopMoveTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		initRays()

	def test_wGenerateBishopMoves_StartingBoard(self):
		position = Position()
		moves = generateBishopMoves(position)
		expected = []
		self.assertCountEqual(moves, expected)

	def test_bGenerateBishopMoves_StartingBoard(self):
		position = Position()
		position.sideToMove = Color.BLACK
		moves = generateBishopMoves(position)
		expected = []
		self.assertCountEqual(moves, expected)

	def test_wGenerateBishopMoves_AfterPawns(self):
		position = Position('rnbqkbnr/p1p2p1p/1p4p1/3pp3/3PP3/1P4P1/P1P2P1P/RNBQKBNR b KQkq - 0 1')
		moves = generateBishopMoves(position)
		expected = [
			Move(Square.C1, Square.B2),
			Move(Square.C1, Square.A3),
			Move(Square.C1, Square.D2),
			Move(Square.C1, Square.E3),
			Move(Square.C1, Square.F4),
			Move(Square.C1, Square.G5),
			Move(Square.C1, Square.H6),
			Move(Square.F1, Square.A6),
			Move(Square.F1, Square.B5),
			Move(Square.F1, Square.C4),
			Move(Square.F1, Square.D3),
			Move(Square.F1, Square.E2),
			Move(Square.F1, Square.G2),
			Move(Square.F1, Square.H3),
		]
		self.assertCountEqual(moves, expected)

	def test_bGenerateBishopMoves_AfterPawns(self):
		position = Position('rnbqkbnr/p1p2p1p/1p4p1/3pp3/3PP3/1P4P1/P1P2P1P/RNBQKBNR b KQkq - 0 1')
		position.sideToMove = Color.BLACK
		moves = generateBishopMoves(position)
		expected = [
			Move(Square.C8, Square.B7),
			Move(Square.C8, Square.A6),
			Move(Square.C8, Square.D7),
			Move(Square.C8, Square.E6),
			Move(Square.C8, Square.F5),
			Move(Square.C8, Square.G4),
			Move(Square.C8, Square.H3),
			Move(Square.F8, Square.A3),
			Move(Square.F8, Square.B4),
			Move(Square.F8, Square.C5),
			Move(Square.F8, Square.D6),
			Move(Square.F8, Square.E7),
			Move(Square.F8, Square.G7),
			Move(Square.F8, Square.H6),
		]
		self.assertCountEqual(moves, expected)

	def test_wQueen_StartingBoard(self):
		position = Position()
		moves = generateQueenMoves(position)
		expected = []
		self.assertCountEqual(moves, expected)

	def test_bQueen_StartingBoard(self):
		position = Position()
		position.sideToMove = Color.BLACK
		moves = generateQueenMoves(position)
		expected = []
		self.assertCountEqual(moves, expected)

	def test_wQueen_StartingBoardWithoutD2Pawn(self):
		position = Position()
		position.board.whitePawns = SECOND_RANK ^ Square.D2.bitboard()
		moves = generateQueenMoves(position)
		expected = [
			Move(Square.D1, Square.D2),
			Move(Square.D1, Square.D3),
			Move(Square.D1, Square.D4),
			Move(Square.D1, Square.D5),
			Move(Square.D1, Square.D6),
			Move(Square.D1, Square.D7, 0x04, capturedPieceType=Piece.P)
		]
		self.assertCountEqual(moves, expected)

	def test_bQueen_StartingBoardWithoutD7Pawn(self):
		position = Position()
		position.board.blackPawns = SEVENTH_RANK ^ Square.D7.bitboard()
		position.sideToMove = Color.BLACK
		moves = generateQueenMoves(position)
		expected = [
			Move(Square.D8, Square.D7),
			Move(Square.D8, Square.D6),
			Move(Square.D8, Square.D5),
			Move(Square.D8, Square.D4),
			Move(Square.D8, Square.D3),
			Move(Square.D8, Square.D2, 0x04, capturedPieceType=Piece.P)
		]
		self.assertCountEqual(moves, expected)

	def test_wAllMoves_StartingPosition(self):
		position = Position()
		moves = generateAllMoves(position)
		self.assertEqual(len(moves), 20)
		expected = [
			Move(Square.A2, Square.A3),
			Move(Square.B2, Square.B3),
			Move(Square.C2, Square.C3),
			Move(Square.D2, Square.D3),
			Move(Square.E2, Square.E3),
			Move(Square.F2, Square.F3),
			Move(Square.G2, Square.G3),
			Move(Square.H2, Square.H3),
			Move(Square.A2, Square.A4, 0x01),
			Move(Square.B2, Square.B4, 0x01),
			Move(Square.C2, Square.C4, 0x01),
			Move(Square.D2, Square.D4, 0x01),
			Move(Square.E2, Square.E4, 0x01),
			Move(Square.F2, Square.F4, 0x01),
			Move(Square.G2, Square.G4, 0x01),
			Move(Square.H2, Square.H4, 0x01),
			Move(Square.B1, Square.A3),
			Move(Square.B1, Square.C3),
			Move(Square.G1, Square.F3),
			Move(Square.G1, Square.H3)
		]
		self.assertCountEqual(moves, expected)

	def testbAllMoves_StartingPosition(self):
		pass

	# Todo: Test a bunch of random game positions.

class MakeMoveTests(unittest.TestCase):

	def test_makeMove_e2e4(self):
		position = Position()
		move = Move(Square.E2, Square.E4)
		position.makeMove(move)

		expected = Position()
		expected.board.whitePawns = (SECOND_RANK ^ Square.E2.bitboard()) | Square.E4.bitboard()
		expected.sideToMove = Color.BLACK

		self.assertEqual(position, expected)

	def test_makeMove_e4xd5(self):
		# TODO The starting position should set the en passant target square in the fen (d6).
		position = Position('rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1')
		position.makeMove(Move(Square.E4, Square.D5, flag=0x04, capturedPieceType=Piece.P))

		expected = Position('rnbqkbnr/ppp1pppp/8/3P4/8/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1')
		self.assertEqual(position, expected)

	def test_unmakeMove_e4xd5(self):
		position = Position('rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1')
		move = Move(Square.E4, Square.D5, flag=0x04, capturedPieceType=Piece.P)
		position.makeMove(move)
		position.unmakeMove(move)

		expected = Position('rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1')
		self.assertEqual(position, expected)


		

	

if __name__ == '__main__':
	unittest.main()