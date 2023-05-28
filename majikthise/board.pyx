# Cython directive
# cython: profile=True

from dataclasses import dataclass
from enum import IntEnum
from copy import deepcopy

import numpy as np
import re

from bitboard cimport *
from constants import *

from cython.operator import dereference



class Color(IntEnum):
	WHITE = 0
	BLACK = 1
	COLOR_NB = 2

	def __invert__(self):
		if self.value == 0:
			return BLACK
		elif self.value == 1:
			return WHITE
		else:
			raise Exception("Error with the inversion of the Color enum.")

cdef enum Piece:
	P=1
	N=2
	B=3
	R=4
	Q=5
	K=6
"""
class Piece(IntEnum):
	P = 0
	N = 1
	B = 2
	R = 3
	Q = 4
	K = 5
"""

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
		# This isn't being set.
		return SQUARE_TO_BITBOARD[self.value]	

	#cpdef size_t bitboardCython(self):
	#	return 0x01 << self.value	

	def isEmpty(self, board: 'CBoard'):
		# Returns true if no white or black pieces occupy the square.
		return not bool(self.bitboard() & board.occupied)

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
		cdef size_t bb = 0
		squareIdx = 56
		idx = 0
		while squareIdx >= 0:
			char = self.fen[idx]
			if char == '/' or char == ' ':
				idx += 1
				squareIdx -= 16
				continue
			elif char == pieceType:
				bb |= <size_t> 1 << squareIdx
				idx += 1
				squareIdx += 1
			elif char.isnumeric():
				idx += 1
				squareIdx += int(char)
				#squareIdx += np.uint64(int(char))
			else:
				idx += 1
				squareIdx += 1

		return bb

	def whitePawns(self):
		return self.findPiece('P')

	def blackPawns(self):
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

	def blackKing(self):
		return self.findPiece('k')

	def whiteKingCastle(self):
		return 1 if re.search('[wb]\s.*K', self.fen) else 0

	def whiteQueenCastle(self):
		return 1 if re.search('[wb]\s.*Q', self.fen) else 0

	def blackKingCastle(self):
		return 1 if re.search('[wb]\s.*k', self.fen) else 0

	def blackQueenCastle(self):
		return 1 if re.search('[wb]\s.*q', self.fen) else 0

