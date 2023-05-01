from dataclasses import dataclass
from enum import IntEnum

import numpy as np
import re

from bitboard import *

class Color(IntEnum):
	WHITE = 0
	BLACK = 1
	COLOR_NB = 2

	def __invert__(self):
		if self.value == 0:
			return Color.BLACK
		elif self.value == 1:
			return Color.WHITE
		else:
			raise Exception("Error with the inversion of the Color enum.")

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
		squareIdx = 56
		idx = 0
		while squareIdx >= 0:
			char = self.fen[idx]
			if char == '/' or char == ' ':
				idx += 1
				squareIdx -= 16
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
		return self.findPiece('P')

	def blackPawns(self) -> np.uint64():
		return self.findPiece('p')

	def whiteKnights(self) -> np.uint64():
		return self.findPiece('N')

	def blackKnights(self) -> np.uint64():
		return self.findPiece('n')

	def whiteBishops(self) -> np.uint64():
		return self.findPiece('B')

	def blackBishops(self) -> np.uint64():
		return self.findPiece('b')

	def whiteRooks(self) -> np.uint64():
		return self.findPiece('R')

	def blackRooks(self) -> np.uint64():
		return self.findPiece('r')

	def whiteQueens(self) -> np.uint64():
		return self.findPiece('Q')

	def blackQueens(self) -> np.uint64():
		return self.findPiece('q')

	def whiteKing(self) -> np.uint64():
		return self.findPiece('K')

	def blackKing(self) -> np.uint64():
		return self.findPiece('k')

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

	def __eq__(self, other: 'CBoard'):
		return (self.whitePawns == other.whitePawns
				and self.whiteBishops == other.whiteBishops
				and self.whiteKnights == other.whiteKnights
				and self.whiteRooks == other.whiteRooks
				and self.whiteQueens == other.whiteQueens
				and self.whiteKing == other.whiteKing
				and self.blackPawns == other.blackPawns
				and self.blackBishops == other.blackBishops
				and self.blackKnights == other.blackKnights
				and self.blackRooks == other.blackRooks
				and self.blackQueens == other.blackQueens
				and self.blackKing == other.blackKing)

	def doubledPawnCount(self, sideToMove: Color) -> int:
		pawnBoard = self.whitePawns if sideToMove == Color.WHITE else self.blackPawns
		file = A_FILE
		count = 0
		for _ in range(7):
			pawns_on_this_file = POPCOUNT(file & pawnBoard)
			if pawns_on_this_file > 1:
				count += pawns_on_this_file
			file <<= np.uint64(1)

		return count

	def isolanis(self, sideToMove: Color) -> np.uint64():
		#https://www.chessprogramming.org/Isolated_Pawns_(Bitboards)
		pawnBoard = self.whitePawns if sideToMove == Color.WHITE else self.blackPawns
		fill = pawnBoard & ~fileFill(eastOne(pawnBoard))
		fill &= pawnBoard & ~fileFill(westOne(pawnBoard))
		return fill

	def isolatedPawnCount(self, sideToMove: Color) -> int:
		return POPCOUNT(self.isolanis(sideToMove))
		
	def blockedPawnCount(self, sideToMove: Color) -> int:
		blockers = WHITE_BOARD(self) | BLACK_BOARD(self)

		if sideToMove == Color.WHITE:
			return POPCOUNT(northOne(self.whitePawns) & blockers)
		else:
			return POPCOUNT(southOne(self.blackPawns) & blockers)

	def makeMove(self, move: 'Move'):
		if move.flag == '0x04':
			self.removePiece(move.destination.bitboard())
		# TODO Handle en passant and promotions and double pawn pushes


		color, piece = self.removePiece(move.origin.bitboard())
		self.putPiece(piece, color, move.destination)
		

	def unmakeMove(self, move: 'Move'):
		#reversedMove = Move(move.destination, move.origin, move.flag)
		#self.makeMove(reversedMove)
		color, piece = self.removePiece(move.destination.bitboard())
		self.putPiece(piece, color, move.origin)

		if move.flag == '0x04':
			# Puts the captured piece back.
			self.putPiece(move.capturedPieceType, ~color, move.origin)
		
		self.putPiece(piece, color, move.origin)

	def removePiece(self, bbSquare):
		if bbSquare & self.whitePawns:
			self.whitePawns = self.whitePawns ^ bbSquare
			return Color.WHITE, Piece.P
		elif bbSquare & self.whiteBishops:
			self.whiteBishops = self.whiteBishops ^ bbSquare
			return Color.WHITE, Piece.B
		elif bbSquare & self.whiteKnights:
			self.whiteKnights = self.whiteKnights ^ bbSquare
			return Color.WHITE, Piece.N
		elif bbSquare & self.whiteRooks:
			self.whiteRooks = self.whiteRooks ^ bbSquare
			return Color.WHITE, Piece.R
		elif bbSquare & self.whiteQueens:
			self.whiteQueens = self.whiteQueens ^ bbSquare
			return Color.WHITE, Piece.Q
		elif bbSquare & self.whiteKing:
			self.whiteKing = self.whiteKing ^ bbSquare
			return Color.WHITE, Piece.K
		elif bbSquare & self.blackPawns:
			self.blackPawns = self.blackPawns ^ bbSquare
			return Color.BLACK, Piece.P
		elif bbSquare & self.blackBishops:
			self.blackBishops = self.blackBishops ^ bbSquare
			return Color.BLACK, Piece.B
		elif bbSquare & self.blackKnights:
			self.blackKnights = self.blackKnights ^ bbSquare
			return Color.BLACK, Piece.N
		elif bbSquare & self.blackRooks:
			self.blackRooks = self.blackRooks ^ bbSquare
			return Color.BLACK, Piece.R
		elif bbSquare & self.blackQueens:
			self.blackQueens = self.blackQueens ^ bbSquare
			return Color.BLACK, Piece.Q
		elif bbSquare & self.blackKing:
			self.blackKing = self.blackKing ^ bbSquare
			return Color.BLACK, Piece.K

		raise Exception("Could not remove piece. square:" + str(bin(self.whitePawns)))

	def putPiece(self, piece: Piece, color: Color, square: Square):
		if piece == Piece.P and color == Color.WHITE:
			self.whitePawns = self.whitePawns | square.bitboard()
		elif piece == Piece.N and color == Color.WHITE:
			self.whiteKnights = self.whiteKnights | square.bitboard()
		elif piece == Piece.B and color == Color.WHITE:
			self.whiteBishops = self.whiteBishops | square.bitboard()
		elif piece == Piece.R and color == Color.WHITE:
			self.whiteRooks = self.whiteRooks | square.bitboard()
		elif piece == Piece.Q and color == Color.WHITE:
			self.whiteQueens = self.whiteQueens | square.bitboard()
		elif piece == Piece.K and color == Color.WHITE:
			self.whiteKing = self.whiteKing | square.bitboard()
		elif piece == Piece.P and color == Color.BLACK:
			self.blackPawns = self.blackPawns | square.bitboard()
		elif piece == Piece.N and color == Color.BLACK:
			self.blackKnights = self.blackKnights | square.bitboard()
		elif piece == Piece.B and color == Color.BLACK:
			self.blackBishops = self.blackBishops | square.bitboard()
		elif piece == Piece.R and color == Color.BLACK:
			self.blackRooks = self.blackRooks | square.bitboard()
		elif piece == Piece.Q and color == Color.BLACK:
			self.blackQueens = self.blackQueens | square.bitboard()
		elif piece == Piece.K and color == Color.BLACK:
			self.blackKing = self.blackKing | square.bitboard()

	def pieceTypeAtSquare(self, square: Square):
		piece: Piece = None

		if (self.whitePawns | self.blackPawns) & square.bitboard():
			piece = Piece.P
		elif (self.whiteKnights | self.blackKnights) & square.bitboard():
			piece = Piece.N
		elif (self.whiteBishops | self.blackBishops) & square.bitboard():
			piece = Piece.B
		elif (self.whiteRooks | self.blackRooks) & square.bitboard():
			piece = Piece.R
		elif (self.whiteQueens | self.blackQueens) & square.bitboard():
			piece = Piece.Q

		return piece

