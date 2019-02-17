import math
import agent
import heuristics as heu
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
        super().__init__(name)  # super contains player number
        # Max search depth
        self.max_depth = max_depth
        self.numMoves = self.player
        self.curr_depth = 0
        self.column = 0



    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        bestCol = 0
        num_steps = 0
        alpha = -math.inf
        beta = math.inf
        bestVal = 0
        all_successors = self.get_successors(brd)
        for boardstate in all_successors:
#            currVal = heu.negamax(self, boardstate[0], alpha, beta, 0)
#            if currVal == 0:
            currVal = heu.simple_heuristic(boardstate[0], boardstate[1])
            if currVal > bestVal:
                bestVal = currVal
                bestCol = boardstate[1]

        return bestCol
    # Get the successors of the given board.
    #
    # PARAM [board.Board] brd: the board state
    # RETURN [list of (board.Board, int)]: a list of the successor boards,
    #                                      along with the column where the last
    #                                      token was added in it
    def get_successors(self, brd):
        """Returns the reachable boards from the given board brd. The return value is a tuple (new board state, column number where last token was added)."""
        # Get possible actions
        self.numMoves += 1
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
            succ.append((nb, col))
        return succ

THE_AGENT = AlphaBetaAgent("XiaoJeffrey", 4)