cdef class CBoard:
	def __init__(self, fen_str: str = None):
		self.fen = Fen(fen_str)

		# Access the piece boards through self.pieceBoards[color][piece]
		self.pieceBoards = [[self.fen.whitePawns(), 
							self.fen.whiteKnights(), 
							self.fen.whiteBishops(),
							self.fen.whiteRooks(),
							self.fen.whiteQueens(),
							self.fen.whiteKing()],
							[self.fen.blackPawns(), 
							self.fen.blackKnights(), 
							self.fen.blackBishops(),
							self.fen.blackRooks(),
							self.fen.blackQueens(),
							self.fen.blackKing()]]

		self.pieceLocations = [None] * 64
	
		self.whiteBoard = 0
		self.blackBoard = 0
		#self.whiteBoard = None
		#self.blackBoard = None
		self.occupied = 0
		self.updateColorBoards()
		self.onInitUpdatePieceLocations()


	def __eq__(self, other: 'CBoard'):
		return (self.pieceBoards == other.pieceBoards
				and self.whiteBoard == other.whiteBoard
				and self.blackBoard == other.blackBoard)

	def doubledPawnCount(self, sideToMove: Color) -> int:
		pawnBoard = self.pieceBoards[WHITE][PAWN] if sideToMove == WHITE else self.pieceBoards[BLACK][PAWN]
		_file = A_FILE
		
		count = 0
		for _ in range(7):
			pawns_on_this_file = POPCOUNT(_file & pawnBoard)
			if pawns_on_this_file > 1:
				count += pawns_on_this_file
			_file <<= 1

		return count

	def isolanis(self, sideToMove: Color) -> np.uint64():
		#https://www.chessprogramming.org/Isolated_Pawns_(Bitboards)
		pawnBoard = self.pieceBoards[WHITE][PAWN] if sideToMove == WHITE else self.pieceBoards[BLACK][PAWN]
		fill = pawnBoard & ~fileFill(eastOne(pawnBoard))
		fill &= pawnBoard & ~fileFill(westOne(pawnBoard))
		return fill

	def isolatedPawnCount(self, sideToMove: Color) -> int:
		return POPCOUNT(self.isolanis(sideToMove))
		
	def blockedPawnCount(self, sideToMove: Color) -> int:
		if sideToMove == WHITE:
			return POPCOUNT(northOne(self.pieceBoards[WHITE][PAWN]) & self.occupied)
		else:
			return POPCOUNT(southOne(self.pieceBoards[BLACK][PAWN]) & self.occupied)

	def makeMove(self, move: 'Move', color):
		if move.flag == 0x04:
			# Remove the captured piece.
			# Add color and piece type to this call. removePiece is one of the slowest functions due to branching.
			self.removePiece(INVERT(color), move.capturedPieceType, move.destination.bitboard())
		# TODO Handle en passant and promotions and double pawn pushes

		movingPiece = self.pieceTypeAtSquare(move.origin)
		self.removePiece(color, movingPiece, move.origin.bitboard())
		self.putPiece(movingPiece, color, move.destination)

		if move.flag == 0x02:
			# King Castle. Move the rook. Reset castling flags
			if color == WHITE:
				self.removePiece(color, ROOK, Square.H1.bitboard())
				self.putPiece(ROOK, WHITE, Square.F1)
			else:
				self.removePiece(color, ROOK, Square.H8.bitboard())
				self.putPiece(ROOK, BLACK, Square.F8)

		if move.flag == 0x03:
			# Queen Castle. Move the rook.
			if color == WHITE:
				self.removePiece(color, ROOK, Square.A1.bitboard())
				self.putPiece(ROOK, WHITE, Square.D1)
			else:
				self.removePiece(color, ROOK, Square.A8.bitboard())
				self.putPiece(ROOK, BLACK, Square.D8)

		self.updateColorBoards()
		

	def unmakeMove(self, move: 'Move', color):
		movingPiece = self.pieceTypeAtSquare(move.destination)
		self.removePiece(color, movingPiece, move.destination.bitboard())
		self.putPiece(movingPiece, color, move.origin)

		if move.flag == 0x02:
			# King Castle. Put the rook back.
			if color == WHITE:
				self.removePiece(color, ROOK, Square.F1.bitboard())
				self.putPiece(ROOK, WHITE, Square.H1)
			else:
				self.removePiece(color, ROOK, Square.F8.bitboard())
				self.putPiece(ROOK, BLACK, Square.H8)
		
		if move.flag == 0x03:
			# Queen Castle. Put the rook back.
			if color == WHITE:
				self.removePiece(color, ROOK, Square.D1.bitboard())
				self.putPiece(ROOK, WHITE, Square.A1)
			else:
				self.removePiece(color, ROOK, Square.D8.bitboard())
				self.putPiece(ROOK, BLACK, Square.A8)

		if move.flag == 0x04:
			# Puts the captured piece back.
			self.putPiece(move.capturedPieceType, INVERT(color), move.destination)

		self.updateColorBoards()
		
	cpdef removePiece(self, color, piece, bbSquare):
		self.pieceBoards[color][piece] = self.pieceBoards[color][piece] ^ bbSquare
		self.pieceLocations[BSF(bbSquare)] = None
		

	cpdef putPiece(self, piece, color, square):
		self.pieceBoards[color][piece] |= square.bitboard()
		self.pieceLocations[square.value] = piece

	def pieceTypeAtSquare(self, square: Square):
		# This might be acting up. Is pieceLocations correct?
		return self.pieceLocations[square.value]

	cpdef updateColorBoards(self):
		self.whiteBoard = self.pieceBoards[WHITE][PAWN] | self.pieceBoards[WHITE][KNIGHT] | self.pieceBoards[WHITE][BISHOP] | self.pieceBoards[WHITE][ROOK] | self.pieceBoards[WHITE][QUEEN] | self.pieceBoards[WHITE][KING]
		self.blackBoard = self.pieceBoards[BLACK][PAWN] | self.pieceBoards[BLACK][KNIGHT] | self.pieceBoards[BLACK][BISHOP] | self.pieceBoards[BLACK][ROOK] | self.pieceBoards[BLACK][QUEEN] | self.pieceBoards[BLACK][KING]
		self.occupied = self.whiteBoard | self.blackBoard

	def onInitUpdatePieceLocations(self):
		for color in range(2):
			for piece in range(6):
				pieceBitboard = deepcopy(self.pieceBoards[color][piece])
				while pieceBitboard:
					squareIdx = BSF(pieceBitboard)
					self.pieceLocations[squareIdx] = piece
					pieceBitboard ^= 0x01 << squareIdx


