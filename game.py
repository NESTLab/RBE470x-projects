import random
import board
import agent

########
# Game #
########

class Game(object):
    """Game logic class"""

    def __init__(self, w, h, n, p1, p2, rseed):
        """Class costructor"""
        # Create board
        self.board = board.Board([[0] * w for i in range(h)], w, h, n)
        # Set random seed
        random.seed(rseed)
        # Players
        self.players = [ p1, p2 ]
        p1.player = 1
        p2.player = 2

    def go(self):
        # Current player
        p = 0
        while self.board.free_cols() and self.board.get_outcome() == 0:
            self.board.print_it()
            while True:
                x = self.players[p].go(self.board)
                print(self.players[p].name, "move:", x)
                if x in self.board.free_cols():
                    break
                else:
                    print("Illegal move, retry...")
            # Legal move, add token there
            self.board.add_token(x)
            # Switch player
            if p == 0:
                p = 1
            else:
                p = 0
        # Print game outcome
        self.board.print_it()
        print("Game over!")
        o = self.board.get_outcome()
        if o == 0:
            print("It's a tie!")
        else:
            print(self.players[o-1].name, "won!")
