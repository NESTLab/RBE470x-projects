import math
import agent

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
        (value, col) = self.minmax_value(brd, -math.inf, math.inf, 0, True)
        return col

    # Maximize or minimize value of next move
    #
    # PARAM
    # RETURN [(int, int)] : tuple with the best possible value and the
    #                       corresponding move choice
    def minmax_value(self, state, alpha, beta, level, maximize):
        if level >= self.max_depth:
            return self.heuristic(state, maximize)

        # -inf if max level, +inf if min level
        value = -math.inf if maximize else math.inf
        bestCol = -1
        # test each column choice
        for (child_state, col) in self.get_successors(state):
            if maximize:
                # MAX_VALUE option
                value = max(value, self.minmax_value(child_state, alpha, beta, level + 1, False))
                if value >= alpha:
                    alpha = value
                    bestCol = col
            else:
                # MIN_VALUE option
                value = min(value, self.minmax_value(child_state, alpha, beta, level + 1, True))
                if value <= beta:
                    beta = value
                    bestCol = col

            # check pruning condition
            if alpha >= beta:
                return value, bestCol

        return value, bestCol

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

    def heuristic(self, state, maximize):
        # initialize result value
        result = 0

        # check board for 1, 2, or 3-in a row formations

        # backup win/loss check - heavily weighted
        # 1 for Player 1, 2 for Player 2, 0 for neither
        end_check = state.get_outcome()
        return 0