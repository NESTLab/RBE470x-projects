import copy

##############
# Game Board #
##############

class Board(object):

    def __init__(self, board, w, h, n):
        """Class constructor"""
        # Board data
        self.board = board
        # Board width
        self.w = w
        # Board height
        self.h = h
        # How many tokens in a row to win
        self.n = n
        # Current player
        self.player = 1

    def copy(self):
        """Returns a copy of this board that can be independently modified"""
        cpy = Board(copy.deepcopy(self.board), self.w, self.h, self.n)
        cpy.player = self.player
        return cpy

    def is_line_at(self, x, y, dx, dy):
        """Return True if a line of identical symbols exists starting at (x,y) in direction (dx,dy)"""
        # Avoid out-of-bounds errors
        if ((x + (self.n-1) * dx >= self.w) or
            (y + (self.n-1) * dy < 0) or (y + (self.n-1) * dy >= self.h)):
            return False
        # Get token at (x,y)
        t = self.board[y][x]
        # Go through elements
        for i in range(1, self.n):
            if self.board[y + i*dy][x + i*dx] != t:
                return False
        return True

    def is_any_line_at(self, x, y):
        """Return True if a line of identical symbols exists starting at (x,y) in any direction"""
        return (self.is_line_at(x, y, 1, 0) or # Horizontal
                self.is_line_at(x, y, 0, 1) or # Vertical
                self.is_line_at(x, y, 1, 1) or # Diagonal up
                self.is_line_at(x, y, 1, -1)) # Diagonal down

    def get_outcome(self):
        """Returns the winner of the game: 1 for Player 1, 2 for Player 2, and 0 for no winner"""
        for x in range(self.w):
            for y in range(self.h):
                if (self.board[y][x] != 0) and self.is_any_line_at(x,y):
                    return self.board[y][x]
        return 0

    def add_token(self, x):
        """Adds a token for the current player at column x; the column is assumed not full"""
        # Find empty slot for token
        y = 0
        while self.board[y][x] != 0:
            y = y + 1
        self.board[y][x] = self.player
        # Switch player
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1

    def free_cols(self):
        """Returns a list of the columns with at least one free slot"""
        return [x for x in range(self.w) if self.board[-1][x] == 0 ]

    def print_it(self):
        print("+", "-" * self.w, "+", sep='')
        for y in range(self.h-1, -1, -1):
            print("|", sep='', end='')
            for x in range(self.w):
                if self.board[y][x] == 0:
                    print(" ", end='')
                else:
                    print(self.board[y][x], end='')
            print("|")
        print("+", "-" * self.w, "+", sep='')
        print(" ", end='')
        for i in range(self.w):
            print(i, end='')
        print("")
