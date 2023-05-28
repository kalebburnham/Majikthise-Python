cdef class CBoard:

    cdef public fen
    cdef public dict pieceBoards

    cdef public list pieceLocations

    cdef public size_t whiteBoard
    cdef public size_t blackBoard
    #self.whiteBoard = None
    #self.blackBoard = None
    cdef public size_t occupied

    cpdef removePiece(self, color, piece, bbSquare)
    cpdef putPiece(self, piece, color, square)
    
    cpdef updateColorBoards(self)

    




