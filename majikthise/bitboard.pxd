cdef size_t A_FILE = 0x0101010101010101
cdef size_t B_FILE = 0x0202020202020202
cdef size_t C_FILE = 0x0404040404040404
cdef size_t D_FILE = 0x0808080808080808
cdef size_t E_FILE = 0x1010101010101010
cdef size_t F_FILE = 0x2020202020202020
cdef size_t G_FILE = 0x4040404040404040
cdef size_t H_FILE = 0x8080808080808080

cdef size_t A1_H8_DIAGONAL = 0x8040201008040201
cdef size_t H1_A8_ANTIDIAGONAL = 0x0102040810204080
cdef size_t LIGHT_SQUARES = 0x55AA55AA55AA55AA
cdef size_t DARK_SQUARES = 0xAA55AA55AA55AA55

cpdef size_t BSF(size_t b)
cpdef size_t BSR(size_t b)
cpdef size_t POPCOUNT(size_t b)

cpdef void initBitboards()
cpdef size_t SQUARE_TO_BITBOARD[64]


cpdef size_t eastOne(size_t b)
cpdef size_t westOne(size_t b)
cpdef size_t northOne(size_t b)
cpdef size_t southOne(size_t b)

cpdef size_t northFill(size_t b)
cpdef size_t southFill(size_t b)
cpdef size_t fileFill(size_t b)