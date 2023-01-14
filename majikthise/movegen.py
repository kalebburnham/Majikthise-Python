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

def wGenerateBishopMoves(b: CBoard) -> list:
	pass

def wGenerateAllPawnMoves(position: Position):
	pass

def wGeneratePawnPushMoves(board: CBoard) -> list:
	occupied: np.uint64() = WHITE_BOARD(board) | BLACK_BOARD(board)
	toBoard: np.uint64() = northOne(board.whitePawns) & ~occupied

	# Promotions are handled elsewhere, so pawns on the seventh rank are ignored.
	eligiblePawns = southOne(toBoard) & ~SEVENTH_RANK

	moves = []
	while eligiblePawns > 0:
		origin = np.uint64(BSF(eligiblePawns))
		eligiblePawns ^= np.uint64(0x01) << origin

		destination =  np.uint64(BSF(toBoard))
		toBoard ^= np.uint64(0x01) << destination

		moves.append(Move(origin=Square(origin), destination=Square(destination)))

	return moves

def bGeneratePawnPushMoves(board: CBoard) -> list:
	occupied: np.uint64() = WHITE_BOARD(board) | BLACK_BOARD(board)
	toBoard: np.uint64() = southOne(board.blackPawns) & ~occupied

	# Promotions are handled elsewhere, so pawns on the second rank are ignored.
	eligiblePawns = northOne(toBoard) & ~SECOND_RANK

	moves = []
	while eligiblePawns > 0:
		origin = np.uint64(BSF(eligiblePawns))
		eligiblePawns ^= np.uint64(0x01) << origin

		destination =  np.uint64(BSF(toBoard))
		toBoard ^= np.uint64(0x01) << destination

		moves.append(Move(origin=Square(origin), destination=Square(destination)))

	return moves

def wGenerateDoublePawnPushMoves(board: CBoard) -> list:
	occupied = WHITE_BOARD(board) | BLACK_BOARD(board)
	toBoard = northOne(northOne(SECOND_RANK & board.whitePawns) & ~occupied) & ~occupied
	eligiblePawns = southOne(southOne(toBoard))

	fromSingles = singularize(eligiblePawns)
	toSingles = singularize(toBoard)

	moves = []
	while eligiblePawns > 0:
		origin = np.uint64(BSF(eligiblePawns))
		eligiblePawns ^= np.uint64(0x01) << origin

		destination =  np.uint64(BSF(toBoard))
		toBoard ^= np.uint64(0x01) << destination

		moves.append(Move(origin=Square(origin), destination=Square(destination)))

	return moves

def bGenerateDoublePawnPushMoves(board: CBoard) -> list:
	occupied = WHITE_BOARD(board) | BLACK_BOARD(board)
	toBoard = southOne(southOne(SECOND_RANK & board.blackPawns) & ~occupied) & ~occupied
	eligiblePawns = northOne(northOne(toBoard))

	moves = []
	while eligiblePawns > 0:
		origin = np.uint64(BSF(eligiblePawns))
		eligiblePawns ^= np.uint64(0x01) << origin

		destination =  np.uint64(BSF(toBoard))
		toBoard ^= np.uint64(0x01) << destination

		moves.append(Move(origin=Square(origin), destination=Square(destination)))

	return moves

def wGeneratePawnCaptures(board: CBoard) -> list:
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

def bGeneratePawnCaptures(board: CBoard) -> list:
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
	board = np.uint64(1 << sq.value)
	return noNoEa(board) | noEaEa(board) | soEaEa(board) | soSoEa(board) | noNoWe(board) | noWeWe(board) | soWeWe(board) | soSoWe(board)

# Generate the moves for a board with a single knight.
def knightMoves(board: np.uint64()) -> list:
	assert POPCOUNT(board) == 1
	origin = BSF(board)
	toBoard = knightAttacks(Square(origin))

	moves = []
	while toBoard:
		destination = np.uint64(BSF(toBoard))
		toBoard ^= np.uint64(0x01) << destination

		moves.append(Move(Square(origin), Square(destination)))
		
	return moves

