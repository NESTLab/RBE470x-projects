import math
import agent
import time
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
    def __init__(self, name):
        super().__init__(name)
        # Max search depth
        self.max_depth = 0
        self.moves = 0
        self.eval = 0
        self.ai_player = 0

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        # Your code here
        self.ai_player = (self.player % 2 + 1)
        self.moves += 1
        if self.moves <= 5 and brd.w >= 9:
            self.max_depth = 3
        else:
            self.max_depth = 4
        tik = time.perf_counter()
        move_col = self.alpha_beta_search(brd)
        tok = time.perf_counter()
        print(f"Made move in {tok - tik:0.4f} seconds")
        print("We called the eval " + str(self.eval) + " times")
        return move_col

    def reorganize_successors(self, successors, brd):
        new_successors = []
        last_successors = []
        for successor in successors:
            if (brd.w * (1 / 3) - 1) <= successor[1] <= (brd.w * (2 / 3)):
                new_successors.append(successor)
            else:
                last_successors.append(successor)
        return new_successors + last_successors

    # The first level of an Alpha-Beta search that kicks off the rest.
    # Separated because the moves need to be tracked at the first level
    #
    # PARAM [board.Board] brd: the board state
    # RETURN [int]: the column of the move evaluated to be best
    def alpha_beta_search(self, brd):
        # Array of possible moves
        possible_moves = []
        successors = self.get_successors(brd)
        successors = self.reorganize_successors(successors, brd)
        alpha = -math.inf
        beta = math.inf
        # For each possible move
        for successor in successors:
            brd = successor[0]
            col = successor[1]
            # create new node, evaluation created by alpha-beta searching all possible children to max_depth
            new_node = alpha_beta_node.AlphaBetaNode(brd, col, self.min_value(brd, self.max_depth, alpha, beta))
            # check if the move wins and if so return immediately
            if new_node.evaluation == math.inf:
                return new_node.col
            elif new_node.evaluation > alpha:
                alpha = new_node.evaluation
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
        value = -math.inf
        # If node is terminal, than we have lost
        if brd.get_outcome() == self.ai_player:
            return -math.inf
        elif brd.get_outcome() == self.player:
            return math.inf
        # If depth = 0, than we need to use the heuristic
        if depth == 0:
            return self.get_evaluation(brd)
        # Now we evaluate each possible next move
        successors = self.get_successors(brd)
        successors = self.reorganize_successors(successors, brd)
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
        value = math.inf
        # If node is terminal, than we have lost
        if brd.get_outcome() == self.ai_player:
            return -math.inf
        elif brd.get_outcome() == self.player:
            return math.inf
        # If depth = 0, than we need to use the heuristic
        if depth == 0:
            return self.get_evaluation(brd)
        # Now we evaluate each possible next move
        successors = self.get_successors(brd)
        successors = self.reorganize_successors(successors, brd)
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
        self.eval += 1
        eval_score = 0
        ai_player = self.player % 2 + 1
        if brd.n == 4:
            eval_score = (self.get_three_token_connect4(brd, self.player) * 50 + self.get_two_token(brd,
                                                                                              self.player) * 10 - self.get_three_token_connect4(
                    brd, ai_player) * 50 - self.get_two_token(brd, ai_player) * 10)
        elif brd.n == 5:
            eval_score = (self.get_four_token(brd, self.player) * 500 + self.get_three_token_connect5(brd,
                                                                                                self.player) * 50 + self.get_two_token(
                    brd, self.player) * 10 - self.get_four_token(brd, ai_player) * 500 - self.get_three_token_connect5(brd,
                                                                                                     ai_player) * 50 - self.get_two_token(
                    brd, ai_player) * 10)
        return eval_score


    def get_one_token(self, brd, player):
        score = 0
        for x in range(brd.w - 1):
            for y in range(brd.h - 1):
                if brd.board[y][x] == player:
                    score += 1
        return score

    def get_two_token(self, brd, player):
        score = 0
        # Check for pairs horizontally.
        for x in range(brd.w - brd.n):
            for y in range(brd.h - 1):
                count = 0
                for token in range(brd.n - 1):
                    if brd.board[y][x + token] == player:
                        count += 1
                    elif brd.board[y][x + token] == 0:
                        count = count
                    else:
                        count -= 1
                if count == 2:
                    score += 1
        # Check for pairs vertically.
        for x in range(brd.w - 1):
            for y in range(brd.h - brd.n):
                count = 0
                for token in range(brd.n - 1):
                    if brd.board[y + token][x] == player:
                        count += 1
                    elif brd.board[y + token][x] == 0:
                        count = count
                    else:
                        count -= 1
                if count == 2:
                    score += 1

        # Check for pairs bottom left to top right /
        for x in range(brd.w - brd.n):
            for y in range(brd.h - brd.n):
                count = 0
                for token in range(brd.n - 1):
                    if brd.board[y + token][x + token] == player:
                        count += 1
                    elif brd.board[y + token][x + token] == 0:
                        count = count
                    else:
                        count -= 1
                if count == 2:
                    score += 1

        # Check for pairs top left to bottom right \
        for x in range(brd.w - brd.n):
            for y in range(brd.n - 1, brd.h):
                count = 0
                for token in range(brd.n - 1):
                    if brd.board[y - token][x + token] == player:
                        count += 1
                    elif brd.board[y - token][x + token] == 0:
                        count = count
                    else:
                        count -= 1
                if count == 2:
                    score += 1
        return score

    def get_three_token_connect4(self, brd, player):
        score = 0
        # Check for row of 3 tokens horizontally
        for x in range(brd.w - 4):
            for y in range(brd.h - 1):
                if ((brd.board[y][x] == player) and (brd.board[y][x + 1] == player) and (brd.board[y][x + 2] == player) and (
                        brd.board[y][x + 3] == 0)) \
                        or ((brd.board[y][x] == player) and (brd.board[y][x + 1] == player) and (brd.board[y][x + 2] == 0) and (
                        brd.board[y][x + 3] == player)) \
                        or ((brd.board[y][x] == player) and (brd.board[y][x + 1] == 0) and (brd.board[y][x + 2] == player) and (
                        brd.board[y][x + 3] == player)) \
                        or ((brd.board[y][x] == 0) and (brd.board[y][x + 1] == player) and (brd.board[y][x + 2] == player) and (
                        brd.board[y][x + 3] == player)):
                    score += 1
        # Check for row of 3 tokens vertically
        for x in range(brd.w - 1):
            for y in range(brd.h - 4):
                if brd.board[y][x] == player and brd.board[y + 1][x] == player and brd.board[y + 2][x] == player and brd.board[y + 3][x] == 0:
                    score += 1
        # Check for row of 3 tokens bottom left to top right
        for x in range(brd.w - 4):
            for y in range(brd.h - 4):
                if ((brd.board[y][x] == player) and (brd.board[y + 1][x + 1] == player) and (brd.board[y + 2][x + 2] == player) and (
                        brd.board[y + 3][x + 3] == 0)) \
                        or ((brd.board[y][x] == player) and (brd.board[y + 1][x + 1] == player) and (brd.board[y + 2][x + 2] == 0) and (
                        brd.board[y + 3][x + 3] == player)) \
                        or ((brd.board[y][x] == player) and (brd.board[y + 1][x + 1] == 0) and (brd.board[y + 2][x + 2] == player) and (
                        brd.board[y + 3][x + 3] == player)) \
                        or ((brd.board[y][x] == 0) and (brd.board[y + 1][x + 1] == player) and (brd.board[y + 2][x + 2] == player) and (
                        brd.board[y + 3][x + 3] == player)):
                    score += 1
        # Check for row of 3 tokens top left to bottom right
        for x in range(brd.w - 4):
            for y in range(brd.h - 4):
                if ((brd.board[y + 3][x] == player) and (brd.board[y + 2][x + 1] == player) and (brd.board[y + 1][x + 2] == player) and (
                        brd.board[y][x + 3] == 0)) \
                        or (
                        (brd.board[y + 3][x] == player) and (brd.board[y + 2][x + 1] == player) and (brd.board[y + 1][x + 2] == 0) and (
                        brd.board[y][x + 3] == player)) \
                        or (
                        (brd.board[y + 3][x] == player) and (brd.board[y + 2][x + 1] == 0) and (brd.board[y + 1][x + 2] == player) and (
                        brd.board[y][x + 3] == player)) \
                        or (
                        (brd.board[y + 3][x] == 0) and (brd.board[y + 2][x + 1] == player) and (brd.board[y + 1][x + 2] == player) and (
                        brd.board[y][x + 3] == player)):
                    score += 1
        return score

    def get_three_token_connect5(self, brd, player):
        score = 0
        # Check for row of 3 tokens horizontally
        for x in range(brd.w - 5):
            for y in range(brd.h - 1):
                if ((brd.board[y][x] == player) and (brd.board[y][x + 1] == player) and (brd.board[y][x + 2] == player) and (
                        brd.board[y][x + 3] == 0) and (brd.board[y][x + 4] == 0)) \
                        or ((brd.board[y][x] == player) and (brd.board[y][x + 1] == player) and (brd.board[y][x + 2] == 0) and (
                        brd.board[y][x + 3] == player) and (brd.board[y][x + 4] == 0)) \
                        or ((brd.board[y][x] == player) and (brd.board[y][x + 1] == player) and (brd.board[y][x + 2] == 0) and (
                        brd.board[y][x + 3] == 0) and (brd.board[y][x + 4] == player)) \
                        or ((brd.board[y][x] == player) and (brd.board[y][x + 1] == 0) and (brd.board[y][x + 2] == player) and (
                        brd.board[y][x + 3] == player) and (brd.board[y][x + 4] == 0)) \
                        or ((brd.board[y][x] == player) and (brd.board[y][x + 1] == 0) and (brd.board[y][x + 2] == player) and (
                        brd.board[y][x + 3] == 0) and (brd.board[y][x + 4] == player)) \
                        or ((brd.board[y][x] == player) and (brd.board[y][x + 1] == 0) and (brd.board[y][x + 2] == 0) and (
                        brd.board[y][x + 3] == player) and (brd.board[y][x + 4] == player)) \
                        or ((brd.board[y][x] == 0) and (brd.board[y][x + 1] == 0) and (brd.board[y][x + 2] == player) and (
                        brd.board[y][x + 3] == player) and (brd.board[y][x + 4] == player)) \
                        or ((brd.board[y][x] == 0) and (brd.board[y][x + 1] == player) and (brd.board[y][x + 2] == player) and (
                        brd.board[y][x + 3] == player) and (brd.board[y][x + 4] == 0)) \
                        or ((brd.board[y][x] == 0) and (brd.board[y][x + 1] == player) and (brd.board[y][x + 2] == player) and (
                        brd.board[y][x + 3] == 0) and (brd.board[y][x + 4] == player)) \
                        or ((brd.board[y][x] == 0) and (brd.board[y][x + 1] == player) and (brd.board[y][x + 2] == 0) and (
                        brd.board[y][x + 3] == player) and (brd.board[y][x + 4] == player)):
                    score += 1
        # Check for row of 3 tokens vertically
        for x in range(brd.w - 1):
            for y in range(brd.h - 5):
                if brd.board[y][x] == player and brd.board[y + 1][x] == player and brd.board[y + 2][x] == player and brd.board[y + 3][
                    x] == 0 and brd.board[y + 4][x] == 0:
                    score += 1
        # Check for row of 3 tokens bottom left to top right
        for x in range(brd.w - 5):
            for y in range(brd.h - 5):
                if ((brd.board[y][x] == player) and (brd.board[y + 1][x + 1] == player) and (brd.board[y + 2][x + 2] == player) and (
                        brd.board[y + 3][x + 3] == 0) and (brd.board[y + 4][x + 4] == 0)) \
                        or ((brd.board[y][x] == player) and (brd.board[y + 1][x + 1] == player) and (brd.board[y + 2][x + 2] == 0) and (
                        brd.board[y + 3][x + 3] == player) and (brd.board[y + 4][x + 4] == 0)) \
                        or ((brd.board[y][x] == player) and (brd.board[y + 1][x + 1] == player) and (brd.board[y + 2][x + 2] == 0) and (
                        brd.board[y + 3][x + 3] == 0) and (brd.board[y + 4][x + 4] == player)) \
                        or ((brd.board[y][x] == player) and (brd.board[y + 1][x + 1] == 0) and (brd.board[y + 2][x + 2] == player) and (
                        brd.board[y + 3][x + 3] == player) and (brd.board[y + 4][x + 4] == 0)) \
                        or ((brd.board[y][x] == player) and (brd.board[y + 1][x + 1] == 0) and (brd.board[y + 2][x + 2] == player) and (
                        brd.board[y + 3][x + 3] == 0) and (brd.board[y + 4][x + 4] == player)) \
                        or ((brd.board[y][x] == player) and (brd.board[y + 1][x + 1] == 0) and (brd.board[y + 2][x + 2] == 0) and (
                        brd.board[y + 3][x + 3] == player) and (brd.board[y + 4][x + 4] == player)) \
                        or ((brd.board[y][x] == 0) and (brd.board[y + 1][x + 1] == 0) and (brd.board[y + 2][x + 2] == player) and (
                        brd.board[y + 3][x + 3] == player) and (brd.board[y + 4][x + 4] == player)) \
                        or ((brd.board[y][x] == 0) and (brd.board[y + 1][x + 1] == player) and (brd.board[y + 2][x + 2] == player) and (
                        brd.board[y + 3][x + 3] == player) and (brd.board[y + 4][x + 4] == 0)) \
                        or ((brd.board[y][x] == 0) and (brd.board[y + 1][x + 1] == player) and (brd.board[y + 2][x + 2] == player) and (
                        brd.board[y + 3][x + 3] == 0) and (brd.board[y + 4][x + 4] == player)) \
                        or ((brd.board[y][x] == 0) and (brd.board[y + 1][x + 1] == player) and (brd.board[y + 2][x + 2] == 0) and (
                        brd.board[y + 3][x + 3] == player) and (brd.board[y + 4][x + 4] == player)):
                    score += 1
        # Check for row of 3 tokens top left to bottom right
        for x in range(brd.w - 5):
            for y in range(brd.h - 5):
                if ((brd.board[y + 4][x] == player) and (brd.board[y + 3][x + 1] == player) and (brd.board[y + 2][x + 2] == player) and (
                        brd.board[y + 1][x + 3] == 0) and (brd.board[y][x + 4] == 0)) \
                        or (
                        (brd.board[y + 4][x] == player) and (brd.board[y + 3][x + 1] == player) and (brd.board[y + 2][x + 2] == 0) and (
                        brd.board[y + 1][x + 3] == player) and (brd.board[y][x + 4] == 0)) \
                        or (
                        (brd.board[y + 4][x] == player) and (brd.board[y + 3][x + 1] == player) and (brd.board[y + 2][x + 2] == 0) and (
                        brd.board[y + 1][x + 3] == 0) and (brd.board[y][x + 4] == player)) \
                        or (
                        (brd.board[y + 4][x] == player) and (brd.board[y + 3][x + 1] == 0) and (brd.board[y + 2][x + 2] == player) and (
                        brd.board[y + 1][x + 3] == player) and (brd.board[y][x + 4] == 0)) \
                        or (
                        (brd.board[y + 4][x] == player) and (brd.board[y + 3][x + 1] == 0) and (brd.board[y + 2][x + 2] == player) and (
                        brd.board[y + 1][x + 3] == 0) and (brd.board[y][x + 4] == player)) \
                        or ((brd.board[y + 4][x] == player) and (brd.board[y + 3][x + 1] == 0) and (brd.board[y + 2][x + 2] == 0) and (
                        brd.board[y + 1][x + 3] == player) and (brd.board[y][x + 4] == player)) \
                        or ((brd.board[y + 4][x] == 0) and (brd.board[y + 3][x + 1] == 0) and (brd.board[y + 2][x + 2] == player) and (
                        brd.board[y + 1][x + 3] == player) and (brd.board[y][x + 4] == player)) \
                        or (
                        (brd.board[y + 4][x] == 0) and (brd.board[y + 3][x + 1] == player) and (brd.board[y + 2][x + 2] == player) and (
                        brd.board[y + 1][x + 3] == player) and (brd.board[y][x + 4] == 0)) \
                        or (
                        (brd.board[y + 4][x] == 0) and (brd.board[y + 3][x + 1] == player) and (brd.board[y + 2][x + 2] == player) and (
                        brd.board[y + 1][x + 3] == 0) and (brd.board[y][x + 4] == player)) \
                        or ((brd.board[y + 4][x] == 0) and (brd.board[y + 3][x + 1] == player) and (brd.board[y + 2][x + 2] == 0) and (
                        brd.board[y + 1][x + 3] == player) and (brd.board[y][x + 4] == player)):
                    score += 1
        return score

    def get_four_token(self, brd, player):
        score = 0
        # Check for row of 4 tokens horizontally
        for x in range(brd.w - 5):
            for y in range(brd.h - 1):
                if ((brd.board[y][x] == player) and (brd.board[y][x + 1] == player) and (brd.board[y][x + 2] == player) and (
                        brd.board[y][x + 3] == player) and (brd.board[y][x + 4] == 0)) \
                        or ((brd.board[y][x] == player) and (brd.board[y][x + 1] == player) and (brd.board[y][x + 2] == player) and (
                        brd.board[y][x + 3] == 0) and (brd.board[y][x + 4] == player)) \
                        or ((brd.board[y][x] == player) and (brd.board[y][x + 1] == player) and (brd.board[y][x + 2] == 0) and (
                        brd.board[y][x + 3] == player) and (brd.board[y][x + 4] == player)) \
                        or ((brd.board[y][x] == player) and (brd.board[y][x + 1] == 0) and (brd.board[y][x + 2] == player) and (
                        brd.board[y][x + 3] == player) and (brd.board[y][x + 4] == player)) \
                        or ((brd.board[y][x] == 0) and (brd.board[y][x + 1] == player) and (brd.board[y][x + 2] == player) and (
                        brd.board[y][x + 3] == player) and (brd.board[y][x + 4] == player)):
                    score += 1
        # Check for row of 4 tokens vertically
        for x in range(brd.w - 1):
            for y in range(brd.h - 5):
                if brd.board[y][x] == player and brd.board[y + 1][x] == player and brd.board[y + 2][x] == player and brd.board[y + 3][
                    x] == player and brd.board[y + 4][x] == 0:
                    score += 1
        # Check for row of 4 tokens bottom left to top right
        for x in range(brd.w - 5):
            for y in range(brd.h - 5):
                if ((brd.board[y][x] == player) and (brd.board[y + 1][x + 1] == player) and (brd.board[y + 2][x + 2] == player) and (
                        brd.board[y + 3][x + 3] == player) and (brd.board[y + 4][x + 4] == 0)) \
                        or (
                        (brd.board[y][x] == player) and (brd.board[y + 1][x + 1] == player) and (brd.board[y + 2][x + 2] == player) and (
                        brd.board[y + 3][x + 3] == 0) and (brd.board[y + 4][x + 4] == player)) \
                        or ((brd.board[y][x] == player) and (brd.board[y + 1][x + 1] == player) and (brd.board[y + 2][x + 2] == 0) and (
                        brd.board[y + 3][x + 3] == player) and (brd.board[y + 4][x + 4] == player)) \
                        or ((brd.board[y][x] == player) and (brd.board[y + 1][x + 1] == 0) and (brd.board[y + 2][x + 2] == player) and (
                        brd.board[y + 3][x + 3] == player) and (brd.board[y + 4][x + 4] == player)) \
                        or ((brd.board[y][x] == 0) and (brd.board[y + 1][x + 1] == player) and (brd.board[y + 2][x + 2] == player) and (
                        brd.board[y + 3][x + 3] == player) and (brd.board[y + 4][x + 4] == player)):
                    score += 1
        # Check for row of 4 tokens top left to bottom right
        for x in range(brd.w - 5):
            for y in range(brd.h - 5):
                if ((brd.board[y + 4][x] == player) and (brd.board[y + 3][x + 1] == player) and (brd.board[y + 2][x + 2] == player) and (
                        brd.board[y + 1][x + 3] == player) and (brd.board[y][x + 4] == 0)) \
                        or ((brd.board[y + 4][x] == player) and (brd.board[y + 3][x + 1] == player) and (
                        brd.board[y + 2][x + 2] == player) and (brd.board[y + 1][x + 3] == 0) and (brd.board[y][x + 4] == player)) \
                        or (
                        (brd.board[y + 4][x] == player) and (brd.board[y + 3][x + 1] == player) and (brd.board[y + 2][x + 2] == 0) and (
                        brd.board[y + 1][x + 3] == player) and (brd.board[y][x + 4] == player)) \
                        or (
                        (brd.board[y + 4][x] == player) and (brd.board[y + 3][x + 1] == 0) and (brd.board[y + 2][x + 2] == player) and (
                        brd.board[y + 1][x + 3] == player) and (brd.board[y][x + 4] == player)) \
                        or (
                        (brd.board[y + 4][x] == 0) and (brd.board[y + 3][x + 1] == player) and (brd.board[y + 2][x + 2] == player) and (
                        brd.board[y + 1][x + 3] == player) and (brd.board[y][x + 4] == player)):
                    score += 1
        return score
