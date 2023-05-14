from bitboard import *
from board import *
from rays import RAYS
from printer import *
from ctypes import *

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

def northOne2(b: c_uint64):
	return b.value << 8

def southOne(b: np.uint64()) -> np.uint64():
	return b >> np.uint64(8)



def generateAllMoves(position: Position):
	moves = []
	# Missing
	if position.sideToMove == Color.WHITE:
		# Still missing Pawn Capture And Promotion and En Passant moves.
		moves.extend(wGeneratePawnPushMoves(position))
		moves.extend(wGenerateDoublePawnPushMoves(position))
		moves.extend(wGeneratePawnCaptures(position))
	else:
		moves.extend(bGeneratePawnPushMoves(position))
		moves.extend(bGenerateDoublePawnPushMoves(position))
		moves.extend(bGeneratePawnCaptures(position))
	moves.extend(generateBishopMoves(position))
	moves.extend(generateKnightMoves(position))
	moves.extend(generateRookMoves(position))
	moves.extend(generateQueenMoves(position))
	moves.extend(generateKingMoves(position))
	
	
	return moves

def wGenerateAllPawnMoves(position: Position):
	pass

def wGeneratePawnPushMoves(position: Position) -> list:
	board = position.board
	toBoard: np.uint64() = northOne(board.pieceBoards[(Color.WHITE, Piece.P)]) & ~board.occupied & ~EIGHTH_RANK

	# Promotions are handled elsewhere, so pawns on the seventh rank are ignored.
	#eligiblePawns = southOne(toBoard) & ~SEVENTH_RANK

	moves = []
	while toBoard > 0:
		destination = Square(BSF(toBoard))
		origin = Square(destination.value - 8)
		moves.append(Move(origin, destination))
		toBoard ^= SQUARE_TO_BITBOARD[destination.value]

	""" 
	while eligiblePawns > 0:
		origin = np.uint64(BSF(eligiblePawns))
		eligiblePawns ^= SQUARE_TO_BITBOARD[origin]
		#eligiblePawns ^= np.uint64(0x01) << origin

		destination =  np.uint64(BSF(toBoard))
		toBoard ^= SQUARE_TO_BITBOARD[destination]
		#toBoard ^= np.uint64(0x01) << destination

		moves.append(Move(origin=Square(origin), destination=Square(destination))) """

	return moves

def bGeneratePawnPushMoves(position: Position) -> list:
	#board = position.board
	#toBoard: np.uint64() = southOne(board.pieceBoards[(Color.BLACK, Piece.P)]) & ~board.occupied & ~FIRST_RANK
	# Promotions are handled elsewhere, so pawns on the second rank are ignored.
	#eligiblePawns = northOne(toBoard) & ~SECOND_RANK
	
	
	moves = []
	"""
	while toBoard > 0:
		destination = Square(BSF(toBoard))
		origin = Square(destination.value + 8)
		moves.append(Move(origin, destination))
		##print(SQUARE_TO_BITBOARD[destination.value])
		
		toBoard ^= SQUARE_TO_BITBOARD[destination.value]
	"""
	for i in reversed(range(8, 56)):
		if position.board.pieceLocations[i] != Piece.P:
			continue

		if SQUARE_TO_BITBOARD[i] & position.board.pieceBoards[(Color.BLACK, Piece.P)]:
			if position.board.pieceLocations[i-8] == None:
				moves.append(Move(Square(i), Square(i-8)))


	"""
	moves = []
	while eligiblePawns > 0:
		origin = np.uint64(BSF(eligiblePawns))
		eligiblePawns ^= np.uint64(0x01) << origin

		destination =  np.uint64(BSF(toBoard))
		toBoard ^= np.uint64(0x01) << destination

		moves.append(Move(origin=Square(origin), destination=Square(destination)))"""

	return moves

