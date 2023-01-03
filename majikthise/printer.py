import numpy as np

from board import CBoard

def printBitboard(bitboard: np.uint64()):
	toPrint = ['\n']
	for row in reversed(range(8)):
		for file in range(8):
			c = '1' if (bitboard >> np.uint64((row * 8 + file))) & np.uint64(1) else '0'
			toPrint.append(c)
		toPrint.append('\n')
	print(''.join(toPrint))

def printCBoard(board: CBoard):
	whiteBoard = board.whitePawns | board.whiteKnights | board.whiteBishops | board.whiteRooks | board.whiteQueens | board.whiteKing
	blackBoard = board.blackPawns | board.blackKnights | board.blackBishops | board.blackRooks | board.blackQueens | board.blackKing
	printBitboard(whiteBoard | blackBoard)