import random

##############
# Game Board #
##############

class C4Board:

    def __init__(self, board, w, h):
        """Class constructor"""
        # Board data
        self.board = board
        # Board width
        self.w = w
        # Board height
        self.h = h

    def isLineAt(self, x, y, dx, dy):
        """Return True if a line of identical symbols exists starting at (x,y) in direction (dx,dy)"""
        # Avoid out-of-bounds errors
        if ((x + 3 * dx >= self.w) or
            (y + 3 * dy < 0) or (y + 3 * dy >= self.h)):
            return False
        # Get token at (x,y)
        t = self.board[y][x]
        # Go through elements
        for i in [1,2,3]:
            if self.board[y + i*dy][x + i*dx] != t:
                return False
        return True

    def isAnyLineAt(self, x, y):
        """Return True if a line of identical symbols exists starting at (x,y) in any direction"""
        return (self.isLineAt(x, y, 1, 0) or # Horizontal
                self.isLineAt(x, y, 0, 1) or # Vertical
                self.isLineAt(x, y, 1, 1) or # Diagonal up
                self.isLineAt(x, y, 1, -1)) # Diagonal down

    def getOutcome(self):
        """Returns the winner of the game: 1 for Player 1, 2 for Player 2, and 0 for no winner"""
        for x in range(self.w):
            for y in range(self.h):
                if (self.board[y][x] != 0) and self.isAnyLineAt(x,y):
                    return self.board[y][x]
        return 0

    def addToken(self, p, x):
        """Adds a token for player p at column x; the column is assumed not full"""
        # Find empty slot for token
        y = 0
        while self.board[y][x] != 0:
            y = y + 1
        self.board[y][x] = p

    def freeCols(self):
        """Returns a list of the columns with at least one free slot"""
        return [x for x in range(self.w) if self.board[-1][x] == 0 ]

    def printIt(self):
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

#####################
# Agent definitions #
#####################

class C4Agent:
    """Abstract agent class"""
    
    def __init__(self, name):
        """Class constructor"""
        # Agent name
        self.name = name

    def go(self, board):
        """Returns a column between 0 and (board.w-1). The column must be free in the board."""
        raise NotImplementedError("Please implement this method")

class RandomC4Agent(C4Agent):
    """Randomly playing agent"""

    def go(self, board):
        return random.choice(board.freeCols())

class InteractiveC4Agent(C4Agent):
    """Interactive player"""

    def go(self, board):
        return int(input("Which column?"))

########
# Game #
########

class Game:

    def __init__(self, w, h, p1, p2, rseed):
        """Class costructor"""
        # Create board
        self.board = C4Board([[0] * w for i in range(h)], w, h)
        # Set random seed
        random.seed(rseed)
        # Create players
        self.players = [ p1, p2 ]

    def go(self):
        # Current player
        p = 0
        while self.board.freeCols() and self.board.getOutcome() == 0:
            self.board.printIt()
            while True:
                x = self.players[p].go(self.board)
                print(self.players[p].name, "move:", x)
                if x in self.board.freeCols():
                    break
                else:
                    print("Illegal move, retry...")
            # Legal move, add token there
            self.board.addToken(p+1, x)
            # Switch player
            if p == 0:
                p = 1
            else:
                p = 0
        # Print game outcome
        self.board.printIt()
        print("Game over!")
        o = self.board.getOutcome()
        if o == 0:
            print("It's a tie!")
        else:
            print(self.players[o-1].name, "won!")

g = Game(7, 6, RandomC4Agent("random1"), RandomC4Agent("random2"), 1)
g.go()

