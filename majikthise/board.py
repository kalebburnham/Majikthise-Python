from dataclasses import dataclass
from enum import IntEnum

import numpy as np

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
		self.parent: Position = None
		self.board: CBoard = None
		self.wAttacks: CBoard = None
		self.bAttacks: CBoard = None

		self.sideToMove: Color = Color.WHITE
		self.halfmove_clock = 0

		self.wkCastle = 0
		self.wqCastle = 0
		self.bkCastle = 0
		self.bqCastle = 0

		self.epTargetSquare: Square = Square.NONE

class Move:
	def __init__(self, origin: Square, destination: Square, flag = 0):
		self.origin = origin
		self.destination = destination
		self.flag = flag

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
