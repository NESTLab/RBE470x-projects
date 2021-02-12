import math
import agent
import random
import alpha_beta_node


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
        move_col = self.alpha_beta_search(brd)
        return move_col

    # The first level of an Alpha-Beta search that kicks off the rest.
    # Separated because the moves need to be tracked at the first level
    #
    # PARAM [board.Board] brd: the board state
    # RETURN [int]: the column of the move evaluated to be best
    def alpha_beta_search(self, brd):
        # Array of possible moves
        possible_moves = []
        successors = self.get_successors(brd)
        # For each possible move
        for successor in successors:
            brd = successor[0]
            col = successor[1]
            # create new node, evaluation created by alpha-beta searching all possible children to max_depth
            new_node = alpha_beta_node.AlphaBetaNode(brd, col, self.min_value(brd, self.max_depth, 0, 1))
            # check if the move wins and if so return immediately
            if new_node.evaluation == 1:
                return new_node.col
            # Add to the array
            possible_moves.append(new_node)
        # Assign Starting Vals to find the best move
        highest_move_val = 0
        move_col = 1
        # Find the column associated with the best move
        for move in possible_moves:
            if move.evaluation >= highest_move_val:
                move_col = move.col
                highest_move_val = move.evaluation
        return move_col

    # find the maximum assured score from a given board
    #
    # PARAM [board.Board] brd: the board state
    # PARAM [int] depth: levels of depth to explore
    # PARAM [float] min_bound:
    # PARAM [float] max_bound:
    # RETURN [float] maximum assured score
    def max_value(self, brd, depth, min_bound, max_bound):
        value = 0.0
        # If node is terminal, than we have lost
        if brd.get_outcome() != 0:
            return value
        # If depth = 0, than we need to use the heuristic
        if depth == 0:
            return self.get_evaluation(brd)
        # Now we evaluate each possible next move
        successors = self.get_successors(brd)
        for successor in successors:
            brd = successor[0]
            value = max(value, self.min_value(brd, depth - 1, min_bound, max_bound))
            min_bound = max(value, min_bound)
            if min_bound >= max_bound:
                return value
        return value

    # find the minimum assured score from a given board
    #
    # PARAM [board.Board] brd: the board state
    # PARAM [int] depth: levels of depth to explore
    # PARAM [float] min_bound:
    # PARAM [float] max_bound:
    # RETURN [float] minimum assured score
    def min_value(self, brd, depth, min_bound, max_bound):
        value = 1.0
        # If node is terminal, than we have lost
        if brd.get_outcome() != 0:
            return value
        # If depth = 0, than we need to use the heuristic
        if depth == 0:
            return self.get_evaluation(brd)
        # Now we evaluate each possible next move
        successors = self.get_successors(brd)
        for successor in successors:
            brd = successor[0]
            value = min(value, self.max_value(brd, depth - 1, min_bound, max_bound))
            min_bound = min(value, max_bound)
            if max_bound <= min_bound:
                return value
        return value

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
            succ.append((nb, col))
        return succ

    # Get the evaluation of the given board.
    #
    # PARAM [board.Board] brd: the board state
    # RETURN [float] eval: The likely hood of either player winning.
    # 0-1; 1 meaning AI will win and 0 meaning the other player will win
    def get_evaluation(self, brd):
        return random.random()
