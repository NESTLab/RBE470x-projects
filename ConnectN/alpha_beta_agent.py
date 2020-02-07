import math
import agent
import board
import random

###########################
# Alpha-Beta Search Agent #
###########################

class AlphaBetaAgent(agent.Agent):
    """Agent that uses alpha-beta search"""

    # Class constructor.
    #
    # PARAM [string] name:      the name of this player
    # PARAM [int]    max_depth: the maximum search depth
    def __init__(self, name, max_depth):
        super().__init__(name)
        # Max search depth
        self.max_depth = max_depth

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        # Your code here

        # Read board
        succ = self.getall_succ(brd, 1)

        print("All Successors")
        max = -1
        move = -1
        for s in succ:
            # print(s[0].print_it())
            # print("\tMove: ", s[1])
            h = self.evalbrd(s[0])
            print((h, s[1]))
            if max < h:
                max = h
                move = s[1]
        print("End")

        # Interpret using heurisitcs
        # Create graph and load in heuristics

        # Call alpha beta on graph

        # Make decision
        # return random.choice(brd.free_cols())
        return move

    # Get the successors of the given board.
    #
    # PARAM [board.Board] brd: the board state
    # RETURN [list of (board.Board, int)]: a list of the successor boards,
    #                                      along with the column where the last
    #                                      token was added in it
    def get_successors(self, brd):
        """Returns the reachable boards from the given board brd. The return value is a tuple (new board state, column number where last token was added)."""
        # Get possible actions
        freecols = brd.free_cols()
        # Are there legal actions left?
        if not freecols:
            return []
        # Make a list of the new boards along with the corresponding actions
        succ = []
        for col in freecols:
            # Clone the original board
            nb = brd.copy()
            # Add a token to the new board
            # (This internally changes nb.player, check the method definition!)
            nb.add_token(col)
            # Add board to list of successors
            succ.append((nb,col))
        return succ

    # Get all the possible configurations x number of moves deep
    #
    # PARAM [board.Board] brd: the current board state
    # PARAM [int] depth: number of moves deep
    # RETURN [list of (board.Board, int)]: a list of the successor boards,
    #                                      along with the column where the last
    #
    def getall_succ(self, brd, depth):
        all_succ = []
        brd_succ = self.get_successors(brd)

        if depth > 1:
            for b in brd_succ:
                all_succ += self.getall_succ(b[0], depth-1)

        if depth == 1:
            return brd_succ
        return all_succ

    # Evaluates the given board configuration
    #
    # PARAM [board.Board] brd: the board state
    # RETURN [int] heuristic value for given board
    #
    def evalbrd(self, brd):
        return random.randint(0, 100)
