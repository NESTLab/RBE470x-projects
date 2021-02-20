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
        self.first_move = True
        self.max_time = 0

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        # Your code here
        if self.first_move:
            self.first_move = False
            return int(brd.w / 2)
        self.ai_player = (self.player % 2 + 1)
        self.moves += 1
        if self.moves <= 6 and brd.w >= 9:
            self.max_depth = 3
        else:
            self.max_depth = 4
        tik = time.perf_counter()
        move_col = self.alpha_beta_search(brd)
        tok = time.perf_counter()
        new_time = tok - tik
        if new_time > self.max_time:
            self.max_time = new_time
        print(f"Made move in {tok - tik:0.4f} seconds")
        print("We called the eval " + str(self.eval) + " times")
        print("We have a max time of " + str(self.max_time) + " seconds")
        return move_col

    @staticmethod
    def reorganize_successors(successors, brd):
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
            new_node = alpha_beta_node.AlphaBetaNode(brd, col, self.min_value(brd, self.max_depth-1, alpha, beta))
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
        if brd.get_outcome() == self.player:
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
            max_bound = min(value, max_bound)
            if max_bound <= min_bound:
                return value
        return value

    # Get the successors of the given board.
    #
    # PARAM [board.Board] brd: the board state
    # RETURN [list of (board.Board, int)]: a list of the successor boards,
    #                                      along with the column where the last
    #                                      token was added in it
    @staticmethod
    def get_successors(brd):
        """Returns the reachable boards from the given board brd. The return value is a tuple
        (new board state, column number where last token was added)."""
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
    # RETURN [float] eval: The evaluation score.
    def get_evaluation(self, brd):
        self.eval += 1
        eval_score = 0
        if brd.n == 4:
            (player_3, player_2, player_1, opponent_3, opponent_2, opponent_1) = self.connect_4_possibilities(brd)
            eval_score = (player_3 * 50 + player_2 * 10 + player_1 * 1
                          - opponent_3 * 50 - opponent_2 * 10 - opponent_1 * 1)
        if brd.n == 5:
            (player_4, player_3, player_2, player_1, opponent_4, opponent_3, opponent_2, opponent_1) \
                = self.connect_5_possibilities(brd)
            eval_score = (player_4 * 500 + player_3 * 50 + player_2 * 10 + player_1 * 1
                          - opponent_4 * 500 - opponent_3 * 50 - opponent_2 * 10 - opponent_1 * 1)
        return eval_score

    # Count possible rows for a connect 4 board
    #
    # PARAM [board.Board] brd: the board state
    # RETURN [int] player_3: number of possible player matches with 3 out of 4 taken
    # RETURN [int] player_2: number of possible player matches with 2 out of 4 taken
    # RETURN [int] player_1: number of possible player matches with 1 out of 4 taken
    # RETURN [int] opponent_3: number of possible opponent matches with 3 out of 4 taken
    # RETURN [int] opponent_2: number of possible opponent matches with 2 out of 4 taken
    # RETURN [int] opponent_1: number of possible opponent matches with 1 out of 4 taken
    # Return Format: (player_3, player_2, player_1, opponent_3, opponent_2, opponent_1)
    def connect_4_possibilities(self, brd):
        # define return variables
        player_3, player_2, player_1, opponent_3, opponent_2, opponent_1 = 0, 0, 0, 0, 0, 0
        # for every tile on the board
        for x in range(brd.w - 1):
            for y in range(brd.h - 1):
                # Check Horizontal
                (current_player, match_score) = self.is_line_at(brd, x, y, 1, 0)
                if current_player == self.player:
                    if match_score == 1:
                        player_1 += 1
                    if match_score == 2:
                        player_2 += 1
                    if match_score == 3:
                        player_3 += 1
                elif current_player == self.ai_player:
                    if match_score == 1:
                        opponent_1 += 1
                    if match_score == 2:
                        opponent_2 += 1
                    if match_score == 3:
                        opponent_3 += 1
                # Check Vertical
                (current_player, match_score) = self.is_line_at(brd, x, y, 0, 1)
                if current_player == self.player:
                    if match_score == 1:
                        player_1 += 1
                    if match_score == 2:
                        player_2 += 1
                    if match_score == 3:
                        player_3 += 1
                elif current_player == self.ai_player:
                    if match_score == 1:
                        opponent_1 += 1
                    if match_score == 2:
                        opponent_2 += 1
                    if match_score == 3:
                        opponent_3 += 1
                # Check Up Diagonal
                (current_player, match_score) = self.is_line_at(brd, x, y, 1, 1)
                if current_player == self.player:
                    if match_score == 1:
                        player_1 += 1
                    if match_score == 2:
                        player_2 += 1
                    if match_score == 3:
                        player_3 += 1
                elif current_player == self.ai_player:
                    if match_score == 1:
                        opponent_1 += 1
                    if match_score == 2:
                        opponent_2 += 1
                    if match_score == 3:
                        opponent_3 += 1
                # Check Down Diagonal
                (current_player, match_score) = self.is_line_at(brd, x, y, 1, -1)
                if current_player == self.player:
                    if match_score == 1:
                        player_1 += 1
                    if match_score == 2:
                        player_2 += 1
                    if match_score == 3:
                        player_3 += 1
                elif current_player == self.ai_player:
                    if match_score == 1:
                        opponent_1 += 1
                    if match_score == 2:
                        opponent_2 += 1
                    if match_score == 3:
                        opponent_3 += 1
        return player_3, player_2, player_1, opponent_3, opponent_2, opponent_1

        # Count possible rows for a connect 5 board
        #
        # PARAM [board.Board] brd: the board state
        # RETURN [int] player_4: number of possible player matches with 4 out of 5 taken
        # RETURN [int] player_3: number of possible player matches with 3 out of 5 taken
        # RETURN [int] player_2: number of possible player matches with 2 out of 5 taken
        # RETURN [int] player_1: number of possible player matches with 1 out of 5 taken
        # RETURN [int] opponent_4: number of possible opponent matches with 4 out of 5 taken
        # RETURN [int] opponent_3: number of possible opponent matches with 3 out of 5 taken
        # RETURN [int] opponent_2: number of possible opponent matches with 2 out of 5 taken
        # RETURN [int] opponent_1: number of possible opponent matches with 1 out of 5 taken
        # Return Format: (player_4, player_3, player_2, player_1, opponent_4, opponent_3, opponent_2, opponent_1)

    def connect_5_possibilities(self, brd):
        # define return variables
        player_4, player_3, player_2, player_1, opponent_4, opponent_3, opponent_2, opponent_1 = 0, 0, 0, 0, 0, 0, 0, 0
        # for every tile on the board
        for x in range(brd.w - 1):
            for y in range(brd.h - 1):
                # Check Horizontal
                (current_player, match_score) = self.is_line_at(brd, x, y, 1, 0)
                if current_player == self.player:
                    if match_score == 1:
                        player_1 += 1
                    if match_score == 2:
                        player_2 += 1
                    if match_score == 3:
                        player_3 += 1
                    if match_score == 4:
                        player_4 += 1
                elif current_player == self.ai_player:
                    if match_score == 1:
                        opponent_1 += 1
                    if match_score == 2:
                        opponent_2 += 1
                    if match_score == 3:
                        opponent_3 += 1
                    if match_score == 4:
                        opponent_4 += 1
                # Check Vertical
                (current_player, match_score) = self.is_line_at(brd, x, y, 0, 1)
                if current_player == self.player:
                    if match_score == 1:
                        player_1 += 1
                    if match_score == 2:
                        player_2 += 1
                    if match_score == 3:
                        player_3 += 1
                    if match_score == 4:
                        player_4 += 1
                elif current_player == self.ai_player:
                    if match_score == 1:
                        opponent_1 += 1
                    if match_score == 2:
                        opponent_2 += 1
                    if match_score == 3:
                        opponent_3 += 1
                    if match_score == 4:
                        opponent_4 += 1
                # Check Up Diagonal
                (current_player, match_score) = self.is_line_at(brd, x, y, 1, 1)
                if current_player == self.player:
                    if match_score == 1:
                        player_1 += 1
                    if match_score == 2:
                        player_2 += 1
                    if match_score == 3:
                        player_3 += 1
                    if match_score == 4:
                        player_4 += 1
                elif current_player == self.ai_player:
                    if match_score == 1:
                        opponent_1 += 1
                    if match_score == 2:
                        opponent_2 += 1
                    if match_score == 3:
                        opponent_3 += 1
                    if match_score == 4:
                        opponent_4 += 1
                # Check Down Diagonal
                (current_player, match_score) = self.is_line_at(brd, x, y, 1, -1)
                if current_player == self.player:
                    if match_score == 1:
                        player_1 += 1
                    if match_score == 2:
                        player_2 += 1
                    if match_score == 3:
                        player_3 += 1
                    if match_score == 4:
                        player_4 += 1
                elif current_player == self.ai_player:
                    if match_score == 1:
                        opponent_1 += 1
                    if match_score == 2:
                        opponent_2 += 1
                    if match_score == 3:
                        opponent_3 += 1
                    if match_score == 4:
                        opponent_4 += 1
        return player_4, player_3, player_2, player_1, opponent_4, opponent_3, opponent_2, opponent_1

    # check for a possible match line.  Will count past un-taken spaces, so 0 x 0 x is two in a row
    #
    # PARAM [board.Board] brd: the board state
    # PARAM [int] x: x position to start
    # PARAM [int] y: y position to start
    # PARAM [int] dx: travel in x
    # PARAM [int] dy: travel in y
    # RETURN [int] player: player who owns possible match (0 means no possible match)
    # RETURN [int] match_length number of tokens in possible match
    # Return Format: (player, match_length)
    @staticmethod
    def is_line_at(brd, x, y, dx, dy):
        current_player = brd.board[y][x]
        if current_player != 0:
            match_length = 1
        else:
            match_length = 0
        for z in [1, 2, 3]:  # checks one over, than two over, than three over
            if x + (dx * z) >= brd.w or \
                    y + (dy * z) >= brd.h or \
                    y + (dy * z) < 0:  # Checking for oot-of-bounds
                return 0, match_length
            current_location_val = brd.board[y + (dy * z)][x + (dx * z)]
            if current_location_val == 0:   # do nothing
                pass
            elif current_player == 0:  # If starting at zero and found a player
                current_player = current_location_val
                match_length += 1
            elif current_location_val != current_player:  # if players don't match
                return 0, match_length
            elif current_location_val == current_player:  # if players do match
                match_length += 1
        return current_player, match_length
