from dataclasses import dataclass
from enum import IntEnum

import numpy as np
import re

from bitboard import *

class Color(IntEnum):
	WHITE = 0
	BLACK = 1
	COLOR_NB = 2

class Piece(IntEnum):
	P = 0
	N = 1
	B = 2
	R = 3
	Q = 4
	K = 5

class Square(IntEnum):
	A1 = 0 
	B1 = 1
	C1 = 2
	D1 = 3
	E1 = 4
	F1 = 5
	G1 = 6
	H1 = 7
	A2 = 8
	B2 = 9
	C2 = 10 
	D2 = 11 
	E2 = 12 
	F2 = 13 
	G2 = 14
	H2 = 15
	A3 = 16 
	B3 = 17 
	C3 = 18 
	D3 = 19 
	E3 = 20 
	F3 = 21 
	G3 = 22 
	H3 = 23
	A4 = 24 
	B4 = 25 
	C4 = 26 
	D4 = 27 
	E4 = 28 
	F4 = 29 
	G4 = 30 
	H4 = 31
	A5 = 32 
	B5 = 33 
	C5 = 34 
	D5 = 35 
	E5 = 36 
	F5 = 37 
	G5 = 38 
	H5 = 39
	A6 = 40 
	B6 = 41 
	C6 = 42 
	D6 = 43 
	E6 = 44 
	F6 = 45 
	G6 = 46 
	H6 = 47
	A7 = 48 
	B7 = 49 
	C7 = 50 
	D7 = 51 
	E7 = 52 
	F7 = 53 
	G7 = 54 
	H7 = 55
	A8 = 56 
	B8 = 57 
	C8 = 58 
	D8 = 59 
	E8 = 60 
	F8 = 61 
	G8 = 62 
	H8 = 63
	NONE = 64

	def bitboard(self):
		return np.uint64(0x01) << np.uint64(self.value)

	def isEmpty(self, board: 'CBoard'):
		# Returns true if no white or black pieces occupy the square.
		return not bool(self.bitboard() & (WHITE_BOARD(board) | BLACK_BOARD(board)))

  #SQUARE_NB = 64

class Dir(IntEnum):
	NORTH = 0
	SOUTH = 1 
	EAST = 2
	WEST = 3
	NORTH_EAST = 4
	NORTH_WEST = 5
	SOUTH_EAST = 6
	SOUTH_WEST = 7

class CBoard:
	def __init__(self):
		self.whitePawns: np.uint64() = np.uint64(0)
		self.whiteKnights: np.uint64() = np.uint64(0)
		self.whiteBishops: np.uint64() = np.uint64(0)
		self.whiteRooks: np.uint64() = np.uint64(0)
		self.whiteQueens: np.uint64() = np.uint64(0)
		self.whiteKing: np.uint64() = np.uint64(0)

		self.blackPawns: np.uint64() = np.uint64(0)
		self.blackKnights: np.uint64() = np.uint64(0)
		self.blackBishops: np.uint64() = np.uint64(0)
		self.blackRooks: np.uint64() = np.uint64(0)
		self.blackQueens: np.uint64() = np.uint64(0)
		self.blackKing: np.uint64() = np.uint64(0)

		self.setPawns()
		self.setKnights()
		self.setBishops()
		self.setRooks()
		self.setQueens()
		self.setKings()

	def setPawns(self, white=True, black=True):
		if white:
			self.whitePawns = SECOND_RANK
		if black:
			self.blackPawns = SEVENTH_RANK

	def setKnights(self, white=True, black=True):
		if white:
			self.whiteKnights = np.uint64(0x42)
		if black:
			self.blackKnights = np.uint64(0x42 << 56)

	def setBishops(self, white=True, black=True):
		if white:
			self.whiteBishops = np.uint64(0x24)
		if black:
			self.blackBishops = np.uint64(0x24 << 56)

	def setRooks(self, white=True, black=True):
		if white:
			self.whiteRooks = np.uint64(0x81)
		if black:
			self.blackRooks = np.uint64(0x81 << 56)

	def setQueens(self, white=True, black=True):
		if white:
			self.whiteQueens = np.uint64(0x08)
		if black:
			self.blackQueens = np.uint64(0x08 << 56)

	def setKings(self, white=True, black=True):
		if white:
			self.whiteKing = np.uint64(0x10)
		if black:
			self.blackKing = np.uint64(0x10 << 56)

class Position:
	def __init__(self):
		self.parent: 'Position' = None
		self.board: CBoard = CBoard()
		self.wAttacks: CBoard = None
		self.bAttacks: CBoard = None

		self.sideToMove: Color = Color.WHITE
		self.halfmove_clock = 0

		# If 1, then castling is allowed.
		self.wkCastle = 1
		self.wqCastle = 1
		self.bkCastle = 1
		self.bqCastle = 1

		self.epTargetSquare: Square = Square.NONE


	def applyMove(self, move: 'Move'):
		return

class Move:
	def __init__(self, origin: Square=Square.NONE, destination: Square=Square.NONE, flag=0):
			self.origin = origin
			self.destination = destination
			self.flag=flag

	def __eq__(self, other):
		return self.origin == other.origin and \
				self.destination == other.destination and \
				self.flag == other.flag

	def __hash__(self):
		return hash((self.origin, self.destination, self.flag))

	def __repr__(self):
		return "Origin: " + str(self.origin) + " Destination: " + str(self.destination) + " Flag: " + str(self.flag)


	def __str__(self):
		return "Origin: " + str(self.origin) + " Destination: " + str(self.destination) + " Flag: " + str(self.flag)

	@staticmethod
	def fromLongAlgebraic(command='', position=None):
		'''
		https://en.wikipedia.org/wiki/Algebraic_notation_(chess)#Long_algebraic_notation

		See the Stockfish implementation:
		https://github.com/official-stockfish/Stockfish/blob/master/src/uci.cpp Line 380
		It creates a move list first from a given position, then iterates through to see which move it matches

		'''
		return


	@staticmethod
	def getFlag(move, position: Position):
		# https://www.chessprogramming.org/Encoding_Moves
		# Double pawn push
		origin = _squareToInt(move[:2])
		destination = _squareToInt(move[2:])
		if Square.B1 <= origin <= Square.B8 \
			and Square.D1 <= destination <= Square.D8 \
			and position.board.whitePawns ^ np.uint64():
				return
		
	@staticmethod
	def _squareToInt(square):
		'''
		Convert a string square to an integer corresponding to the Square enum.
		For example, a1 = 0, a5=40, c2=10
		This function should be tested.
		'''
		square = square.lower()
		if not re.search(square, '[abcdefgh][12345678'):
			raise ValueError("Square not valid: {square}")
		return (square[1]-1)*8 + (ord(square[0])-97)