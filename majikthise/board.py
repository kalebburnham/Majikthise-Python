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

class Fen:
	def __init__(self, fen: str):
		if fen is None:
			self.fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
		else:
			self.fen = fen
		#self.occupied = _occupied()

	def findPiece(self, pieceType):
		bb = np.uint64(0)
		squareIdx = 0
		idx = 0
		while squareIdx < 64:
			char = self.fen[idx]
			if char == '/':
				idx += 1
				continue
			elif char == pieceType:
				bb |= Square(squareIdx).bitboard()
				idx += 1
				squareIdx += 1
			elif char.isnumeric():
				idx += 1
				squareIdx += np.uint64(int(char))
			else:
				idx += 1
				squareIdx += 1

		return bb

	def whitePawns(self) -> np.uint64():
		return self.findPiece('p')

	def blackPawns(self) -> np.uint64():
		return self.findPiece('P')

	def whiteKnights(self) -> np.uint64():
		return self.findPiece('n')

	def blackKnights(self) -> np.uint64():
		return self.findPiece('N')

	def whiteBishops(self) -> np.uint64():
		return self.findPiece('b')

	def blackBishops(self) -> np.uint64():
		return self.findPiece('B')

	def whiteRooks(self) -> np.uint64():
		return self.findPiece('r')

	def blackRooks(self) -> np.uint64():
		return self.findPiece('R')

	def whiteQueens(self) -> np.uint64():
		return self.findPiece('q')

	def blackQueens(self) -> np.uint64():
		return self.findPiece('Q')

	def whiteKing(self) -> np.uint64():
		return self.findPiece('k')

	def blackKing(self) -> np.uint64():
		return self.findPiece('K')

class CBoard:
	def __init__(self, fen: str = None):
		self.fen = Fen(fen)

		self.whitePawns = self.fen.whitePawns()
		self.whiteBishops = self.fen.whiteBishops()
		self.whiteKnights = self.fen.whiteKnights()
		self.whiteRooks = self.fen.whiteRooks()
		self.whiteQueens = self.fen.whiteQueens()
		self.whiteKing = self.fen.whiteKing()

		self.blackPawns = self.fen.blackPawns()
		self.blackBishops = self.fen.blackBishops()
		self.blackKnights = self.fen.blackKnights()
		self.blackRooks = self.fen.blackRooks()
		self.blackQueens = self.fen.blackQueens()
		self.blackKing = self.fen.blackKing()

class Position:
	def __init__(self, fen=None):
		self.parent: 'Position' = None
		self.board: CBoard = CBoard(fen)
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


		
