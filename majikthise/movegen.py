from bitboard import *
from board import *

# Knight moves
def noNoEa(b: np.uint64()) -> np.uint64(): 
	return (b << np.uint64(17)) & ~A_FILE

def noEaEa(b: np.uint64()) -> np.uint64():
	return (b << np.uint64(10)) & ~A_FILE & ~B_FILE

def soEaEa(b: np.uint64()) -> np.uint64():
	return (b >> np.uint64(6)) & ~A_FILE & ~B_FILE

def soSoEa(b: np.uint64()) -> np.uint64():
	return (b >> np.uint64(15)) & ~A_FILE

def noNoWe(b: np.uint64()) -> np.uint64():
	return (b << np.uint64(15)) & ~H_FILE

def noWeWe(b: np.uint64()) -> np.uint64():
	return (b << np.uint64(6)) & ~H_FILE & ~G_FILE

def soWeWe(b: np.uint64()) -> np.uint64():
	return (b >> np.uint64(10)) & ~H_FILE & ~G_FILE

def soSoWe(b: np.uint64()) -> np.uint64():
	return (b >> np.uint64(17)) & ~H_FILE

def noWe(b: np.uint64()) -> np.uint64():
	return (b << np.uint64(7)) & ~H_FILE

def noEa(b: np.uint64()) -> np.uint64():
	return (b << np.uint64(9)) & ~A_FILE

def soWe(b: np.uint64()) -> np.uint64():
	return (b >> np.uint64(9)) & ~H_FILE

def soEa(b: np.uint64()) -> np.uint64():
	return (b >> np.uint64(7)) & ~A_FILE

def northOne(b: np.uint64()) -> np.uint64():
	return b << np.uint64(8)

def southOne(b: np.uint64()) -> np.uint64():
	return b >> np.uint64(8)


def wGenerateAllMoves(position: Position):
	pass

def wGenerateBishopMoves(b: CBoard) -> list[Move]:
	pass

def wGenerateAllPawnMoves(position: Position):
	pass

def wGeneratePawnPushMoves(board: CBoard) -> list:
	occupied: np.uint64() = WHITE_BOARD(board) | BLACK_BOARD(board)
	toBoard: np.uint64() = northOne(board.whitePawns) & ~occupied

	# Promotions are handled elsewhere, so pawns on the seventh rank are ignored.
	eligiblePawns = southOne(toBoard) & ~SEVENTH_RANK

	fromSingles = singularize(eligiblePawns)
	toSingles = singularize(toBoard)

	moves = []
	for i in range(len(fromSingles)):
		origin = Square(BSF(fromSingles[i]))
		destination = Square(BSF(toSingles[i]))
		moves.append(Move(origin=origin, destination=destination))

	return moves

def bGeneratePawnPushMoves(board: CBoard) -> list:
	occupied: np.uint64() = WHITE_BOARD(board) | BLACK_BOARD(board)
	toBoard: np.uint64() = southOne(board.blackPawns) & ~occupied

	# Promotions are handled elsewhere, so pawns on the second rank are ignored.
	eligiblePawns = northOne(toBoard) & ~SECOND_RANK

	fromSingles = singularize(eligiblePawns)
	toSingles = singularize(toBoard)

	moves = []
	for i in range(len(fromSingles)):
		origin = Square(BSF(fromSingles[i]))
		destination = Square(BSF(toSingles[i]))
		moves.append(Move(origin=origin, destination=destination))

	return moves

def wGenerateDoublePawnPushMoves(board: CBoard) -> list[Move]:
	occupied = WHITE_BOARD(board) | BLACK_BOARD(board)
	toBoard = northOne(northOne(SECOND_RANK & board.whitePawns) & ~occupied) & ~occupied
	eligiblePawns = southOne(southOne(toBoard))

	fromSingles = singularize(eligiblePawns)
	toSingles = singularize(toBoard)

	moves = []
	for i in range(len(fromSingles)):
		origin = Square(BSF(fromSingles[i]))
		destination = Square(BSF(toSingles[i]))
		moves.append(Move(origin=origin, destination=destination))

	return moves

