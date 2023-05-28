import numpy as np
from ctypes import c_uint64

import timeit

import time

# Cython directive
# cython: profile=True

# Cython has an issue with exposing C constants to Python.
# This workaround was suggested 
#A_FILE = A_FILE_enum
#B_FILE = B_FILE_enum
#C_FILE = C_FILE_enum
#D_FILE = D_FILE_enum
#E_FILE = E_FILE_enum
#F_FILE = F_FILE_enum
#G_FILE = G_FILE_enum
#H_FILE = H_FILE_enum
	

#MYSTRING = MYSTRING_DEFINE 
#A_FILE = A_FILE_DEFINE

cdef size_t A_FILE = 0x0101010101010101
cdef size_t B_FILE = 0x0202020202020202
cdef size_t C_FILE = 0x0404040404040404
cdef size_t D_FILE = 0x0808080808080808
cdef size_t E_FILE = 0x1010101010101010
cdef size_t F_FILE = 0x2020202020202020
cdef size_t G_FILE = 0x4040404040404040
cdef size_t H_FILE = 0x8080808080808080


BITBOARD_TO_SQUARE = {}

cpdef void initBitboards():
	# Provides access to a bitboard array to quickly switch between square number and bitboard representation.
	for i in range(64):
		SQUARE_TO_BITBOARD[i] = <size_t> 0x01 << i
		BITBOARD_TO_SQUARE[np.uint64(0x01)] = i

cpdef size_t eastOne(size_t b):
	return (b << 1) & ~A_FILE

cpdef eastOneCython(size_t b):
	cdef size_t afile = 0x0101010101010101
	return b << 1 & ~afile

cpdef size_t westOne(size_t b):
	return b >> 1 & ~H_FILE

cpdef size_t northOne(size_t b):
	return b << 8

cpdef northOneCython(size_t b):
	return b << 8

cpdef size_t southOne(size_t b):
	return b >> 8

# These are called Kogge-Stone algorithms.
# They also exist for lateral and diagonal fills.
'''
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
'''

cpdef size_t northFill(size_t b):
	b |= b << 8
	b |= b << 16
	b |= b << 32
	return b

cpdef size_t southFill(size_t b):
	b |= b >> 8
	b |= b >> 16
	b |= b >> 32
	return b

cpdef size_t fileFill(size_t b):
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
'''
def BSF(b: np.uint64()) -> int:
	debruijn64 = np.uint64(0x03f79d71b4cb0a89)
	#assert b != 0 # Keeping the assert doubles the cost of the function from 1.5 to 3 nanoseconds.
	return bsf_index[((b & -b) * debruijn64) >> np.uint64(58)]
'''


bsf2_index = [
	0, 47,  1, 56, 48, 27,  2, 60,
   57, 49, 41, 37, 28, 16,  3, 61,
   54, 58, 35, 52, 50, 42, 21, 44,
   38, 32, 29, 23, 17, 11,  4, 62,
   46, 55, 26, 59, 40, 36, 15, 53,
   34, 51, 20, 43, 31, 22, 10, 45,
   25, 39, 14, 33, 19, 30,  9, 24,
   13, 18,  8, 12,  7,  6,  5, 63
]

def BSF2(b: int):
	debruijn64 = 0x03f79d71b4cb0a89
	return bsf_index[c_uint64((b ^ (b-1)) * debruijn64).value  >> 58]

cpdef size_t BSF(size_t b):
	cdef size_t debruijn64 = 0x03f79d71b4cb0a89
	return bsf2_index[((b ^ (b-1)) * debruijn64) >> 58]

cpdef runBSFRepeated(size_t n):
	cy = timeit.timeit('bb.BSF3(10483)', setup='import bitboard as bb', number=n)

	setup = '''
import bitboard as bb
import numpy as np
	'''
	py = timeit.timeit('bb.BSF(np.uint64(10483))', setup=setup, number=n)
	print(cy, py)
	print('Cython is {}x faster than Python'.format(py/cy) )
	#start = time.time()
	#for i in range(n):
	#	BSF(i)
	#end = time.time()
	#print(f"Total tm: {start-end}")

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
cpdef size_t BSR(size_t b):
	cdef size_t debruijn64 = 0x03f79d71b4cb0a89
	# assert b != 0
	b |= b >> 0x01
	b |= b >> 0x02
	b |= b >> 0x04
	b |= b >> 0x08
	b |= b >> 0x10
	b |= b >> 0x20
	return bsr_index[(b * debruijn64) >> 58]

# https://www.chessprogramming.org/Population_Count#Brian_Kernighan.27s_way
'''
def POPCOUNT(b) -> int:
	count = 0
	while (b):
		count += 1
		b &= b - np.uint64(1) # reset LS1B
	return count
'''

cpdef size_t POPCOUNT(size_t b):
	cdef size_t count = 0
	while (b):
		count += 1
		b &= b - 1 # reset LS1B
	return count

def generateBoard():
	pass

def generateEmptyBoard():
	pass

def wIsInCheck():
	pass