from board import Position

class Engine:

    # restrict search to this moves only
    searchmoves = 5
    depth = 5
    plies = 5
    movetime = 10000

    move_list = []

    def __init__(self, debug=False):
        self.debug = debug
        self.position = Position()
        
    