def bGenerateDoublePawnPushMoves(board: CBoard) -> list[Move]:
	occupied = WHITE_BOARD(board) | BLACK_BOARD(board)
	toBoard = southOne(southOne(SECOND_RANK & board.blackPawns) & ~occupied) & ~occupied
	eligiblePawns = northOne(northOne(toBoard))

	fromSingles = singularize(eligiblePawns)
	toSingles = singularize(toBoard)

	moves = []
	for i in range(len(fromSingles)):
		origin = Square(BSF(fromSingles[i]))
		destination = Square(BSF(toSingles[i]))
		moves.append(Move(origin=origin, destination=destination))

	return moves

def wGeneratePawnCaptures(board: CBoard) -> list[Move]:
	# Eigth-rank pawn captures are handles in wGeneratePromotionAndCaptureMoves
	singlePawns = singularize(board.whitePawns & ~SEVENTH_RANK)

	moves = []
	for i in range(len(singlePawns)):
		if noWe(singlePawns[i]) & BLACK_BOARD(board):
			origin = Square(BSF(singlePawns[i]))
			destination = Square(origin + 7)
			moves.append(origin, destination, flag=0x04)

		if noEa(singlePawns[i]) & BLACK_BOARD(board):
			origin = Square(BSF(singlePawns[i]))
			destination = Square(origin + 9)
			moves.append(origin, destination, flag=0x04)

	return moves

def bGeneratePawnCaptures(board: CBoard) -> list[Move]:
	# First-rank pawn captures are handled in bGeneratePromotionAndCaptureMoves
	singlePawns = singularize(board.blackPawns & ~SECOND_RANK)
	for i in range(len(singlePawns)):
		if soWe(singlePawns[i]) & WHITE_BOARD(board):
			origin = Square(BSF(singlePawns[i]))
			destination = Square(origin - 9)
			moves.append(origin, destination, flag=0x04)

		if soEa(singlePawns[i]) & WHITE_BOARD(board):
			origin = Square(BSF(singlePawns[i]))
			destination = Square(origin - 7)
			moves.append(origin, destination, flag=0x04)

	return moves

def knightAttacks(sq: Square) -> np.uint64():
	board = np.uint64(1 << sq)
	return noNoEa(board) | noEaEa(board) | soEaEa(board) | soSoEa(board) | noNoWe(board) | noWeWe(board) | soWeWe(board) | soSoWe(board)

# Generate the moves for a board with a single knight.
def knightMoves(board) -> list:
	assert POPCOUNT(board) == 1
	origin = BSF(board)
	toBoard = knightAttacks(board)

	toSingles = singularize(toBoard)
	moves = []
	for i in range(len(toSingles)):
		destination = BSF(toSingles[i])
		moves.append(origin=origin, destination=destination)

	return moves

def wGenerateKnightMoves(board) -> list:
	if not board.whiteKnights:
		return []

	fromSingles = singularize(board.whiteKnights)

	for knight in fromSingles:
		moves = knightMoves(knight)
		# for each move,
		# 	if the destination intersects black's occupied board, update the flag
		#	if the move would leave white in check, remove the move from the list.

def kingAttacks(sq: Square) -> np.uint64():
	board = np.uint64(1 << sq)
	return ((board << 1) & ~A_FILE) | ((board >> 1) & ~H_FILE) | board << 8 | board >> 8 | noWe(board) | noEa(board) | soWe(board) | soEa(board);

# Given any bitboard, return a list of bitboards with only one piece per board.
def singularize(b: np.uint64()) -> list:
	count = 0
	singles = []
	while (b):
		pos = np.uint64(BSF(b))
		singles.append(np.uint64(1) << pos)
		count += 1
		b ^= np.uint64(1) << pos

	return singles