def wGenerateDoublePawnPushMoves(position: Position) -> list:
	board = position.board
	toBoard = northOne(northOne(SECOND_RANK & board.pieceBoards[(Color.WHITE, Piece.P)]) & ~board.occupied) & ~board.occupied
	eligiblePawns = southOne(southOne(toBoard))

	fromSingles = singularize(eligiblePawns)
	toSingles = singularize(toBoard)

	if (Square.A2.bitboard() | position.board.pieceBoards[(Color.WHITE, Piece.P)]) and not (Square.A3.bitboard() | Square.A4.bitboard()) & board.occupied:
		pass

	moves = []
	while eligiblePawns > 0:
		origin = np.uint64(BSF(eligiblePawns))
		eligiblePawns ^= np.uint64(0x01) << origin

		destination =  np.uint64(BSF(toBoard))
		toBoard ^= np.uint64(0x01) << destination

		moves.append(Move(origin=Square(origin), destination=Square(destination), flag=0x01))

	return moves

def bGenerateDoublePawnPushMoves(position: Position) -> list:
	board = position.board
	toBoard = southOne(southOne(SECOND_RANK & board.pieceBoards[(Color.BLACK, Piece.P)]) & ~board.occupied) & ~board.occupied
	eligiblePawns = northOne(northOne(toBoard))

	moves = []
	while eligiblePawns > 0:
		origin = np.uint64(BSF(eligiblePawns))
		eligiblePawns ^= np.uint64(0x01) << origin

		destination =  np.uint64(BSF(toBoard))
		toBoard ^= np.uint64(0x01) << destination

		moves.append(Move(origin=Square(origin), destination=Square(destination), flag=0x01))

	return moves

def wGeneratePawnCaptures(position: Position) -> list:
	board = position.board
	
	# Eigth-rank pawn captures are handled in wGeneratePromotionAndCaptureMoves
	singlePawns = singularize(board.pieceBoards[(Color.WHITE, Piece.P)] & ~SEVENTH_RANK)

	moves = []
	for i in range(len(singlePawns)):
		if noWe(singlePawns[i]) & board.blackBoard:
			origin = Square(BSF(singlePawns[i]))
			destination = Square(origin + 7)
			capturedPieceType = position.board.pieceTypeAtSquare(destination)
			moves.append(Move(origin, destination, flag=0x04, capturedPieceType=capturedPieceType))

		if noEa(singlePawns[i]) & board.blackBoard:
			origin = Square(BSF(singlePawns[i]))
			destination = Square(origin + 9)
			capturedPieceType = position.board.pieceTypeAtSquare(destination)
			moves.append(Move(origin, destination, flag=0x04, capturedPieceType=capturedPieceType))

	return moves

def bGeneratePawnCaptures(position: Position) -> list:
	board = position.board

	# First-rank pawn captures are handled in bGeneratePromotionAndCaptureMoves
	singlePawns = singularize(board.pieceBoards[(Color.BLACK, Piece.P)] & ~SECOND_RANK)
	moves = []
	for i in range(len(singlePawns)):
		if soWe(singlePawns[i]) & board.whiteBoard:
			origin = Square(BSF(singlePawns[i]))
			destination = Square(origin - 9)
			capturedPieceType = position.board.pieceTypeAtSquare(destination)
			moves.append(Move(origin, destination, flag=0x04, capturedPieceType=capturedPieceType))

		if soEa(singlePawns[i]) & board.whiteBoard:
			origin = Square(BSF(singlePawns[i]))
			destination = Square(origin - 7)
			capturedPieceType = position.board.pieceTypeAtSquare(destination)
			moves.append(Move(origin, destination, flag=0x04, capturedPieceType=capturedPieceType))

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

