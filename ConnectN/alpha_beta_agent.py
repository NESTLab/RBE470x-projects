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
        parent_node = alpha_beta_node.AlphaBetaNode(brd, None, None)
        parent_node.children = self.make_children(parent_node, 0)
        return self.find_max_node(parent_node).col

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
    # RETURN [int] eval: The likely hood of either player winning.
    # 0-1; 1 meaning AI will win and 0 meaning the other player will win
    def get_evaluation(self, brd):
        return None

    def make_children(self, node, level):
        children = []
        if level < self.max_depth:
            successors = self.get_successors(node.board)
            for successor in successors:
                new_node = alpha_beta_node.AlphaBetaNode(successor[0], successor[1], random.random())
                children.append(new_node)
            for new_child in children:
                new_child.children = self.make_children(new_child, level + 1)
        else:
            return children
        return children

    # Get the max node from the tree.
    #
    # PARAM [alpha_beta_node.AlphaBetaNode] parent_node: the root node of the tree
    # RETURN [alpha_beta_node.AlphaBetaNode] max_node: The node with the max value
    # found using alpha-beta-pruning
    def find_max_node(self, parent_node):
        return parent_node.children[0]
