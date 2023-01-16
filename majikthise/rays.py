import numpy as np

from board import *
from bitboard import *

a = 1
RAYS = [[np.uint64(0)] * 64 for i in range(8)] # of type Board


# Source: https://www.chessprogramming.org/On_an_empty_Board

def initRays():
	for sq in range(np.uint64(64)):
		sq = np.uint64(sq)
		RAYS[Dir.NORTH][sq] = np.uint64(0x0101010101010100) << sq
		RAYS[Dir.SOUTH][sq] = np.uint64(0x0080808080808080) >> (np.uint64(63)-sq)
		RAYS[Dir.EAST][sq] = np.uint64(2) * ((np.uint64(1) << (sq | np.uint64(7))) - (np.uint64(1) << sq))
		RAYS[Dir.WEST][sq] = ((np.uint64(1) << (sq)) - np.uint64(1)) ^ ((np.uint64(1) << (sq//np.uint64(8))*np.uint64(8)) - np.uint64(1))

	diag: np.uint64() = A1_H8_DIAGONAL
	for rank in range(8):
		diag = diag >> np.uint64(1) & ~H_FILE
		diag2 = diag
		for file in range(8):
			diag2 = (diag2 << np.uint64(1)) & ~A_FILE
			RAYS[Dir.NORTH_EAST][rank*8+file] = diag2

	diag = A1_H8_DIAGONAL
	for rank in reversed(range(8)):
		diag = (diag << np.uint64(1)) & ~A_FILE
		diag2 = diag
		for file in reversed(range(8)):
			diag2 = (diag2 >> np.uint64(1)) & ~H_FILE
			RAYS[Dir.SOUTH_WEST][rank*8+file] = diag2

	diag = H1_A8_ANTIDIAGONAL
	for rank in range(8):
		diag = (diag << np.uint64(1)) & ~A_FILE
		diag2 = diag
		for file in reversed(range(8)):
			diag2 = (diag2 >> np.uint64(1)) & ~H_FILE
			RAYS[Dir.NORTH_WEST][rank*8+file] = diag2

	diag = H1_A8_ANTIDIAGONAL
	for rank in reversed(range(8)):
		diag = (diag >> np.uint64(1)) & ~H_FILE
		diag2 = diag
		for file in range(8):
			diag2 = (diag2 << np.uint64(1)) & ~A_FILE
			RAYS[Dir.SOUTH_EAST][rank*8+file] = diag2
	