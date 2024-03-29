import sys
sys.path.append('../majikthise')

import unittest

from bitboard import *
from board import *
from movegen import *
from rays import *

from constants import *

class MovegenTests(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		initBitboards()

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

	@classmethod
	def setUpClass(cls):
		initBitboards()

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
		position.board.pieceBoards[WHITE][PAWN] = np.uint64(0x080100)
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
		position.board.pieceBoards[WHITE][PAWN] = 0x0104000000
		position.board.pieceBoards[BLACK][PAWN] = 0x0400000000
		position.board.updateColorBoards()
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
		position.board.pieceBoards[WHITE][PAWN] = Square.A7.bitboard()
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
		position.board.pieceBoards[BLACK][PAWN] = 0x0400800000
		moves = bGeneratePawnPushMoves(position)
		move1 = Move(origin=Square.C5, destination=Square.C4)
		move2 = Move(origin=Square.H3, destination=Square.H2)

	def test_bPawnPush_Blockers(self):
		'''
		Place an unobstructed black pawn on C5 and an obstructed pawn on H3 and
		generate their single space pushes.
		'''
		position = Position()
		position.board.pieceBoards[BLACK][PAWN] = 0x0400800000
		position.board.pieceBoards[WHITE][PAWN] = SECOND_RANK
		position.board.updateColorBoards()
		position.sideToMove = BLACK
		moves = bGeneratePawnPushMoves(position)
		print(moves)
		expectedMove = Move(origin=Square.C5, destination=Square.C4)
		self.assertCountEqual(moves, [expectedMove])

	def test_bPawnPush_OnSecond(self):
		'''
		A black pawn on the seventh rank cannot push to the second and remain a
		pawn. That case will be handled by bGeneratePawnPromotions.

		Place one pawn on A2. No moves should be returned.
		'''
		position = Position()
		position.board.pieceBoards[BLACK][PAWN] = 0x100
		moves = bGeneratePawnPushMoves(position)
		self.assertCountEqual(moves, [])

	def test_wDoublePawnPush_NoBlockers(self):
		'''
		Place all white pawns on the second rank with no blockers. Verify they
		all move to the fourth rank.
		'''
		position = Position()
		position.board.pieceBoards[WHITE][PAWN] = SECOND_RANK
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
		expectedMoves = [Move(Square.E4, Square.D5, 0x04, capturedPieceType=PAWN)]

		self.assertCountEqual(moves, expectedMoves)

	def test_wGeneratePawnCaptures_KnightOnC3(self):
		position = Position()
		moves = [Move(Square.B1, Square.C3), Move(Square.E7, Square.E6)]
		for move in moves:
			position.makeMove(move)
		generatedMoves = generateAllMoves(position)
		# TODO Incomplete Test
		return
class KnightMoveTests(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		initBitboards()

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
		expected = 0x00000000A0100010
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
		expected = 0x00000000A0100010
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
		position.board.pieceBoards[WHITE][KNIGHT] = 0
		moves = generateKnightMoves(position)
		expected = []
		self.assertEqual(moves, expected)

	def test_wGenerateKnightMoves_CombinationAttackBlocked(self):
		# simulate game after moves 1. Nc3 e5 2. Nf3 d5 3. Ng5 e4
		position = Position()
		position.board.pieceBoards[WHITE][KNIGHT] = Square.C3.bitboard() | Square.G5.bitboard()
		position.board.pieceBoards[BLACK][PAWN] = 0x00E7000810000000
		position.board.updateColorBoards()
		moves = generateKnightMoves(position)
		expected = [
			Move(origin=Square.C3, destination=Square.B1),
			Move(origin=Square.C3, destination=Square.A4),
			Move(origin=Square.C3, destination=Square.B5),
			Move(origin=Square.C3, destination=Square.D5, flag=0x04, capturedPieceType=PAWN),
			Move(origin=Square.C3, destination=Square.E4, flag=0x04, capturedPieceType=PAWN),
			Move(origin=Square.G5, destination=Square.H3),
			Move(origin=Square.G5, destination=Square.F3),
			Move(origin=Square.G5, destination=Square.E4, flag=0x04, capturedPieceType=PAWN),
			Move(origin=Square.G5, destination=Square.E6),
			Move(origin=Square.G5, destination=Square.F7, flag=0x04, capturedPieceType=PAWN),
			Move(origin=Square.G5, destination=Square.H7, flag=0x04, capturedPieceType=PAWN)
		]

		self.assertCountEqual(moves, expected)

	def test_bGenerateKnightMoves_StartingPosition(self):
		'''
		At the very first move, test the moves the black knights can make.
		'''
		position = Position()
		position.sideToMove = BLACK
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
		position.sideToMove = BLACK
		position.board.pieceBoards[BLACK][KNIGHT] = 0
		moves = generateKnightMoves(position)
		expected = []
		self.assertEqual(moves, expected)

	def test_bGenerateKnightMoves_CombinationAttackBlocked(self):
		# simulate game after moves 1. e4 Nc6 2. d4 Nf6
		position = Position()
		position.sideToMove = BLACK
		position.board.pieceBoards[BLACK][KNIGHT] = Square.C6.bitboard() | Square.F6.bitboard()
		position.board.pieceBoards[WHITE][PAWN] = 0x0000000018000000 # D4 and E4
		position.board.updateColorBoards()
		moves = generateKnightMoves(position)

		expected = [
			Move(origin=Square.C6, destination=Square.B8),
			Move(origin=Square.C6, destination=Square.A5),
			Move(origin=Square.C6, destination=Square.B4),
			Move(origin=Square.C6, destination=Square.D4, flag=0x04, capturedPieceType=PAWN),
			Move(origin=Square.C6, destination=Square.E5),
			Move(origin=Square.F6, destination=Square.G8),
			Move(origin=Square.F6, destination=Square.D5),
			Move(origin=Square.F6, destination=Square.E4, flag=0x04, capturedPieceType=PAWN),
			Move(origin=Square.F6, destination=Square.G4),
			Move(origin=Square.F6, destination=Square.H5)
		]

		self.assertCountEqual(moves, expected)

class KingMoveTests(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		initBitboards()

	def test_wGenerateKingMoves_StartingPosition(self):
		position = Position()
		moves = generateKingMoves(position)
		expected = []
		self.assertCountEqual(moves, expected)

	def test_wGenerateKingMoves_e4e5(self):
		position = Position()
		position.board.pieceBoards[WHITE][PAWN] = (SECOND_RANK ^ Square.E2.bitboard()) | Square.E4.bitboard() # 1. e4
		position.board.pieceBoards[BLACK][PAWN] = (SEVENTH_RANK ^ Square.E7.bitboard()) | Square.E5.bitboard() # 1. e4 e5
		position.board.updateColorBoards()
		moves = generateKingMoves(position)
		expected = [Move(Square.E1, Square.E2)]
		self.assertCountEqual(moves, expected)

	def test_bGenerateKingMoves_StartingPosition(self):
		position = Position()
		position.board.pieceBoards[WHITE][PAWN] = (SECOND_RANK ^ Square.E2.bitboard()) | Square.E4.bitboard() # 1. e4
		position.sideToMove = BLACK
		moves = generateKingMoves(position)
		expected = []
		self.assertCountEqual(moves, expected)

	def test_bGenerateKingMoves_e4e5(self):
		'''
		Test black's options after 1. e4 e5. Not a valid game, but all that matters is that the e7 pawn is moved.
		'''
		position = Position()
		position.board.pieceBoards[WHITE][PAWN] = (SECOND_RANK ^ Square.E2.bitboard()) | Square.E4.bitboard() # 1. e4
		position.board.pieceBoards[BLACK][PAWN] = (SEVENTH_RANK ^ Square.E7.bitboard()) | Square.E5.bitboard() # 1. e4 e5
		position.sideToMove = BLACK
		position.board.updateColorBoards()

		moves = generateKingMoves(position)
		expected = [Move(Square.E8, Square.E7)]

		self.assertCountEqual(moves, expected)

	def test_wGenerateKingMoves_KingsideCastle(self):
		position = Position()
		position.board.pieceBoards[WHITE][KNIGHT] = Square.B1.bitboard()
		position.board.pieceBoards[WHITE][BISHOP] = Square.C1.bitboard()
		position.board.updateColorBoards()
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
		initBitboards()

	def test_rookAttacks_A1(self):
		blockers = 0
		sq = Square.A1
		bbAttacks = rookAttacks(sq, blockers)
		expected = 0x0101010101010100 | 0xfe
		self.assertEqual(bbAttacks, expected)

	def test_rookAttacks_A8Starting(self):
		position = Position()
		blockers = (position.board.whiteBoard | position.board.blackBoard) ^ Square.A8.bitboard()
		sq = Square.A8
		bbAttacks = rookAttacks(sq, blockers)
		expected = Square.A7.bitboard() | Square.B8.bitboard()
		self.assertEqual(bbAttacks, expected)

	def test_rookAttacks_Trapped(self):
		blockers = Square.D4.bitboard() | Square.E5.bitboard() | Square.E3.bitboard() | Square.F4.bitboard()
		sq = Square.E4
		bbAttacks = rookAttacks(sq, blockers)
		expected = blockers
		self.assertEqual(bbAttacks, expected)

	def test_rookAttacks_SemiTrapped(self):
		blockers = Square.D4.bitboard() | Square.E5.bitboard() | Square.E3.bitboard()
		sq = Square.E4
		bbAttacks = rookAttacks(sq, blockers)
		expected = blockers | Square.F4.bitboard() | Square.G4.bitboard() | Square.H4.bitboard()
		self.assertEqual(bbAttacks, expected)

	def test_wGenerateRookMoves_StartingPosition(self):
		position = Position()
		moves = generateRookMoves(position)
		expected = []
		self.assertEqual(moves, expected)

	def test_wGenerateRookMoves_a2a4(self):
		position = Position()
		position.board.pieceBoards[WHITE][PAWN] = (SECOND_RANK ^ Square.A2.bitboard()) | Square.A4.bitboard()
		position.board.updateColorBoards()
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
			Move(Square.A4, Square.A5, 0x04, capturedPieceType=BISHOP),
			Move(Square.A4, Square.B4),
			Move(Square.A4, Square.C4),
			Move(Square.A4, Square.D4, 0x04, capturedPieceType=PAWN),
			Move(Square.E1, Square.F1),
			Move(Square.E1, Square.E2),
			Move(Square.E1, Square.E3),
			Move(Square.E1, Square.E4, 0x04, capturedPieceType=PAWN)
		]
		self.assertCountEqual(moves, expected)

	def test_wGenerateRookMoves_NoRooksOnBoard(self):
		position = Position()
		position.board.pieceBoards[WHITE][ROOK] = 0
		moves = generateRookMoves(position)
		expected = []
		
		self.assertEqual(moves, expected)

	def test_bGenerateRookMoves_StartingPosition(self):
		position = Position()
		position.sideToMove = BLACK
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
		initBitboards()

	def test_wGenerateBishopMoves_StartingBoard(self):
		position = Position()
		moves = generateBishopMoves(position)
		expected = []
		self.assertCountEqual(moves, expected)

	def test_bGenerateBishopMoves_StartingBoard(self):
		position = Position()
		position.sideToMove = BLACK
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
		position.sideToMove = BLACK
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
		position.sideToMove = BLACK
		moves = generateQueenMoves(position)
		expected = []
		self.assertCountEqual(moves, expected)

	def test_wQueen_StartingBoardWithoutD2Pawn(self):
		position = Position()
		position.board.pieceBoards[WHITE][PAWN] = SECOND_RANK ^ Square.D2.bitboard()
		position.board.updateColorBoards()
		moves = generateQueenMoves(position)
		expected = [
			Move(Square.D1, Square.D2),
			Move(Square.D1, Square.D3),
			Move(Square.D1, Square.D4),
			Move(Square.D1, Square.D5),
			Move(Square.D1, Square.D6),
			Move(Square.D1, Square.D7, 0x04, capturedPieceType=PAWN)
		]
		self.assertCountEqual(moves, expected)

	def test_bQueen_StartingBoardWithoutD7Pawn(self):
		position = Position()
		position.board.pieceBoards[BLACK][PAWN] = SEVENTH_RANK ^ Square.D7.bitboard()
		position.board.updateColorBoards()
		position.sideToMove = BLACK
		moves = generateQueenMoves(position)
		expected = [
			Move(Square.D8, Square.D7),
			Move(Square.D8, Square.D6),
			Move(Square.D8, Square.D5),
			Move(Square.D8, Square.D4),
			Move(Square.D8, Square.D3),
			Move(Square.D8, Square.D2, 0x04, capturedPieceType=PAWN)
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

	@classmethod
	def setUpClass(cls):
		initBitboards()

	def test_makeMove_e2e4(self):
		position = Position()
		move = Move(Square.E2, Square.E4)
		position.makeMove(move)

		expected = Position()
		expected.board.pieceBoards[WHITE][PAWN] = (SECOND_RANK ^ Square.E2.bitboard()) | Square.E4.bitboard()
		expected.board.updateColorBoards()
		expected.sideToMove = BLACK

		

		self.assertEqual(position, expected)

	def test_makeMove_e4xd5(self):
		# TODO The starting position should set the en passant target square in the fen (d6).
		position = Position('rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1')
		position.makeMove(Move(Square.E4, Square.D5, flag=0x04, capturedPieceType=PAWN))

		expected = Position('rnbqkbnr/ppp1pppp/8/3P4/8/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1')
		expected.sideToMove = BLACK

		self.assertEqual(position, expected)

	def test_unmakeMove_e4xd5(self):
		position = Position('rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1')
		move = Move(Square.E4, Square.D5, flag=0x04, capturedPieceType=PAWN)
		position.makeMove(move)
		position.unmakeMove(move)

		expected = Position('rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1')
		self.assertEqual(position, expected)

class SequenceTests(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		initBitboards()

	def test_Sequence1(self):
		position = Position()
		moves = [Move(Square.B1, Square.C3), Move(Square.E7, Square.E6)]
		for move in moves:
			position.makeMove(move)

		generatedMoves = generateAllMoves(position)
		#print(generatedMoves)
		

class PieceLocationTests(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		initBitboards()

	def test_PieceLocation_1e4(self):
		position = Position()
		position.makeMove(Move(Square.E2, Square.E4, flag=0x01))

'''
def repeatNorthOne():
		from random import randint
		for _ in range(3000000):
			northOne(np.uint64(randint(0, 64)))

def repeatNorthOne2():
	from random import randint
	for _ in range(3000000):
		northOne2(c_uint64(randint(0, 64)))

class IntBitShiftSpeedTest(unittest.TestCase):

	def test_NorthOne(self):
		import cProfile
		cProfile.run('repeatNorthOne()')

	def test_NorthOne2(self):
		import cProfile
		cProfile.run('repeatNorthOne2()')


def repeatBSF():
	from random import randint
	for _ in range(100000):
		BSF(np.uint64(randint(0, 2**63)))
	
def repeatBSF2():
	from random import randint
	for _ in range(100000):
		BSF2(c_uint64(randint(0, 2**63)).value)

class BSFTests(unittest.TestCase):
	def test_BSF(self):
		import cProfile
		cProfile.run('repeatBSF()')


	def test_BSF2(self):
		import cProfile
		cProfile.run('repeatBSF2()')
'''

if __name__ == '__main__':
	unittest.main()