def generateKnightMoves(board, color_to_move: Color) -> list:
	if not board.whiteKnights and color_to_move == Color.BLACK:
		return []

	if not board.blackKnights and color_to_move == Color.BLACK:
		return []

	# Make copy to avoid modifying the actual board.
	knights = board.whiteKnights if color_to_move == Color.WHITE else board.blackKnights

	pseudolegalMoves = []
	while knights:
		origin = np.uint64(0x01) << np.uint64(BSF(knights))
		knights ^= origin
		possibleMoves = knightMoves(origin)
		for move in possibleMoves:
			destination: Square = move.destination
			bb: np.uint64() = np.uint64(0x01) << np.uint64(destination.value)
			if bb & WHITE_BOARD(board) and color_to_move == Color.WHITE:
				# Intersects own pieces, ignore move.
				continue
			elif bb & WHITE_BOARD(board) and color_to_move == Color.BLACK:
				# Capture
				move.flag=0x04
				pseudolegalMoves.append(move)
			elif bb & BLACK_BOARD(board) and color_to_move == Color.BLACK:
				# Intersects own pieces, ignore move.
				continue
			elif bb & BLACK_BOARD(board) and color_to_move == Color.WHITE:
				move.flag=0x04
				pseudolegalMoves.append(move)
			else:
				# Quiet move.
				pseudolegalMoves.append(move)

	return pseudolegalMoves

def kingAttacks(sq: Square) -> np.uint64():
	''' Return a bitboard of the squares a king can move to from the given square. '''
	board = np.uint64(1 << sq)
	return ((board << np.uint64(1)) & ~A_FILE) | ((board >> np.uint64(1)) & ~H_FILE) | board << np.uint64(8) | board >> np.uint64(8) | noWe(board) | noEa(board) | soWe(board) | soEa(board);

def generateKingMoves(position: Position):
	'''
	Returns a pseudolegal list of Moves for the king.
	This method does not check for legality of a move.
	'''
	if position.sideToMove == Color.WHITE:
		sqOrigin = Square(BSF(position.board.whiteKing))
	else:
		sqOrigin = Square(BSF(position.board.blackKing))

	bbToBoard = kingAttacks(sqOrigin)

	pseudolegalMoves = []
	while bbToBoard:
		sqDestination: Square = Square(BSF(bbToBoard))
		bbDestination = sqDestination.bitboard()
		bbToBoard ^= bbDestination
		if bbDestination & WHITE_BOARD(position.board) and position.sideToMove == Color.WHITE:
			# Intersects own pieces. Ignore move.
			continue
		elif bbDestination & BLACK_BOARD(position.board) and position.sideToMove == Color.WHITE:
			# Capture
			pseudolegalMoves.append(Move(sqOrigin, sqDestination, 0x04))
		elif bbDestination & WHITE_BOARD(position.board) and position.sideToMove == Color.BLACK:
			# Capture
			pseudolegalMoves.append(Move(sqOrigin, sqDestination, 0x04))
		elif bbDestination & BLACK_BOARD(position.board) and position.sideToMove == Color.BLACK:
			# Intersects own pieces. Ignore move.
			continue
		else:
			# Quiet move
			pseudolegalMoves.append(Move(sqOrigin, sqDestination))

	# Castle moves
	if position.sideToMove == Color.WHITE:
		if position.wkCastle and Square.F1.isEmpty(position.board) and Square.G1.isEmpty(position.board):
			pseudolegalMoves.append(Move(origin=sqOrigin, destination=Square.G1, flag=0x02))
		if position.wqCastle and Square.D1.isEmpty(position.board) and Square.C1.isEmpty(position.board) and Square.B1.isEmpty(position.board):
			pseudolegalMoves.append(Move(origin=sqOrigin, destination=Square.C1, flag=0x03))

	else:
		if position.bkCastle and Square.F8.isEmpty(position.board) and Square.G8.isEmpty(position.board):
			pseudolegalMoves.append(Move(origin=sqOrigin, destination=Square.G8, flag=0x02))
		if position.bqCastle and Square.D8.isEmpty(position.board) and Square.C8.isEmpty(position.board) and Square.B8.isEmpty(position.board):
			pseudolegalMoves.append(Move(origin=sqOrigin, destination=Square.C8, flag=0x03))

	return pseudolegalMoves

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
