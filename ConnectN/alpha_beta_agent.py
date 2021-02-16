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
    # PARAM [int] max_depth: the maximum search depth
    # PARAM [int] to_win: number of pieces in a row to win
    # PARAM [bool] isPlayer1: true if the AI is player 1
    def __init__(self, name, max_depth, to_win):
        super().__init__(name)
        # Max search depth
        self.max_depth = max_depth
        # Num of pieces in a row to win
        self.to_win = to_win
        self.player = 0


    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""


        # find opponent token
        if self.player == 0:
            self.player = self.find_player(brd)


        return self.find_best_column(brd)

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

    # use the minimax algorithm to choose the best column to add to
    #
    # PARAM  [board.Board] brd: the current board state
    # RETURN [int]: index of the column to add a the next move
    #
    def find_best_column(self, brd):
        val = float('-inf')
        move = -1
        for child in self.get_successors(brd):
            next_brd = child[0]
            next_move = child[1]
            found_val = self.minimax(next_brd, self.max_depth, True)
            if found_val > val:
                val = found_val
                move = next_move
        return move

    # minimax algorithm to be called by go
    #
    # PARAM  [board.Board] brd: the board state
    # PARAM  [int] depth: the max depth of recursive calls
    # PARAM  [bool] max_node: determins if max or min node
    # RETURN [float]: value of given decision tree
    #
    def minimax(self, brd, depth, max_node):
        # is the game over?
        if depth == 0 or len(brd.free_cols()) == 0 or brd.get_outcome() != 0:
            res = self.evaluate(brd)
            return res
        # max
        if max_node:
            v = float('-inf')
            for child in self.get_successors(brd):
                res = self.minimax(child[0], depth-1, False)
                v = max(v, res)
            return v
        # min
        v = float('inf')
        for child in self.get_successors(brd):
            res = self.minimax(child[0], depth-1, True)
            v = min(v, res)
        return v

    def evaluate(self, brd):
        # TODO
        # COUNT NUMBER OF TRAPS (7 SHAPE)

        # if self.player == 2:
            # Be Deffensive = weight the other player MORE than yourse
        


        return self.num_in_a_row(brd) + self.win_bonus(brd)
    
    def win_bonus(self, brd):
        outcome = brd.get_outcome()
        if self.player == outcome:
            return 200
        elif outcome != 0:
            return -200
        else:
            return 0

    # UNFINISHED
    def num_in_a_row(self, brd):
        # each points[i] is number of occurances with i+1 in a row
        pos_points = []
        for _ in range(self.to_win):
            pos_points.append(0)
        h = brd.h
        w = brd.w
        # horizontal
        good_seen = 0
        for row in brd.board:
            for col in row:
                if col == self.player:
                    good_seen = good_seen + 1
                else:
                    good_seen = 0
        # vertical
        good_seen = 0
        for col in range(w):
            for row in range(h):
                if brd.board[row][col] == self.player:
                    good_seen = good_seen + 1
                elif good_seen > 0 and good_seen-1 < len(pos_points):
                    pos_points[good_seen-1] = pos_points[good_seen-1] + 1
                    good_seen = 0
        
        # TODO ***********
        # diagnal

        # count points
        result = 0
        for v in pos_points:
            result = result * self.quad_scalar(v)
        return result
    

    # helper function to num_in_a_row which adds 1 to the value at the index of point-1
    #
    # PARAM  [list of int] lst: number of n in a row at index = n-1
    # PARAM  [int] point: longest re-occurance of peices found in a arow
    #
    def add_to_points_list(self, lst, point):
        if point > 0 and point-1 < len(lst):
            lst[point-1] = lst[point-1] + 1

    # equation used to value larger n_in_a_row occurances exponentially greater
    #
    # PARAM  [int] x: n_in_a_row
    # RETURN [float]: scalar value used to weigh number of occurances of n_in_a_row
    #
    def quad_scalar(self, x):
        return x*x*x/self.to_win
        
    # run once at the first move of the agent, finding which piece to place
    # [PARAM] brd: board from game
    # [int]: which player the AI is playing as
    #
    def find_player(self, brd):
        for row in brd.board:
            for col in row:
                if col != 0:
                    return 2
        return 1