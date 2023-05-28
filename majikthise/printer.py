import numpy as np

from board import CBoard, Position

def printBitboard(bitboard: np.uint64()):
	toPrint = ['\n']
	for row in reversed(range(8)):
		for file in range(8):
			c = '1' if (bitboard >> (row * 8 + file)) & 1 else '0'
			toPrint.append(c)
		toPrint.append('\n')
	print(''.join(toPrint))

def printCBoard(board: CBoard):
	printBitboard(board.whiteBoard | board.blackBoard)

def printCBoardDiff(first: CBoard, second: CBoard):
	if first.whiteBoard != second.whiteBoard:
		print("The difference is in the white board.")

	if first.blackBoard != second.blackBoard:
		print("The difference is in the black board.")

	if first.pieceBoards != second.pieceBoards:
		print("The difference is in the piece boards. If you loaded the position by FEN, did you forget to set sideToMove?")

def printPositionDiff(first: Position, second: Position):
	if first.board != second.board:
		print("The difference is in the boards")
	
	if first.sideToMove != second.sideToMove:
		print("The difference is in the side to move.")

	if (first.bkCastle != second.bkCastle) or (first.bqCastle != second.bqCastle):
		print("The difference is in the black castling rules.")

	if (first.wkCastle != second.wkCastle) or (first.wqCastle != second.wqCastle):
		print("The difference is in the white castling rules.")
