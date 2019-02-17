import math


# /**
#  * Recursively score connect 4 position using negamax variant of alpha-beta algorithm.
#  * @param: alpha < beta, a score window within which we are evaluating the position.
#  *
#  * @return the exact score, an upper or lower bound score depending of the case:
#  * - if actual score of position <= alpha then actual score <= return value <= alpha
#  * - if actual score of position >= beta then beta <= return value <= actual score
#  * - if alpha <= actual score <= beta then return value = actual score
#  */


def negamax(agent, board, alpha, beta, num_steps):
    if num_steps == agent.max_depth:  # give up if no solution
        return 0

    assert (alpha < beta)
    all_successors = agent.get_successors(board)
    for boardstate in all_successors:
        if boardstate[0].get_outcome() == agent.player:
                return (1000 + num_steps)  # our player

    beta_max = math.inf  # set upper bound
    if beta > beta_max:
        beta = beta_max  # there is no need to keep beta above our max possible score.
        if alpha >= beta:
            return beta  # prune the exploration if the [alpha;beta] window is empty.

    num_steps += 1

    for boardstate in all_successors:  # compute the score of all possible next move and keep the best one
        # It's opponent turn in P2 position after current player plays x column.
        score = -negamax(agent, boardstate[0], -beta, -alpha, num_steps)
        if score >= beta:
            return score  # prune
        if score > alpha:
            alpha = score  # set alpha
    return alpha


class ValueColPair(object):
    def __init__(self, value, column):
        self.value = value
        self.column = column


def simple_heuristic(board, col):
    y = get_token_row(board, col)
    value = 0
    value += is_partial_line_at(board, col, y, 1, 0)
    value += is_partial_line_at(board, col, y, 0, 1)
    value += is_partial_line_at(board, col, y, 1, 1)
    value += is_partial_line_at(board, col, y, 1, -1)
    return value


def is_partial_line_at(board, x, y, dx, dy):
    """Return True if a line of identical tokens exists starting at (x,y) in direction (dx,dy)"""
    # Avoid out-of-bounds errors
    total = 0
    if ((x + (board.n - 1) * dx >= board.w) or
            (y + (board.n - 1) * dy < 0) or (y + (board.n - 1) * dy >= board.h)):
        return 0
    # Get token at (x,y)
    t = board.board[y][x]  # t is our player

    my_count = 0
    other_count = 0
    my_in_a_row = True
    other_in_a_row = True
    if t == 1:
        other = 2
    else:
        other = 1

    # Go through elements
    for i in range(1, board.n):
        curr_token = board.board[y + i * dy][x + i * dx]
        if my_in_a_row is True and curr_token == t:
            my_count += 1
        else:
            my_in_a_row = False

        if other_in_a_row is True and curr_token == other:
            other_count += 1
        else:
            other_in_a_row = False

    total = my_count + other_count - 1

    if other_count == board.n - 1:  # if blocking an opponent's gamewinning move
        total = 500 + other_count  # give blocking a move priority over everything else if not guaranteed win

    return total


def get_token_row(boardstate, col):  # gets the token at the top of the column
    y = 0
    while boardstate.board[y][col] != 0 and y < boardstate.h - 1:
        y = y + 1
    return y
