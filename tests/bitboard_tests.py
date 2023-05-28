import sys
sys.path.append('../majikthise')

import unittest

import bitboard
from bitboard import *
from board import *
from printer import *
from constants import *

class BitboardTests(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		initBitboards()

	'''
	Assertion error was removed for performance.
	def test_bsf_0b00(self):
		self.assertRaises(AssertionError, BSF, np.uint64(0b00))
	'''

	def test_bsf_0b1000(self):
		b = 0b1000
		self.assertEqual(BSF(b), 3)

	def test_bsf_0b1110(self):
		b = 0b1110
		self.assertEqual(BSF(b), 1)

	def test_bsf_0xFFFFFF00(self):
		b = 0xFFFFFF00
		self.assertEqual(BSF(b), 8)

	def test_bsf_0x8000000000000000(self):
		b = 0x8000000000000000
		self.assertEqual(BSF(b), 63)

	def test_bsf_17179869219(self):
		b = 17179869219
		self.assertEqual(BSF(b), 0)

	"""
	def test_bsr_0b00(self):
		self.assertRaises(AssertionError, BSR, 0b00)
	"""

	def test_bsr_0b01(self):
		self.assertEqual(BSR(0b01), 0)

	def test_bsr_0b11(self):
		self.assertEqual(BSR(0b11), 1)

	def test_bsr_0x8000000000000000(self):
		b = 0b1000000000000000000000000000000000000000000000000000000000000000
		self.assertEqual(BSR(b), 63)

	def test_generateBoard(self):
		b = CBoard()
		self.assertEqual(b.pieceBoards[(Color.WHITE, Piece.P)], SECOND_RANK)

	def test_northFill(self):
		b = Square.E5.bitboard()
		b = northFill(b)
		exp = Square.E5.bitboard() | Square.E6.bitboard() | Square.E7.bitboard() | Square.E8.bitboard()
		self.assertEqual(b, exp)

	def test_fileFill_H5(self):
		self.assertEqual(fileFill(eastOne(Square.H5.bitboard())), 0)

class FenTests(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		initBitboards()

	def test_StartingPosition(self):
		position = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
		fen = Fen(position)
		self.assertEqual(fen.whitePawns(), SECOND_RANK)
		self.assertEqual(fen.blackPawns(), SEVENTH_RANK)
		self.assertEqual(fen.whiteKnights(), Square.B1.bitboard() | Square.G1.bitboard())
		self.assertEqual(fen.blackKnights(), Square.B8.bitboard() | Square.G8.bitboard())
		self.assertEqual(fen.whiteBishops(), Square.C1.bitboard() | Square.F1.bitboard())
		self.assertEqual(fen.blackBishops(), Square.C8.bitboard() | Square.F8.bitboard())
		self.assertEqual(fen.whiteRooks(), Square.A1.bitboard() | Square.H1.bitboard())
		self.assertEqual(fen.blackRooks(), Square.A8.bitboard() | Square.H8.bitboard())
		self.assertEqual(fen.whiteQueens(), Square.D1.bitboard())
		self.assertEqual(fen.blackQueens(), Square.D8.bitboard())
		self.assertEqual(fen.whiteKing(), Square.E1.bitboard())
		self.assertEqual(fen.blackKing(), Square.E8.bitboard())

class CBoardTests(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		initBitboards()
		
	def test_DoubledPawns_StartingPosition(self):
		position = Position()
		self.assertEqual(position.board.doubledPawnCount(Color.WHITE), 0)
		self.assertEqual(position.board.doubledPawnCount(Color.BLACK), 0)

	def test_DoubledPawns_e3e2(self):
		position = Position()
		position.board.pieceBoards[(Color.WHITE, Piece.P)] ^= Square.D2.bitboard()
		position.board.pieceBoards[(Color.WHITE, Piece.P)] |= Square.E3.bitboard()
		self.assertEqual(position.board.doubledPawnCount(Color.WHITE), 2)

	def test_DoubledPawns_Tripled(self):
		position = Position('8/p7/p7/p7/8/8/8/8 w KQkq - 0 1')
		self.assertEqual(position.board.doubledPawnCount(Color.BLACK), 3)

	def test_DoubledPawns_AllOnSameFile(self):
		position = Position('8/2P5/2P5/2P5/2P5/2P5/2P5/2P5 w KQkq - 0 1')
		self.assertEqual(position.board.doubledPawnCount(Color.WHITE), 7)

	def test_isolanis_white1(self):
		b = CBoard()
		b.pieceBoards[(Color.WHITE, Piece.P)] = Square.E5.bitboard()
		self.assertEqual(b.isolatedPawnCount(Color.WHITE), 1)
		self.assertEqual(b.isolanis(0), b.pieceBoards[(Color.WHITE, Piece.P)])

	def test_isolanis_black2(self):
		b = CBoard()
		b.pieceBoards[(Color.BLACK, Piece.P)] = Square.E5.bitboard() | Square.H5.bitboard()
		self.assertEqual(b.isolatedPawnCount(Color.BLACK), 2)
		self.assertEqual(b.isolanis(1), b.pieceBoards[(Color.BLACK, Piece.P)])

	def test_isolanis_startingPosition(self):
		b = CBoard()
		self.assertEqual(b.isolatedPawnCount(0), 0)
		self.assertEqual(b.isolatedPawnCount(Color.BLACK), 0)
		
	def test_isolanis_fourIsolanis(self):
		b = CBoard()
		b.pieceBoards[(Color.BLACK, Piece.P)] = Square.A7.bitboard() | Square.C7.bitboard() | \
						Square.E7.bitboard() | Square.H7.bitboard()
		self.assertEqual(b.isolatedPawnCount(1), 4)

	def test_blockedPawns_e4e5(self):
		b = CBoard()
		b.pieceBoards[(Color.WHITE, Piece.P)] = Square.E4.bitboard() | Square.E5.bitboard()
		b.updateColorBoards()
		self.assertEqual(b.blockedPawnCount(0), 1)

	def test_blockedPawns_StartingPosition(self):
		b = CBoard()
		self.assertEqual(b.blockedPawnCount(0), 0)
		self.assertEqual(b.blockedPawnCount(1), 0)

	def test_blockedPawns_a6a7(self):
		b = CBoard()
		b.pieceBoards[(Color.BLACK, Piece.P)] = Square.A6.bitboard() | Square.A7.bitboard()
		b.updateColorBoards()
		self.assertEqual(b.blockedPawnCount(1), 1)

	def test_blockedPawns_AFile(self):
		b = CBoard()
		b.pieceBoards[(Color.WHITE, Piece.P)] = A_FILE & ~Square.A8.bitboard()
		b.pieceBoards[(Color.BLACK, Piece.R)] = 0
		b.pieceBoards[(Color.BLACK, Piece.P)] = 0
		b.updateColorBoards()
		self.assertEqual(b.blockedPawnCount(0), 6)

if __name__ == '__main__':
	unittest.main()