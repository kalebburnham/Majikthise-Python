import numpy as np

from board import *
from bitboard import *
from constants import *

a = 1
RAYS = [[<size_t> 0] * 64 for i in range(8)] # of type Board


# Source: https://www.chessprogramming.org/On_an_empty_Board

cpdef initRays():
	cdef size_t diag
	cdef size_t diag2

	for sq in range(64):
		RAYS[Dir.NORTH][sq] = <size_t> 0x0101010101010100 << <size_t> sq
		RAYS[Dir.SOUTH][sq] = <size_t> 0x0080808080808080 >> (<size_t> 63-<size_t> sq)
		RAYS[Dir.EAST][sq] = <size_t> (2 * ((1 << (sq | 7)) - (1 << sq)))
		RAYS[Dir.WEST][sq] = <size_t> (((1 << sq) - 1) ^ ((1 << (sq//8)*8) - 1))

	diag = A1_H8_DIAGONAL
	
	for rank in range(8):
		diag = diag >> 1 & ~H_FILE
		diag2 = diag
		for file in range(8):
			diag2 = (diag2 << 1) & ~A_FILE
			RAYS[Dir.NORTH_EAST][rank*8+file] = <size_t> diag2

	diag = A1_H8_DIAGONAL
	for rank in reversed(range(8)):
		diag = (diag << 1) & ~A_FILE
		diag2 = diag
		for _file in reversed(range(8)):
			diag2 = (diag2 >> 1) & ~H_FILE
			RAYS[Dir.SOUTH_WEST][rank*8+_file] = <size_t> diag2

	diag = H1_A8_ANTIDIAGONAL
	for rank in range(8):
		diag = (diag << 1) & ~A_FILE
		diag2 = diag
		for _file in reversed(range(8)):
			diag2 = (diag2 >> 1) & ~H_FILE
			RAYS[Dir.NORTH_WEST][rank*8+_file] = <size_t> diag2

	diag = H1_A8_ANTIDIAGONAL
	for rank in reversed(range(8)):
		diag = (diag >> 1) & ~H_FILE
		diag2 = diag
		for _file in range(8):
			diag2 = (diag2 << 1) & ~A_FILE
			RAYS[Dir.SOUTH_EAST][rank*8+_file] = <size_t> diag2
	