def generateKnightMoves(position: Position) -> list:
	if not position.board.pieceBoards[(Color.WHITE, Piece.N)] and position.sideToMove == Color.BLACK:
		return []

	if not position.board.pieceBoards[(Color.BLACK, Piece.N)] and position.sideToMove == Color.BLACK:
		return []

	# Make copy to avoid modifying the actual board.
	knights = position.board.pieceBoards[(Color.WHITE, Piece.N)] if position.sideToMove == Color.WHITE else position.board.pieceBoards[(Color.BLACK, Piece.N)]
	pseudolegalMoves = []
	while knights:
		origin = np.uint64(0x01) << np.uint64(BSF(knights))
		knights ^= origin
		possibleMoves = knightMoves(origin)
		for move in possibleMoves:
			destination: Square = move.destination
			bb: np.uint64() = np.uint64(0x01) << np.uint64(destination.value)
			if bb & position.board.whiteBoard and position.sideToMove == Color.WHITE:
				# Intersects own pieces, ignore move.
				continue
			elif bb & position.board.whiteBoard and position.sideToMove == Color.BLACK:
				# Capture
				move.flag=0x04
				move.capturedPieceType = position.board.pieceTypeAtSquare(move.destination)
				pseudolegalMoves.append(move)
			elif bb & position.board.blackBoard and position.sideToMove == Color.BLACK:
				# Intersects own pieces, ignore move.
				continue
			elif bb & position.board.blackBoard and position.sideToMove == Color.WHITE:
				move.flag=0x04
				move.capturedPieceType = position.board.pieceTypeAtSquare(move.destination)
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
		sqOrigin = Square(BSF(position.board.pieceBoards[(Color.WHITE, Piece.K)]))
	else:
		sqOrigin = Square(BSF(position.board.pieceBoards[(Color.BLACK, Piece.K)]))

	bbToBoard = kingAttacks(sqOrigin)
	pseudolegalMoves = []
	while bbToBoard:
		sqDestination: Square = Square(BSF(bbToBoard))
		bbDestination = sqDestination.bitboard()
		bbToBoard ^= bbDestination
		if bbDestination & position.board.whiteBoard and position.sideToMove == Color.WHITE:
			# Intersects own pieces. Ignore move.
			continue
		elif bbDestination & position.board.blackBoard and position.sideToMove == Color.WHITE:
			# Capture
			pseudolegalMoves.append(Move(sqOrigin, sqDestination, flag=0x04, capturedPieceType=position.board.pieceTypeAtSquare(sqDestination)))
		elif bbDestination & position.board.whiteBoard and position.sideToMove == Color.BLACK:
			# Capture
			pseudolegalMoves.append(Move(sqOrigin, sqDestination, 0x04, capturedPieceType=position.board.pieceTypeAtSquare(sqDestination)))
		elif bbDestination & position.board.blackBoard and position.sideToMove == Color.BLACK:
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

def rookAttacks(sq: Square, blockers: np.uint64()):
	north_attacks = RAYS[Dir.NORTH][sq.value]
	if north_attacks & blockers:
		blockerIdx = BSF(north_attacks & blockers)
		north_attacks &= ~RAYS[Dir.NORTH][blockerIdx]

	east_attacks = RAYS[Dir.EAST][sq]
	if east_attacks & blockers:
		blockerIdx = BSF(east_attacks & blockers)
		east_attacks &= ~RAYS[Dir.EAST][blockerIdx]

	south_attacks = RAYS[Dir.SOUTH][sq.value]
	if south_attacks & blockers:
		blockerIdx = BSR(south_attacks & blockers)
		south_attacks &= ~RAYS[Dir.SOUTH][blockerIdx]

	west_attacks = RAYS[Dir.WEST][sq]
	if west_attacks & blockers:
		blockerIdx = BSR(west_attacks & blockers)
		west_attacks &= ~RAYS[Dir.WEST][blockerIdx]

	return north_attacks | east_attacks | south_attacks | west_attacks

def generateRookMoves(position: Position):
	if position.sideToMove == Color.WHITE:
		rooks = position.board.pieceBoards[(Color.WHITE, Piece.R)]
	else:
		rooks = position.board.pieceBoards[(Color.BLACK, Piece.R)]

	moves = []
	while rooks:
		sqOrigin = Square(BSF(rooks))
		rooks ^= sqOrigin.bitboard()

		blockers = position.board.occupied ^ sqOrigin.bitboard()
		bbDestinations = rookAttacks(sqOrigin, blockers)
		while bbDestinations:
			sqDestination = Square(BSF(bbDestinations))
			
			bbDestinations ^= sqDestination.bitboard()

			if sqDestination.isEmpty(position.board):
				moves.append(Move(sqOrigin, sqDestination))
			elif sqDestination.bitboard() & position.board.whiteBoard:
				if position.sideToMove == Color.BLACK:
					moves.append(Move(sqOrigin, sqDestination, flag=0x04, capturedPieceType=position.board.pieceTypeAtSquare(sqDestination)))
			else:
				if position.sideToMove == Color.WHITE:
					moves.append(Move(sqOrigin, sqDestination, flag=0x04, capturedPieceType=position.board.pieceTypeAtSquare(sqDestination)))

	return moves

