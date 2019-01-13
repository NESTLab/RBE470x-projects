import math
import agent

###########################
# Alpha-Beta Search Agent #
###########################

class AlphaBetaAgent(agent.Agent):
    """Agent that uses alpha-beta search"""

    def __init__(self, name, max_depth):
        super().__init__(name)
        # Max search depth
        self.max_depth = max_depth

    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        # Your code here

    def get_successors(self, b):
        """Returns the reachable boards from the given board b. The return value is a tuple (new board state, column number where last token was added)."""
        # Get possible moves
        freecols = b.free_cols()
        # Is there any?
        if not freecols:
            return []
        # Make a list of the new boards with that move added
        succ = []
        for c in freecols:
            # Make new board with added move
            nb = b.copy()
            nb.add_token(c)
            # Add board to list
            succ.append((nb,c))
        return succ
