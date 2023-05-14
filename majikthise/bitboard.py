import numpy as np

A_FILE = np.uint64(0x0101010101010101)
B_FILE = np.uint64(0x0202020202020202)
C_FILE = np.uint64(0x0404040404040404)
D_FILE = np.uint64(0x0808080808080808)
E_FILE = np.uint64(0x1010101010101010)
F_FILE = np.uint64(0x2020202020202020)
G_FILE = np.uint64(0x4040404040404040)
H_FILE = np.uint64(0x8080808080808080)

FIRST_RANK = np.uint64(0x00000000000000FF)
SECOND_RANK = np.uint64(0x000000000000FF00)
THIRD_RANK = np.uint64(0x0000000000FF0000)
FOURTH_RANK = np.uint64(0x00000000FF000000)
FIFTH_RANK = np.uint64(0x000000FF00000000)
SIXTH_RANK = np.uint64(0x0000FF0000000000)
SEVENTH_RANK = np.uint64(0x00FF000000000000)
EIGHTH_RANK = np.uint64(0xFF00000000000000)

A1_H8_DIAGONAL = np.uint64(0x8040201008040201)
H1_A8_ANTIDIAGONAL = np.uint64(0x0102040810204080)
LIGHT_SQUARES = np.uint64(0x55AA55AA55AA55AA)
DARK_SQUARES = np.uint64(0xAA55AA55AA55AA55)

def eastOne(b: np.uint64()) -> np.uint64():
	return (b << np.uint64(1)) & ~A_FILE

def westOne(b: np.uint64()) -> np.uint64():
	return (b >> np.uint64(1)) & ~H_FILE

def northOne(b: np.uint64()) -> np.uint64():
	return b << np.uint64(8)

def southOne(b: np.uint64()) -> np.uint64():
	return b >> np.uint64(8)

# These are called Kogge-Stone algorithms.
# They also exist for lateral and diagonal fills.
def northFill(b) -> np.uint64():
	b |= (b << np.uint64(8))
	b |= (b << np.uint64(16))
	b |= (b << np.uint64(32))
	return b

def southFill(b) -> np.uint64():
	b |= (b >> np.uint64(8))
	b |= (b >> np.uint64(16))
	b |= (b >> np.uint64(32))
	return b

def fileFill(b) -> np.uint64():
	return northFill(b) | southFill(b)

bsf_index = [0,  1, 48,  2, 57, 49, 28,  3,
   61, 58, 50, 42, 38, 29, 17,  4,
   62, 55, 59, 36, 53, 51, 43, 22,
   45, 39, 33, 30, 24, 18, 12,  5,
   63, 47, 56, 27, 60, 41, 37, 16,
   54, 35, 52, 21, 44, 32, 23, 11,
   46, 26, 40, 15, 34, 20, 31, 10,
   25, 14, 19,  9, 13,  8,  7,  6]

# Bit Scan Forward using De Bruijn multiplication
# Undefined for b == 0
# Returns the index of the least significant one bit
# https://www.chessprogramming.org/BitScan#DeBruijnMultiplation
def BSF(b: np.uint64()) -> int:
	debruijn64 = np.uint64(0x03f79d71b4cb0a89)
	#assert b != 0 # Keeping the assert doubles the cost of the function from 1.5 to 3 nanoseconds.
	return bsf_index[((b & -b) * debruijn64) >> np.uint64(58)]

bsr_index = [0, 47,  1, 56, 48, 27,  2, 60,
   57, 49, 41, 37, 28, 16,  3, 61,
   54, 58, 35, 52, 50, 42, 21, 44,
   38, 32, 29, 23, 17, 11,  4, 62,
   46, 55, 26, 59, 40, 36, 15, 53,
   34, 51, 20, 43, 31, 22, 10, 45,
   25, 39, 14, 33, 19, 30,  9, 24,
   13, 18,  8, 12,  7,  6,  5, 63]
# Bit Scan Reverse using De Bruijn multiplication
# Undefined for b == 0
# Returns the index of the most significant one bit
# https://www.chessprogramming.org/BitScan#De_Bruijn_Multiplication_2
# authors Kim Walisch, Mark Dickinson
def BSR(b: np.uint64()) -> int:
	debruijn64 = np.uint64(0x03f79d71b4cb0a89)
	# assert b != 0
	b |= b >> np.uint(0x01)
	b |= b >> np.uint(0x02)
	b |= b >> np.uint(0x04)
	b |= b >> np.uint(0x08)
	b |= b >> np.uint(0x10)
	b |= b >> np.uint(0x20)
	return bsr_index[(b * debruijn64) >> np.uint64(58)]

# https://www.chessprogramming.org/Population_Count#Brian_Kernighan.27s_way
def POPCOUNT(b) -> int:
	count = 0
	while (b):
		count += 1
		b &= b - np.uint64(1) # reset LS1B
	return count

def generateBoard():
	pass

def generateEmptyBoard():
	pass

def wIsInCheck():
	pass