class Position:
	def __init__(self, fen=None, debug=False):
		self.parent: 'Position' = None
		self.board: CBoard = CBoard(fen)
		self.wAttacks: CBoard = None
		self.bAttacks: CBoard = None

		self.sideToMove = WHITE
		self.halfmove_clock = 0

		# If 1, then castling is allowed.
		self.wkCastle = self.board.fen.whiteKingCastle()
		self.wqCastle = self.board.fen.whiteQueenCastle()
		self.bkCastle = self.board.fen.blackKingCastle()
		self.bqCastle = self.board.fen.blackQueenCastle()

		self.epTargetSquare: Square = Square.NONE

		self.moveSequence = []

		self.debug = debug

	def __eq__(self, other):
		return (self.board == other.board
				and self.sideToMove == other.sideToMove
				and self.halfmove_clock == other.halfmove_clock
				and self.wkCastle == other.wkCastle
				and self.wqCastle == other.wqCastle
				and self.bkCastle == other.bkCastle
				and self.bqCastle == other.bqCastle)

	def __repr__(self):
		return f'''Board: \n 
				{self.board} \n 
				Side to move: {self.sideToMove} \n 
				Halfmove clock: {self.halfmove_clock} \n 
				White kingside castle: {self.wkCastle} \n
				White queenside castle: {self.wqCastle} \n
				Black kingside castle: {self.bkCastle} \n
				Black queenside castle: {self.bqCastle}'''

	def __str__(self):
		return f'''Board: \n 
				{self.board} \n 
				Side to move: {self.sideToMove} \n 
				Halfmove clock: {self.halfmove_clock} \n 
				White kingside castle: {self.wkCastle} \n
				White queenside castle: {self.wqCastle} \n
				Black kingside castle: {self.bkCastle} \n
				Black queenside castle: {self.bqCastle}'''


	def makeMove(self, move: 'Move'):
		# What all needs to be updated?
		# The board - need to translate squares to pieces on them.
		# The turn. Should swap after updates are complete.
		# Halfmove clock?
		self.moveSequence.append(move)
		if self.debug:
			file = open("Position_log.txt", "a")
			file.write(f'{self.sideToMove} MAKE MOVE {move} SEQUENCE {self.moveSequence}\n')
			file.close()
		self.board.makeMove(move, self.sideToMove)
		
		# TODO Update castling flags when king or rook moves.

		# If castling, update castle flags.
		if move.flag == 0x02 or move.flag == 0x03:
			# King castle
			if self.sideToMove == WHITE:
				self.wkCastle = 0
				self.wqCastle = 0
			else:
				self.bkCastle = 0
				self.bqCastle = 0


		self.sideToMove = WHITE if self.sideToMove == BLACK else BLACK
		return

	def unmakeMove(self, move: 'Move'):
		# TODO Captures, en passants, promotions, halfmove clock
		#self.sideToMove = WHITE if self.sideToMove == BLACK else BLACK
		if self.debug:
			file = open("Position_log.txt", "a")
			file.write(f'{self.sideToMove} UNMAKE MOVE {move}\n')
			file.close()
		self.board.unmakeMove(move, INVERT(self.sideToMove))
		self.moveSequence.pop()

		# If castling, update castle flags.
		# TODO This can lead to false results if one side initially had a flag of 0 before the move.
		# It might be better to store castling flags in a stack in the Position.
		if move.flag == 0x02 or move.flag == 0x03:
			# King castle
			if self.sideToMove == WHITE:
				self.wkCastle = 1
				self.wqCastle = 1
			else:
				self.bkCastle = 1
				self.bqCastle = 1

		self.sideToMove = WHITE if self.sideToMove == BLACK else BLACK
		return

	def score(self):
		# Use NegaMax
		# Todo: Add mobility count
		# https://www.chessprogramming.org/Evaluation
		_score = 9 * (POPCOUNT(self.board.pieceBoards[WHITE][QUEEN]) - POPCOUNT(self.board.pieceBoards[BLACK][QUEEN])) \
			+ 5 * (POPCOUNT(self.board.pieceBoards[WHITE][ROOK]) - POPCOUNT(self.board.pieceBoards[BLACK][ROOK])) \
			+ 3 * (POPCOUNT(self.board.pieceBoards[WHITE][KNIGHT]) - POPCOUNT(self.board.pieceBoards[BLACK][KNIGHT])) \
			+ 3 * (POPCOUNT(self.board.pieceBoards[WHITE][BISHOP]) - POPCOUNT(self.board.pieceBoards[BLACK][BISHOP])) \
			+ (POPCOUNT(self.board.pieceBoards[WHITE][PAWN]) - POPCOUNT(self.board.pieceBoards[BLACK][PAWN]))

		_score -= 0.5 * (self.board.doubledPawnCount(WHITE) - self.board.doubledPawnCount(BLACK))
		_score -= 0.5 * (self.board.isolatedPawnCount(WHITE) - self.board.isolatedPawnCount(BLACK))
		_score -= 0.5 * (self.board.blockedPawnCount(WHITE) - self.board.blockedPawnCount(BLACK))

		return _score if self.sideToMove == WHITE else -1 * _score

	def traverse(self, ply):
		if ply == 0:
			return 0

		from movegen import generateAllMoves
		moves = generateAllMoves(self)
		nMoves = len(moves)
		for move in moves:
			#expected = deepcopy(self)
			self.makeMove(move)
			nMoves += self.traverse(ply-1)
			self.unmakeMove(move)
			#if self != expected:
				#from printer import printCBoard
				#printCBoard(expected.board)
				#printCBoard(self.board)
				#raise Exception(f"Positions not equivalent: {move.capturedPieceType}\n{self.moveSequence}")
		
		return nMoves

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
				print(self)
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


		