def bishopAttacks(sq: Square, blockers: np.uint64()):
	nw_attacks = RAYS[Dir.NORTH_WEST][sq]
	if RAYS[Dir.NORTH_WEST][sq] & blockers:
		blockerIdx = BSF(RAYS[Dir.NORTH_WEST][sq] & blockers)
		nw_attacks &= ~RAYS[Dir.NORTH_WEST][blockerIdx]

	ne_attacks = RAYS[Dir.NORTH_EAST][sq]
	if RAYS[Dir.NORTH_EAST][sq] & blockers:
		blockerIdx = BSF(RAYS[Dir.NORTH_EAST][sq] & blockers)
		ne_attacks &= ~RAYS[Dir.NORTH_EAST][blockerIdx]

	se_attacks = RAYS[Dir.SOUTH_EAST][sq]
	if se_attacks & blockers:
		blockerIdx = BSR(se_attacks & blockers)
		se_attacks &= ~RAYS[Dir.SOUTH_EAST][blockerIdx]

	sw_attacks = RAYS[Dir.SOUTH_WEST][sq]
	if RAYS[Dir.SOUTH_WEST][sq] & blockers:
		blockerIdx = BSR(RAYS[Dir.SOUTH_WEST][sq] & blockers)
		sw_attacks &= ~RAYS[Dir.SOUTH_WEST][blockerIdx]
	return nw_attacks | ne_attacks | se_attacks | sw_attacks

def generateBishopMoves(position: Position):
	if position.sideToMove == Color.WHITE:
		bishops = position.board.pieceBoards[(Color.WHITE, Piece.B)]
	else:
		bishops = position.board.pieceBoards[(Color.BLACK, Piece.B)]

	moves = []
	while bishops:
		sqOrigin = Square(BSF(bishops))
		bishops ^= sqOrigin.bitboard()

		blockers = position.board.occupied ^ sqOrigin.bitboard()
		bbDestinations = bishopAttacks(sqOrigin, blockers)

		while bbDestinations:
			sqDestination = Square(BSF(bbDestinations))
			
			bbDestinations ^= sqDestination.bitboard()
			if sqDestination.isEmpty(position.board):
				moves.append(Move(sqOrigin, sqDestination))
			elif sqDestination.bitboard() & position.board.whiteBoard:
				if position.sideToMove == Color.BLACK:
					moves.append(Move(sqOrigin, sqDestination, flag=0x04, capturedPieceType=position.board.pieceTypeAtSquare(sqDestination)))
			else:
				if position.sideToMove == Color.WHITE:
					moves.append(Move(sqOrigin, sqDestination, flag=0x04, capturedPieceType=position.board.pieceTypeAtSquare(sqDestination)))
	return moves
		
def generateQueenMoves(position):
	if position.sideToMove == Color.WHITE:
		queens = position.board.pieceBoards[(Color.WHITE, Piece.Q)]
	else:
		queens = position.board.pieceBoards[(Color.BLACK, Piece.Q)]

	moves = []
	while queens:
		sqOrigin = Square(BSF(queens))
		queens ^= sqOrigin.bitboard()
		blockers = position.board.occupied ^ sqOrigin.bitboard()
		bbDestinations = bishopAttacks(sqOrigin, blockers) | rookAttacks(sqOrigin, blockers)
		while bbDestinations:
			sqDestination = Square(BSF(bbDestinations))
			
			bbDestinations ^= sqDestination.bitboard()
			if sqDestination.isEmpty(position.board):
				moves.append(Move(sqOrigin, sqDestination))
			elif sqDestination.bitboard() & position.board.whiteBoard:
				if position.sideToMove == Color.BLACK:
					moves.append(Move(sqOrigin, sqDestination, flag=0x04, capturedPieceType=position.board.pieceTypeAtSquare(sqDestination)))
			else:
				if position.sideToMove == Color.WHITE:
					moves.append(Move(sqOrigin, sqDestination, flag=0x04, capturedPieceType=position.board.pieceTypeAtSquare(sqDestination)))
	return moves

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