class Position:
	# TODO Write Equality Function
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

	def __eq__(self, other):
		return (self.board == other.board
				and self.sideToMove == other.sideToMove
				and self.halfmove_clock == other.halfmove_clock
				and self.wkCastle == other.wkCastle
				and self.wqCastle == other.wqCastle
				and self.bkCastle == other.bkCastle
				and self.bqCastle == other.bqCastle)

	def makeMove(self, move: 'Move'):
		# What all needs to be updated?
		# The board - need to translate squares to pieces on them.
		# The turn. Should swap after updates are complete.
		# Halfmove clock?
		self.board.makeMove(move)
		self.sideToMove = Color.WHITE if self.sideToMove == Color.BLACK else Color.BLACK
		return

	def unmakeMove(self, move: 'Move'):
		# TODO Captures, en passants, promotions, halfmove clock
		self.board.unmakeMove(move)
		self.sideToMove = Color.WHITE if self.sideToMove == Color.BLACK else Color.BLACK
		return

	def score(self):
		# Use NegaMax
		# Todo: Add mobility count
		# https://www.chessprogramming.org/Evaluation
		_score = 9 * (POPCOUNT(self.board.whiteQueens) - POPCOUNT(self.board.blackQueens)) \
			+ 5 * (POPCOUNT(self.board.whiteRooks) - POPCOUNT(self.board.blackRooks)) \
			+ 3 * (POPCOUNT(self.board.whiteKnights) - POPCOUNT(self.board.blackKnights)) \
			+ 3 * (POPCOUNT(self.board.whiteBishops) - POPCOUNT(self.board.blackBishops)) \
			+ (POPCOUNT(self.board.whitePawns) - POPCOUNT(self.board.blackPawns))

		_score -= 0.5 * (self.board.doubledPawnCount(Color.WHITE) - self.board.doubledPawnCount(Color.BLACK))
		_score -= 0.5 * (self.board.isolatedPawnCount(Color.WHITE) - self.board.isolatedPawnCount(Color.BLACK))
		_score -= 0.5 * (self.board.blockedPawnCount(Color.WHITE) - self.board.blockedPawnCount(Color.BLACK))

		return _score if self.sideToMove == Color.WHITE else -1 * _score

class Move:
	def __init__(self, 
				origin: Square=Square.NONE, 
				destination: Square=Square.NONE, 
				flag=0, 
				capturedPieceType=None):
			self.origin = origin
			self.destination = destination
			self.flag=flag
			self.capturedPieceType = capturedPieceType
			self.enpassantOrigin = origin if flag == 0x05 else Square.NONE

			if flag == 0x04 and self.capturedPieceType == None:
				raise Exception("A capture move was generated with no defined capturedPieceType.")

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


		
